"""Tests for expanded segments: data tools, scoring, product design, prompts."""
import uuid

import pytest

from app.agent.prompts import SEGMENT_CONTEXT, build_system_prompt
from app.models.session import SessionState
from app.segments.loader import SegmentRegistry
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.data import *  # noqa: F401,F403
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.product.design import MORATORIUM_TRIGGERS
from app.tools.registry import ToolRegistry, ToolResultStatus
from app.tools.scoring.score import SEGMENT_WEIGHTS


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(
    state: SessionState = SessionState.VERIFIED,
    confirmed: bool = False,
    maker: bool = False,
):
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="LENDER_001",
        borrower_confirmed=confirmed,
        maker_approved=maker,
    )


ALL_NEW_SEGMENTS = [
    "WAREHOUSE_RECEIPT", "GOLD_LOAN", "EV_FINANCING", "SOLAR_FINANCING",
    "SHG_MEMBER", "TRADER_AGRI", "MSE_MANUFACTURING", "STREET_VENDOR",
    "STUDENT_HOUSING", "TRUCK_OPERATOR", "AUTO_RICKSHAW", "BEAUTY_SALON",
    "DHABA_RESTAURANT", "POULTRY_FARMER", "FISHERY", "HANDLOOM_WEAVER",
    "TAILORING_UNIT", "MEDICAL_SHOP", "SUGARCANE_FARMER", "VEGETABLE_GROWER",
    "FPO_ENTITY", "NBFC_BC", "CONSTRUCTION_WORKER", "DOMESTIC_WORKER",
    "E_RICKSHAW", "MICRO_HOUSING", "DAIRY_PROCESSOR", "AGRI_INPUT_DEALER",
    "RENTAL_INCOME", "COTTON_FARMER", "RICE_MILLER", "EDTECH_STUDENT",
    "HEALTH_CLINIC", "MICRO_CONTRACTOR", "CAB_DRIVER",
]

ORIGINAL_SEGMENTS = ["DAIRY_FARMER", "KIRANA_SHOP", "GIG_WORKER"]


# --- Segment YAML loading ---

def test_all_33_segments_load():
    SegmentRegistry.clear()
    count = SegmentRegistry.load_from_directory("segments")
    all_segments = SegmentRegistry.get_all()
    for seg_id in ORIGINAL_SEGMENTS + ALL_NEW_SEGMENTS:
        assert seg_id in all_segments, f"Segment {seg_id} not loaded"
    assert count >= 33


def test_segment_yaml_structure():
    SegmentRegistry.clear()
    SegmentRegistry.load_from_directory("segments")
    for seg_id in ALL_NEW_SEGMENTS:
        seg = SegmentRegistry.get(seg_id)
        assert seg is not None, f"Segment {seg_id} missing"
        assert seg.channel == "whatsapp"
        assert len(seg.languages) >= 1
        assert len(seg.required_sources) >= 2
        assert seg.scoring_model != ""
        assert len(seg.scoring_features) >= 5
        product = seg.product
        assert "type" in product
        assert "amount_range" in product
        assert "tenure_range" in product


# --- Scoring weights ---

def test_all_segments_have_scoring_weights():
    for seg_id in ORIGINAL_SEGMENTS + ALL_NEW_SEGMENTS:
        assert seg_id in SEGMENT_WEIGHTS, f"Missing weights for {seg_id}"
        weights = SEGMENT_WEIGHTS[seg_id]
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.02, (
            f"Weights for {seg_id} sum to {total}, expected ~1.0"
        )


# --- Prompt context ---

def test_all_segments_have_prompt_context():
    for seg_id in ORIGINAL_SEGMENTS + ALL_NEW_SEGMENTS:
        assert seg_id in SEGMENT_CONTEXT, (
            f"Missing prompt context for {seg_id}"
        )
        assert len(SEGMENT_CONTEXT[seg_id]) > 50


def test_build_system_prompt_with_segment():
    SegmentRegistry.clear()
    SegmentRegistry.load_from_directory("segments")
    seg = SegmentRegistry.get("GOLD_LOAN")
    prompt = build_system_prompt(
        lender_name="TestLender",
        segment=seg,
        language="hi",
    )
    assert "GOLD_LOAN" in prompt
    assert "TestLender" in prompt
    assert "SEGMENT-SPECIFIC GUIDANCE" in prompt
    assert "gold" in prompt.lower()


# --- New data tools ---

NEW_DATA_TOOLS = {
    "fetch_warehouse_receipt": {"receipt_id": "WR-001"},
    "fetch_gold_appraisal": {"appraisal_id": "GA-001"},
    "fetch_ev_telematics": {"vehicle_id": "EV-001"},
    "fetch_solar_generation": {"installation_id": "SOL-001"},
    "fetch_shg_records": {"group_id": "SHG-001"},
    "fetch_vehicle_telematics": {"vehicle_id": "TRK-001"},
    "fetch_poultry_data": {"farmer_id": "PLT-001"},
    "fetch_fishery_data": {"member_id": "FSH-001"},
    "fetch_fpo_data": {"registration_id": "FPO-001"},
    "fetch_upi_transactions": {"merchant_id": "UPI-001"},
    "fetch_property_records": {"property_id": "PROP-001"},
    "fetch_edtech_data": {"student_id": "STU-001"},
}


@pytest.mark.asyncio
async def test_new_data_tools_registered():
    for name in NEW_DATA_TOOLS:
        tool = ToolRegistry.get(name)
        assert tool is not None, f"Tool '{name}' not registered"
        assert tool.category.value == "data"


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name,kwargs", NEW_DATA_TOOLS.items())
async def test_new_data_tool_execution(tool_name, kwargs):
    executor = ToolExecutor()
    result = await executor.execute(tool_name, _ctx(), **kwargs)
    assert result.status == ToolResultStatus.SUCCESS
    assert isinstance(result.data, dict)
    assert len(result.data) > 0


@pytest.mark.asyncio
async def test_new_data_tools_blocked_unverified():
    executor = ToolExecutor()
    ctx = _ctx(state=SessionState.UNVERIFIED)
    for name, kwargs in NEW_DATA_TOOLS.items():
        result = await executor.execute(name, ctx, **kwargs)
        assert result.status == ToolResultStatus.BLOCKED, (
            f"Tool {name} should be blocked in UNVERIFIED"
        )


# --- Segment scoring ---

@pytest.mark.asyncio
async def test_segment_scoring_new_segments():
    from app.tools.scoring.score import compute_segment_score

    for seg_id in ALL_NEW_SEGMENTS:
        result = await compute_segment_score(
            segment=seg_id,
            features={k: 0.7 for k in SEGMENT_WEIGHTS[seg_id]},
        )
        assert 0 <= result["score"] <= 900
        assert result["grade"] in ("A1", "A2", "B1", "B2", "REJECT")
        assert result["model_version"] == f"{seg_id.lower()}_score_v1"


# --- Product design ---

@pytest.mark.asyncio
async def test_product_design_new_segments():
    from app.tools.product.design import design_dynamic_product

    for seg_id in ALL_NEW_SEGMENTS:
        result = await design_dynamic_product(
            segment=seg_id,
            score=650,
            interest_rate=15.0,
            requested_amount=100000,
            monthly_income=30000,
        )
        assert float(result["amount"]) > 0
        assert float(result["interest_rate"]) > 0
        assert result["tenure_months"] > 0
        assert result["schedule_type"] != ""


# --- Moratorium triggers ---

def test_moratorium_triggers_coverage():
    segments_with_triggers = {
        "DAIRY_FARMER", "WAREHOUSE_RECEIPT", "EV_FINANCING",
        "SOLAR_FINANCING", "SHG_MEMBER", "POULTRY_FARMER",
        "FISHERY", "SUGARCANE_FARMER", "VEGETABLE_GROWER",
        "COTTON_FARMER", "CONSTRUCTION_WORKER", "STREET_VENDOR",
        "TRUCK_OPERATOR", "AUTO_RICKSHAW", "E_RICKSHAW",
        "CAB_DRIVER", "MICRO_HOUSING", "EDTECH_STUDENT",
    }
    for seg_id in segments_with_triggers:
        triggers = MORATORIUM_TRIGGERS.get(seg_id, [])
        assert len(triggers) >= 1, (
            f"Missing moratorium triggers for {seg_id}"
        )
