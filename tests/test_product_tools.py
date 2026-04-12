import uuid

import pytest

from app.models.session import SessionState
from app.segments.loader import SegmentRegistry
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.product import *  # noqa: F401,F403
from app.tools.registry import ToolRegistry, ToolResultStatus


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(state=SessionState.VERIFIED):
    return ExecutionContext(session_id=uuid.uuid4(), session_state=state, lender_id="L1")


@pytest.mark.asyncio
async def test_all_5_product_tools_registered():
    names = {
        "design_dynamic_product",
        "generate_seasonal_schedule",
        "generate_daily_micro_schedule",
        "generate_payout_linked_schedule",
        "compute_insurance_premium",
    }
    for name in names:
        assert ToolRegistry.get(name) is not None


@pytest.mark.asyncio
async def test_design_dairy_product():
    ex = ToolExecutor()
    r = await ex.execute(
        "design_dynamic_product",
        _ctx(),
        segment="DAIRY_FARMER",
        score=680,
        requested_amount=100000,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["schedule_type"] == "SEASONAL_DYNAMIC"
    assert r.data["insurance_type"] == "PASHU_BIMA"
    assert len(r.data["moratorium_triggers"]) == 2


@pytest.mark.asyncio
async def test_design_kirana_product():
    ex = ToolExecutor()
    r = await ex.execute(
        "design_dynamic_product",
        _ctx(),
        segment="KIRANA_SHOP",
        score=600,
        requested_amount=200000,
    )
    assert r.data["schedule_type"] == "DAILY_MICRO"
    assert r.data["insurance_type"] is None


@pytest.mark.asyncio
async def test_seasonal_schedule():
    ex = ToolExecutor()
    r = await ex.execute(
        "generate_seasonal_schedule",
        _ctx(),
        amount=100000,
        rate=15.0,
        tenure_months=12,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert len(r.data["entries"]) == 12
    seasons = {e["season"] for e in r.data["entries"]}
    assert "flush" in seasons or "lean" in seasons


@pytest.mark.asyncio
async def test_daily_micro_schedule():
    ex = ToolExecutor()
    r = await ex.execute(
        "generate_daily_micro_schedule",
        _ctx(),
        amount=100000,
        rate=16.0,
        tenure_months=12,
    )
    assert r.data["schedule_type"] == "DAILY_MICRO"
    assert r.data["working_days_per_month"] == 26


@pytest.mark.asyncio
async def test_payout_linked_schedule():
    ex = ToolExecutor()
    r = await ex.execute(
        "generate_payout_linked_schedule",
        _ctx(),
        amount=50000,
        avg_monthly_payout=22000,
        deduction_rate=0.15,
    )
    assert r.data["schedule_type"] == "PAYOUT_LINKED"
    assert r.data["deduction_rate"] == 0.15


@pytest.mark.asyncio
async def test_insurance_premium():
    ex = ToolExecutor()
    r = await ex.execute(
        "compute_insurance_premium",
        _ctx(),
        insurance_type="PASHU_BIMA",
        sum_insured=100000,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert float(r.data["annual_premium"]) > 0


def test_segment_template_loading():
    SegmentRegistry.clear()
    count = SegmentRegistry.load_from_directory("segments")
    assert count >= 33

    dairy = SegmentRegistry.get("DAIRY_FARMER")
    assert dairy is not None
    assert dairy.channel == "whatsapp"
    assert "CREDIT_BUREAU" in dairy.required_sources
    assert dairy.scoring_model == "dairy_score_v1"
    assert len(dairy.scoring_features) == 6

    kirana = SegmentRegistry.get("KIRANA_SHOP")
    assert kirana is not None
    assert kirana.product["type"] == "DAILY_MICRO"

    gig = SegmentRegistry.get("GIG_WORKER")
    assert gig is not None
    assert gig.product["type"] == "PAYOUT_LINKED"
    SegmentRegistry.clear()
