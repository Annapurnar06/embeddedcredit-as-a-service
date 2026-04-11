import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.execution import *  # noqa: F401,F403
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.registry import ToolRegistry, ToolResultStatus


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(state=SessionState.CONFIRMED, confirmed=True, maker=True, kfs=False):
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="L1",
        borrower_confirmed=confirmed,
        maker_approved=maker,
        kfs_generated=kfs,
    )


@pytest.mark.asyncio
async def test_all_6_execution_tools_registered():
    names = {
        "generate_kfs", "initiate_esign", "enroll_insurance",
        "setup_enach_mandate", "execute_disbursement", "register_cersai",
    }
    for name in names:
        assert ToolRegistry.get(name) is not None


@pytest.mark.asyncio
async def test_execution_blocked_in_verified():
    ex = ToolExecutor()
    ctx = _ctx(state=SessionState.VERIFIED)
    r = await ex.execute("initiate_esign", ctx)
    assert r.status == ToolResultStatus.BLOCKED
    assert "CONFIRMED" in r.error


@pytest.mark.asyncio
async def test_execution_blocked_without_confirmation():
    ex = ToolExecutor()
    ctx = _ctx(confirmed=False)
    r = await ex.execute("initiate_esign", ctx)
    assert r.status == ToolResultStatus.BLOCKED


@pytest.mark.asyncio
async def test_execution_blocked_without_maker():
    ex = ToolExecutor()
    ctx = _ctx(maker=False)
    r = await ex.execute("execute_disbursement", ctx)
    assert r.status == ToolResultStatus.BLOCKED
    assert "maker-checker" in r.error


@pytest.mark.asyncio
async def test_generate_kfs():
    ex = ToolExecutor()
    ctx = ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=SessionState.CONFIRMED,
        lender_id="L1",
    )
    r = await ex.execute(
        "generate_kfs", ctx,
        borrower_name="Ramesh", lender_name="Test NBFC",
        amount=100000, rate=15.0, tenure_months=18,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["cooling_off_period_days"] == 3


@pytest.mark.asyncio
async def test_esign():
    ex = ToolExecutor()
    r = await ex.execute("initiate_esign", _ctx())
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "OTP_SENT"


@pytest.mark.asyncio
async def test_insurance():
    ex = ToolExecutor()
    r = await ex.execute(
        "enroll_insurance", _ctx(),
        insurance_type="PASHU_BIMA", sum_insured=80000,
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "ENROLLED"


@pytest.mark.asyncio
async def test_enach():
    ex = ToolExecutor()
    r = await ex.execute(
        "setup_enach_mandate", _ctx(),
        max_amount=10000, frequency="monthly",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["mode"] == "eNACH"


@pytest.mark.asyncio
async def test_disbursement():
    ex = ToolExecutor()
    r = await ex.execute(
        "execute_disbursement", _ctx(),
        amount=100000, mode="UPI", beneficiary_account="12345678901234",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "SUCCESS"
    assert r.data["reference_id"].startswith("DISB-")


@pytest.mark.asyncio
async def test_cersai():
    ex = ToolExecutor()
    ctx = ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=SessionState.CONFIRMED,
        lender_id="L1",
    )
    r = await ex.execute(
        "register_cersai", ctx,
        asset_type="VEHICLE", asset_description="Tractor",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "REGISTERED"


@pytest.mark.asyncio
async def test_full_execution_flow():
    """End-to-end: KFS -> eSign -> insurance -> eNACH -> disburse."""
    ex = ToolExecutor()
    ctx = _ctx()

    kfs = await ex.execute(
        "generate_kfs", ctx,
        borrower_name="Ramesh", amount=100000, rate=15.0, tenure_months=18,
    )
    assert kfs.status == ToolResultStatus.SUCCESS

    esign = await ex.execute("initiate_esign", ctx)
    assert esign.status == ToolResultStatus.SUCCESS

    ins = await ex.execute(
        "enroll_insurance", ctx, insurance_type="PASHU_BIMA", sum_insured=80000,
    )
    assert ins.status == ToolResultStatus.SUCCESS

    mandate = await ex.execute(
        "setup_enach_mandate", ctx, max_amount=10000,
    )
    assert mandate.status == ToolResultStatus.SUCCESS

    disb = await ex.execute(
        "execute_disbursement", ctx, amount=100000, mode="UPI",
    )
    assert disb.status == ToolResultStatus.SUCCESS
