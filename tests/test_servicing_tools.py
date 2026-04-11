import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.registry import ToolRegistry, ToolResultStatus
from app.tools.servicing import *  # noqa: F401,F403


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


def _ctx(state=SessionState.VERIFIED, confirmed=False, maker=False):
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="L1",
        borrower_confirmed=confirmed,
        maker_approved=maker,
    )


@pytest.mark.asyncio
async def test_all_6_servicing_tools_registered():
    names = {
        "get_loan_status", "get_repayment_schedule", "process_prepayment",
        "apply_moratorium", "generate_statement", "generate_noc",
    }
    for name in names:
        assert ToolRegistry.get(name) is not None


@pytest.mark.asyncio
async def test_loan_status():
    ex = ToolExecutor()
    r = await ex.execute("get_loan_status", _ctx(), loan_id="LOAN-001")
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "ACTIVE"
    assert r.data["dpd"] == 0


@pytest.mark.asyncio
async def test_repayment_schedule():
    ex = ToolExecutor()
    r = await ex.execute("get_repayment_schedule", _ctx())
    assert r.status == ToolResultStatus.SUCCESS
    assert len(r.data["entries"]) == 18
    assert r.data["completed_months"] == 4


@pytest.mark.asyncio
async def test_prepayment_reduce_tenure():
    ex = ToolExecutor()
    r = await ex.execute(
        "process_prepayment", _ctx(confirmed=True, maker=True),
        amount=10000, mode="reduce_tenure",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["months_saved"] == 2


@pytest.mark.asyncio
async def test_prepayment_reduce_emi():
    ex = ToolExecutor()
    r = await ex.execute(
        "process_prepayment", _ctx(confirmed=True, maker=True),
        amount=10000, mode="reduce_emi",
    )
    assert r.data["new_emi"] is not None


@pytest.mark.asyncio
async def test_prepayment_blocked_without_confirmation():
    ex = ToolExecutor()
    r = await ex.execute(
        "process_prepayment", _ctx(confirmed=False),
        amount=10000,
    )
    assert r.status == ToolResultStatus.BLOCKED


@pytest.mark.asyncio
async def test_moratorium():
    ex = ToolExecutor()
    r = await ex.execute(
        "apply_moratorium", _ctx(confirmed=True, maker=True),
        months=2, reason="flood",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["moratorium_months"] == 2
    assert r.data["no_late_fees"] is True


@pytest.mark.asyncio
async def test_statement():
    ex = ToolExecutor()
    r = await ex.execute("generate_statement", _ctx())
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["generated"] is True


@pytest.mark.asyncio
async def test_noc():
    ex = ToolExecutor()
    r = await ex.execute("generate_noc", _ctx())
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["status"] == "GENERATED"
