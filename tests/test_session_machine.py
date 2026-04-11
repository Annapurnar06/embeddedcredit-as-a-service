import pytest

from app.models.session import SessionState
from app.tools.session_machine import SessionMachine, SessionStateError


def test_valid_transitions():
    assert SessionMachine.can_transition(SessionState.UNVERIFIED, SessionState.VERIFIED)
    assert SessionMachine.can_transition(SessionState.VERIFIED, SessionState.CONFIRMED)
    assert SessionMachine.can_transition(SessionState.UNVERIFIED, SessionState.EXPIRED)
    assert SessionMachine.can_transition(SessionState.VERIFIED, SessionState.EXPIRED)
    assert SessionMachine.can_transition(SessionState.CONFIRMED, SessionState.EXPIRED)


def test_invalid_transitions():
    assert not SessionMachine.can_transition(SessionState.UNVERIFIED, SessionState.CONFIRMED)
    assert not SessionMachine.can_transition(SessionState.VERIFIED, SessionState.UNVERIFIED)
    assert not SessionMachine.can_transition(SessionState.CONFIRMED, SessionState.VERIFIED)
    assert not SessionMachine.can_transition(SessionState.EXPIRED, SessionState.UNVERIFIED)


def test_transition_executes():
    result = SessionMachine.transition(SessionState.UNVERIFIED, SessionState.VERIFIED)
    assert result == SessionState.VERIFIED


def test_invalid_transition_raises():
    with pytest.raises(SessionStateError, match="Invalid transition"):
        SessionMachine.transition(SessionState.UNVERIFIED, SessionState.CONFIRMED)


def test_meets_minimum():
    assert SessionMachine.meets_minimum(SessionState.VERIFIED, SessionState.UNVERIFIED)
    assert SessionMachine.meets_minimum(SessionState.VERIFIED, SessionState.VERIFIED)
    assert not SessionMachine.meets_minimum(SessionState.VERIFIED, SessionState.CONFIRMED)
    assert SessionMachine.meets_minimum(SessionState.CONFIRMED, SessionState.UNVERIFIED)
    assert SessionMachine.meets_minimum(SessionState.CONFIRMED, SessionState.CONFIRMED)
    assert not SessionMachine.meets_minimum(SessionState.UNVERIFIED, SessionState.VERIFIED)
