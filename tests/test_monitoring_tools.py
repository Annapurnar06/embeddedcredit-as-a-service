import uuid

import pytest

from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.monitoring import *  # noqa: F401,F403
from app.tools.registry import ToolRegistry, ToolResultStatus


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
async def test_all_5_monitoring_tools_registered():
    names = {
        "poll_monitoring_signals", "evaluate_monitoring_triggers",
        "execute_auto_intervention", "evaluate_graduation",
        "schedule_monitoring_job",
    }
    for name in names:
        assert ToolRegistry.get(name) is not None


@pytest.mark.asyncio
async def test_poll_signals():
    ex = ToolExecutor()
    r = await ex.execute("poll_monitoring_signals", _ctx())
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["signals_polled"] == 5
    assert len(r.data["signals"]) == 5


@pytest.mark.asyncio
async def test_evaluate_triggers_none():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_monitoring_triggers", _ctx(),
        segment="DAIRY_FARMER", signals=[],
    )
    assert r.data["recommended_action"] == "NONE"


@pytest.mark.asyncio
async def test_evaluate_triggers_breach():
    ex = ToolExecutor()
    signals = [
        {"signal_type": "bank_txn_drop", "value": 0.9},
        {"signal_type": "cooperative_pouring_drop", "value": 0.8},
        {"signal_type": "dpd_change", "value": 0.95},
    ]
    r = await ex.execute(
        "evaluate_monitoring_triggers", _ctx(),
        segment="DAIRY_FARMER", signals=signals,
    )
    assert r.data["recommended_action"] == "ESCALATE"
    assert len(r.data["triggered"]) == 3


@pytest.mark.asyncio
async def test_evaluate_triggers_single():
    ex = ToolExecutor()
    signals = [{"signal_type": "bank_txn_drop", "value": 0.5}]
    r = await ex.execute(
        "evaluate_monitoring_triggers", _ctx(),
        segment="DAIRY_FARMER", signals=signals,
    )
    assert r.data["recommended_action"] == "WATCH"


@pytest.mark.asyncio
async def test_auto_intervention_nudge():
    ex = ToolExecutor()
    r = await ex.execute(
        "execute_auto_intervention", _ctx(confirmed=True, maker=True),
        intervention_type="nudge", reason="missed payment",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["action"] == "SEND_NUDGE"
    assert r.data["status"] == "EXECUTED"


@pytest.mark.asyncio
async def test_auto_intervention_moratorium():
    ex = ToolExecutor()
    r = await ex.execute(
        "execute_auto_intervention", _ctx(confirmed=True, maker=True),
        intervention_type="moratorium", reason="flood",
    )
    assert r.data["action"] == "AUTO_MORATORIUM"
    assert r.data["status"] == "PENDING_REVIEW"


@pytest.mark.asyncio
async def test_graduation_eligible():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_graduation", _ctx(),
        months_on_book=12, on_time_rate=0.97,
        current_rate=15.0, current_limit=100000,
    )
    assert r.data["eligible"] is True
    assert r.data["offer_count"] >= 2


@pytest.mark.asyncio
async def test_graduation_not_eligible():
    ex = ToolExecutor()
    r = await ex.execute(
        "evaluate_graduation", _ctx(),
        months_on_book=3, on_time_rate=0.7,
    )
    assert r.data["eligible"] is False
    assert r.data["offer_count"] == 0


@pytest.mark.asyncio
async def test_schedule_job():
    ex = ToolExecutor()
    r = await ex.execute(
        "schedule_monitoring_job", _ctx(confirmed=True, maker=True),
        segment="KIRANA_SHOP",
    )
    assert r.status == ToolResultStatus.SUCCESS
    assert r.data["frequency"] == "daily"
    assert r.data["status"] == "SCHEDULED"


@pytest.mark.asyncio
async def test_schedule_job_override_frequency():
    ex = ToolExecutor()
    r = await ex.execute(
        "schedule_monitoring_job", _ctx(confirmed=True, maker=True),
        segment="DAIRY_FARMER", override_frequency="daily",
    )
    assert r.data["frequency"] == "daily"
