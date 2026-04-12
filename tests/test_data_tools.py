import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.data import *  # noqa: F401,F403
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.registry import ToolRegistry, ToolResultStatus


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


@pytest.mark.asyncio
async def test_all_12_data_tools_registered():
    names = {
        "fetch_uli_parallel",
        "fetch_aa_bank_data",
        "pull_credit_bureau",
        "analyze_bank_statement",
        "extract_document",
        "fetch_cooperative_data",
        "fetch_platform_earnings",
        "fetch_gst_returns",
        "compute_device_score",
        "cross_validate_sources",
        "compute_confidence_score",
        "compute_borrower_profile",
    }
    for name in names:
        tool = ToolRegistry.get(name)
        assert tool is not None, f"Tool '{name}' not registered"
        assert tool.category.value == "data"


@pytest.mark.asyncio
async def test_data_tools_blocked_in_unverified():
    executor = ToolExecutor()
    ctx = _ctx(state=SessionState.UNVERIFIED)
    result = await executor.execute("fetch_uli_parallel", ctx)
    assert result.status == ToolResultStatus.BLOCKED


@pytest.mark.asyncio
async def test_uli_fetch():
    executor = ToolExecutor()
    result = await executor.execute("fetch_uli_parallel", _ctx(), pincode="385001")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["land_records"] is not None
    assert result.data["weather_imd"]["district"] == "Banaskantha"


@pytest.mark.asyncio
async def test_aa_bank_data():
    executor = ToolExecutor()
    result = await executor.execute("fetch_aa_bank_data", _ctx(), consent_id="consent-123")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["bank_name"] == "STATE BANK OF INDIA"
    assert result.data["months_available"] == 12


@pytest.mark.asyncio
async def test_bureau_requires_confirmation():
    executor = ToolExecutor()
    result = await executor.execute("pull_credit_bureau", _ctx(confirmed=False), aadhaar_hash="abc")
    assert result.status == ToolResultStatus.BLOCKED


@pytest.mark.asyncio
async def test_bureau_with_confirmation():
    executor = ToolExecutor()
    result = await executor.execute("pull_credit_bureau", _ctx(confirmed=True), aadhaar_hash="abc")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["score"] == 720
    assert result.data["bureau"] == "CIBIL"


@pytest.mark.asyncio
async def test_bank_statement():
    executor = ToolExecutor()
    result = await executor.execute("analyze_bank_statement", _ctx())
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["months_analyzed"] == 6
    assert result.data["foir"] == 0.28


@pytest.mark.asyncio
async def test_extract_document():
    executor = ToolExecutor()
    result = await executor.execute("extract_document", _ctx(), document_type="ITR")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["document_type"] == "ITR"
    assert result.data["fields_extracted"] == 8


@pytest.mark.asyncio
async def test_cooperative_data():
    executor = ToolExecutor()
    result = await executor.execute("fetch_cooperative_data", _ctx(), membership_id="BD-2020-12345")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["membership_tenure_months"] == 48
    assert result.data["pouring_regularity_pct"] == 92.0


@pytest.mark.asyncio
async def test_platform_earnings():
    executor = ToolExecutor()
    result = await executor.execute(
        "fetch_platform_earnings",
        _ctx(),
        platform="swiggy",
        platform_user_id="USR123",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["platform"] == "swiggy"
    assert result.data["active_months"] == 18


@pytest.mark.asyncio
async def test_gst_returns():
    executor = ToolExecutor()
    result = await executor.execute("fetch_gst_returns", _ctx(), gstin="24AAAAA0000A1Z5")
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["filing_regularity_pct"] == 91.7


@pytest.mark.asyncio
async def test_device_score():
    executor = ToolExecutor()
    result = await executor.execute("compute_device_score", _ctx(), device_fingerprint="fp123")
    assert result.status == ToolResultStatus.SUCCESS
    assert 0 <= result.data["score"] <= 1000


@pytest.mark.asyncio
async def test_cross_validate_consistent():
    executor = ToolExecutor()
    result = await executor.execute(
        "cross_validate_sources",
        _ctx(),
        bank_income=45000,
        cooperative_income=42000,
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["consistent"] is True


@pytest.mark.asyncio
async def test_cross_validate_inconsistent():
    executor = ToolExecutor()
    result = await executor.execute(
        "cross_validate_sources",
        _ctx(),
        bank_income=45000,
        cooperative_income=15000,
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["consistent"] is False
    assert len(result.data["anomalies"]) > 0


@pytest.mark.asyncio
async def test_confidence_score_high():
    executor = ToolExecutor()
    result = await executor.execute(
        "compute_confidence_score",
        _ctx(),
        sources_available=5,
        sources_required=3,
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["level"] == "HIGH"
    assert result.data["score"] >= 0.8


@pytest.mark.asyncio
async def test_confidence_score_low():
    executor = ToolExecutor()
    result = await executor.execute(
        "compute_confidence_score",
        _ctx(),
        sources_available=1,
        sources_required=3,
        anomaly_free=False,
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["level"] in ("LOW", "MEDIUM")


@pytest.mark.asyncio
async def test_borrower_profile():
    executor = ToolExecutor()
    bid = str(uuid.uuid4())
    result = await executor.execute(
        "compute_borrower_profile",
        _ctx(),
        borrower_id=bid,
        segment="DAIRY_FARMER",
        aadhaar_verified=True,
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["aadhaar_verified"] is True
    assert result.data["segment"] == "DAIRY_FARMER"
