import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.identity import *  # noqa: F401,F403
from app.tools.registry import ToolRegistry, ToolResultStatus


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(state: SessionState = SessionState.UNVERIFIED, confirmed: bool = False):
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="LENDER_001",
        borrower_confirmed=confirmed,
    )


@pytest.mark.asyncio
async def test_verify_aadhaar_otp_send():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_aadhaar_otp", _ctx(), aadhaar_number="123456789012"
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["otp_sent"] is True


@pytest.mark.asyncio
async def test_verify_aadhaar_otp_verify():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_aadhaar_otp",
        _ctx(),
        aadhaar_number="123456789012",
        otp="123456",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["verified"] is True
    assert result.data["name"] is not None
    assert result.data["address_pincode"] is not None


@pytest.mark.asyncio
async def test_verify_aadhaar_otp_invalid_number():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_aadhaar_otp", _ctx(), aadhaar_number="12345"
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["verified"] is False


@pytest.mark.asyncio
async def test_verify_aadhaar_voice_otp():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_aadhaar_voice_otp",
        _ctx(),
        aadhaar_number="123456789012",
        spoken_otp="123456",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["verified"] is True


@pytest.mark.asyncio
async def test_verify_pan():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_pan",
        _ctx(),
        pan_number="ABCDE1234F",
        aadhaar_name="Ramesh Patel",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["valid"] is True
    assert result.data["name_match_score"] > 0.85


@pytest.mark.asyncio
async def test_verify_pan_invalid():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_pan", _ctx(), pan_number="INVALID"
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["valid"] is False


@pytest.mark.asyncio
async def test_verify_bank_account():
    executor = ToolExecutor()
    result = await executor.execute(
        "verify_bank_account",
        _ctx(),
        account_number="12345678901234",
        ifsc="SBIN0001234",
        aadhaar_name="Ramesh Patel",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["account_valid"] is True
    assert result.data["bank_name"] == "STATE BANK OF INDIA"


@pytest.mark.asyncio
async def test_initiate_aa_consent():
    executor = ToolExecutor()
    result = await executor.execute(
        "initiate_aa_consent",
        _ctx(confirmed=True),
        borrower_phone="9876543210",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["consent_id"] is not None
    assert result.data["status"] == "PENDING"


@pytest.mark.asyncio
async def test_aa_consent_requires_confirmation():
    executor = ToolExecutor()
    result = await executor.execute(
        "initiate_aa_consent",
        _ctx(confirmed=False),
        borrower_phone="9876543210",
    )
    assert result.status == ToolResultStatus.BLOCKED
    assert "confirmation" in result.error


@pytest.mark.asyncio
async def test_check_negative_list():
    executor = ToolExecutor()
    result = await executor.execute(
        "check_negative_list",
        _ctx(),
        aadhaar_hash="abc123def456",
    )
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["clear"] is True
    assert len(result.data["sources_checked"]) == 4


@pytest.mark.asyncio
async def test_identity_tools_blocked_in_expired():
    executor = ToolExecutor()
    ctx = _ctx(state=SessionState.EXPIRED)
    result = await executor.execute("verify_aadhaar_otp", ctx, aadhaar_number="123456789012")
    assert result.status == ToolResultStatus.BLOCKED


@pytest.mark.asyncio
async def test_all_6_identity_tools_registered():
    identity_names = {
        "verify_aadhaar_otp",
        "verify_aadhaar_voice_otp",
        "verify_pan",
        "verify_bank_account",
        "initiate_aa_consent",
        "check_negative_list",
    }
    for name in identity_names:
        tool = ToolRegistry.get(name)
        assert tool is not None, f"Tool '{name}' not registered"
        assert tool.category.value == "identity"
