import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.registry import ToolRegistry, ToolResultStatus
from app.tools.scoring import *  # noqa: F401,F403


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(state=SessionState.VERIFIED, confirmed=False, maker=False):
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="LENDER_001",
        borrower_confirmed=confirmed,
        maker_approved=maker,
    )


@pytest.mark.asyncio
async def test_all_8_scoring_tools_registered():
    names = {
        "evaluate_segment_policy", "compute_segment_score", "compute_risk_pricing",
        "check_fraud_signals", "generate_cam", "run_what_if",
        "check_psl_classification", "generate_explainability",
    }
    for name in names:
        assert ToolRegistry.get(name) is not None, f"'{name}' not registered"


@pytest.mark.asyncio
async def test_policy_approve():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_segment_policy", _ctx(),
        segment="DAIRY_FARMER", score=700, confidence_level="HIGH",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["decision"] == "APPROVE"


@pytest.mark.asyncio
async def test_policy_refer():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_segment_policy", _ctx(),
        segment="DAIRY_FARMER", score=550, confidence_level="HIGH",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["decision"] == "REFER"


@pytest.mark.asyncio
async def test_policy_reject_fraud():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_segment_policy", _ctx(),
        segment="DAIRY_FARMER", score=700, fraud_clear=False,
    )
    assert r.data["decision"] == "REJECT"


@pytest.mark.asyncio
async def test_segment_score():
    ex = ToolExecutor()
    r = await ex.execute(
        "compute_segment_score", _ctx(),
        segment="DAIRY_FARMER",
        features={"pouring_regularity": 0.92, "bureau_score": 720, "bank_stability": 0.85},
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert 0 <= r.data["score"] <= 900


@pytest.mark.asyncio
async def test_risk_pricing():
    ex = ToolExecutor()
    r = await ex.execute("compute_risk_pricing", _ctx(), score=700)
    assert r.data["rate_band"] == "A2"


@pytest.mark.asyncio
async def test_fraud_pass():
    ex = ToolExecutor()
    r = await ex.execute(
        "check_fraud_signals", _ctx(),
        aadhaar_hash="abc", device_fingerprint="fp1",
    )
    assert r.data["result"] == "PASS"


@pytest.mark.asyncio
async def test_fraud_velocity():
    ex = ToolExecutor()
    r = await ex.execute(
        "check_fraud_signals", _ctx(),
        applications_48h=5, device_fingerprint="fp1",
    )
    assert r.data["result"] in ("HOLD", "REJECT")


@pytest.mark.asyncio
async def test_cam_generation():
    ex = ToolExecutor()
    r = await ex.execute(
        "generate_cam", _ctx(),
        borrower_name="Ramesh", segment="DAIRY_FARMER",
        score=550, score_grade="B1", income_monthly=42000,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert "Ramesh" in r.data["borrower_summary"]


@pytest.mark.asyncio
async def test_psl_dairy():
    ex = ToolExecutor()
    r = await ex.execute("check_psl_classification", _ctx(), segment="DAIRY_FARMER")
    assert r.data["eligible"] is True
    assert r.data["category"] == "Agriculture"


@pytest.mark.asyncio
async def test_psl_gig():
    ex = ToolExecutor()
    r = await ex.execute("check_psl_classification", _ctx(), segment="GIG_WORKER")
    assert r.data["eligible"] is False


@pytest.mark.asyncio
async def test_explainability():
    ex = ToolExecutor()
    r = await ex.execute(
        "generate_explainability", _ctx(),
        decision="REJECT", reason_codes=["SCORE_BELOW_MINIMUM"], language="hi",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert len(r.data["borrower_facing_reasons"]) == 1
