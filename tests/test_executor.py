import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.registry import (
    AuthorityLevel,
    ToolCategory,
    ToolRegistry,
    ToolResultStatus,
    lending_tool,
)


@pytest.fixture(autouse=True)
def clear_state():
    saved_tools = dict(ToolRegistry._tools)
    ToolRegistry.clear()
    CircuitBreakerManager.clear()

    @lending_tool(
        name="test_verify_aadhaar_otp",
        description="Verify Aadhaar via OTP",
        category=ToolCategory.IDENTITY,
    )
    async def _verify_aadhaar(**kwargs):
        return {"verified": True, "name": "Ramesh Patel"}

    @lending_tool(
        name="test_fetch_bureau",
        description="Fetch bureau report",
        category=ToolCategory.DATA,
        requires_confirmation=True,
    )
    async def _fetch_bureau(**kwargs):
        return {"score": 720, "grade": "B1"}

    @lending_tool(
        name="test_execute_disbursement",
        description="Disburse loan",
        category=ToolCategory.EXECUTION,
        authority_level=AuthorityLevel.WRITE,
        requires_confirmation=True,
    )
    async def _disburse(**kwargs):
        return {"reference_id": "REF123"}

    @lending_tool(
        name="test_slow_tool",
        description="A slow tool",
        category=ToolCategory.DATA,
        timeout_seconds=1,
    )
    async def _slow_tool(**kwargs):
        import asyncio

        await asyncio.sleep(5)
        return {"data": "never"}

    yield
    ToolRegistry.clear()
    ToolRegistry._tools = saved_tools
    CircuitBreakerManager.clear()


def _make_context(
    state: SessionState = SessionState.UNVERIFIED,
    confirmed: bool = False,
    maker_approved: bool = False,
) -> ExecutionContext:
    return ExecutionContext(
        session_id=uuid.uuid4(),
        session_state=state,
        lender_id="LENDER_001",
        borrower_confirmed=confirmed,
        maker_approved=maker_approved,
    )


@pytest.mark.asyncio
async def test_identity_tool_in_unverified():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.UNVERIFIED)
    result = await executor.execute("test_verify_aadhaar_otp", ctx)
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["verified"] is True


@pytest.mark.asyncio
async def test_data_tool_blocked_in_unverified():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.UNVERIFIED, confirmed=True)
    result = await executor.execute("test_fetch_bureau", ctx)
    assert result.status == ToolResultStatus.BLOCKED
    assert "requires session state VERIFIED" in result.error


@pytest.mark.asyncio
async def test_data_tool_allowed_in_verified():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.VERIFIED, confirmed=True)
    result = await executor.execute("test_fetch_bureau", ctx)
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["score"] == 720


@pytest.mark.asyncio
async def test_confirmation_required():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.VERIFIED, confirmed=False)
    result = await executor.execute("test_fetch_bureau", ctx)
    assert result.status == ToolResultStatus.BLOCKED
    assert "requires explicit borrower confirmation" in result.error


@pytest.mark.asyncio
async def test_execution_tool_requires_confirmed_state():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.VERIFIED, confirmed=True, maker_approved=True)
    result = await executor.execute("test_execute_disbursement", ctx)
    assert result.status == ToolResultStatus.BLOCKED
    assert "requires session state CONFIRMED" in result.error


@pytest.mark.asyncio
async def test_execution_tool_requires_maker_approval():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.CONFIRMED, confirmed=True, maker_approved=False)
    result = await executor.execute("test_execute_disbursement", ctx)
    assert result.status == ToolResultStatus.BLOCKED
    assert "maker-checker" in result.error


@pytest.mark.asyncio
async def test_execution_tool_success():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.CONFIRMED, confirmed=True, maker_approved=True)
    result = await executor.execute("test_execute_disbursement", ctx)
    assert result.status == ToolResultStatus.SUCCESS
    assert result.data["reference_id"] == "REF123"


@pytest.mark.asyncio
async def test_nonexistent_tool():
    executor = ToolExecutor()
    ctx = _make_context()
    result = await executor.execute("nonexistent_tool", ctx)
    assert result.status == ToolResultStatus.BLOCKED
    assert "not found" in result.error


@pytest.mark.asyncio
async def test_timeout():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.VERIFIED)
    result = await executor.execute("test_slow_tool", ctx)
    assert result.status == ToolResultStatus.TIMEOUT
    assert "timed out" in result.error


@pytest.mark.asyncio
async def test_circuit_breaker_trips():
    executor = ToolExecutor()

    @lending_tool(
        name="test_failing_tool",
        description="Always fails",
        category=ToolCategory.IDENTITY,
        circuit_breaker_threshold=2,
    )
    async def _failing(**kwargs):
        raise ValueError("API error")

    ctx = _make_context(SessionState.UNVERIFIED)

    r1 = await executor.execute("test_failing_tool", ctx)
    assert r1.status == ToolResultStatus.FAILURE

    r2 = await executor.execute("test_failing_tool", ctx)
    assert r2.status == ToolResultStatus.FAILURE

    r3 = await executor.execute("test_failing_tool", ctx)
    assert r3.status == ToolResultStatus.DEGRADED
    assert "Circuit breaker OPEN" in r3.error


@pytest.mark.asyncio
async def test_latency_tracking():
    executor = ToolExecutor()
    ctx = _make_context(SessionState.UNVERIFIED)
    result = await executor.execute("test_verify_aadhaar_otp", ctx)
    assert result.latency_ms >= 0
    assert result.session_state_before == "UNVERIFIED"
