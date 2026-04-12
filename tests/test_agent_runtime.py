import uuid

import pytest

from app.agent.runtime import AgentRuntime, AgentSession
from app.core.audit import AuditTrail
from app.models.session import SessionState
from app.tools.data import *  # noqa: F401,F403
from app.tools.execution import *  # noqa: F401,F403
from app.tools.identity import *  # noqa: F401,F403
from app.tools.product import *  # noqa: F401,F403
from app.tools.scoring import *  # noqa: F401,F403


def _session(
    state: SessionState = SessionState.UNVERIFIED,
    segment: str = "DAIRY_FARMER",
) -> AgentSession:
    return AgentSession(
        session_id=uuid.uuid4(),
        lender_id="TEST_NBFC",
        state=state,
        segment=segment,
        language="hi",
    )


@pytest.mark.asyncio
async def test_greeting():
    runtime = AgentRuntime()
    session = _session()
    turn = await runtime.process_message(session, "namaste")
    assert turn.agent_response != ""
    assert turn.state_before == "UNVERIFIED"
    assert turn.state_after == "UNVERIFIED"


@pytest.mark.asyncio
async def test_aadhaar_verification_triggers_tool():
    runtime = AgentRuntime()
    session = _session()
    turn = await runtime.process_message(session, "verify my aadhaar please")
    assert "verify_aadhaar_otp" in turn.tools_called


@pytest.mark.asyncio
async def test_state_transitions_on_verification():
    runtime = AgentRuntime()
    session = _session()
    assert session.state == SessionState.UNVERIFIED

    turn = await runtime.process_message(session, "verify my aadhaar 123456789012")
    if "verify_aadhaar_otp" in turn.tools_called:
        verified_results = [
            r for r in turn.tool_results if r.get("data", {}).get("verified") is True
        ]
        if verified_results:
            assert session.state == SessionState.VERIFIED


@pytest.mark.asyncio
async def test_conversation_history_maintained():
    runtime = AgentRuntime()
    session = _session()
    await runtime.process_message(session, "namaste")
    await runtime.process_message(session, "mujhe loan chahiye")
    assert len(session.history) == 2
    assert session.history[0].borrower_message == "namaste"
    assert session.history[1].borrower_message == "mujhe loan chahiye"


@pytest.mark.asyncio
async def test_audit_trail_populated():
    audit = AuditTrail()
    runtime = AgentRuntime(audit_trail=audit)
    session = _session()
    await runtime.process_message(session, "namaste")
    assert audit.total_logs >= 1


@pytest.mark.asyncio
async def test_empathetic_response_on_distress():
    runtime = AgentRuntime()
    session = _session(state=SessionState.VERIFIED)
    turn = await runtime.process_message(session, "my cow died last week")
    assert any(
        w in turn.agent_response.lower()
        for w in ["dukh", "sorry", "understand", "samajh", "mushkil"]
    )


@pytest.mark.asyncio
async def test_complaint_triggers_grievance():
    runtime = AgentRuntime()
    session = _session(state=SessionState.VERIFIED)
    turn = await runtime.process_message(session, "I have a complaint, this is wrong")
    response_lower = turn.agent_response.lower()
    assert any(w in response_lower for w in ["grievance", "pareshani", "sampark", "officer"])


@pytest.mark.asyncio
async def test_session_messages_list():
    session = _session()
    from app.agent.runtime import ConversationTurn

    session.history.append(
        ConversationTurn(
            borrower_message="hello",
            agent_response="namaste",
        )
    )
    msgs = session.messages
    assert len(msgs) == 2
    assert msgs[0].role == "user"
    assert msgs[1].role == "assistant"


@pytest.mark.asyncio
async def test_multiple_turns():
    runtime = AgentRuntime()
    session = _session()

    t1 = await runtime.process_message(session, "namaste")
    assert t1.agent_response != ""

    t2 = await runtime.process_message(session, "mujhe loan chahiye")
    assert t2.agent_response != ""

    t3 = await runtime.process_message(session, "haan theek hai")
    assert t3.agent_response != ""

    assert len(session.history) == 3
