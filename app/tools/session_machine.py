from __future__ import annotations

from app.models.session import SessionState
from app.tools.registry import STATE_ORDER


class SessionStateError(Exception):
    pass


class SessionMachine:
    """Enforces session state transitions. State can only advance forward."""

    VALID_TRANSITIONS: dict[SessionState, list[SessionState]] = {
        SessionState.UNVERIFIED: [SessionState.VERIFIED, SessionState.EXPIRED],
        SessionState.VERIFIED: [SessionState.CONFIRMED, SessionState.EXPIRED],
        SessionState.CONFIRMED: [SessionState.EXPIRED],
        SessionState.EXPIRED: [],
    }

    @classmethod
    def can_transition(cls, current: SessionState, target: SessionState) -> bool:
        return target in cls.VALID_TRANSITIONS.get(current, [])

    @classmethod
    def transition(cls, current: SessionState, target: SessionState) -> SessionState:
        if not cls.can_transition(current, target):
            raise SessionStateError(
                f"Invalid transition: {current.value} -> {target.value}. "
                f"Valid targets: {[s.value for s in cls.VALID_TRANSITIONS.get(current, [])]}"
            )
        return target

    @classmethod
    def meets_minimum(cls, current: SessionState, minimum: SessionState) -> bool:
        return STATE_ORDER.get(current, -1) >= STATE_ORDER.get(minimum, 99)
