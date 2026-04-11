"""Session manager -- maps channel user IDs to agent sessions."""
from __future__ import annotations

import uuid

from app.agent.runtime import AgentSession
from app.models.session import SessionState


class SessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, AgentSession] = {}

    def _key(self, channel: str, channel_user_id: str, lender_id: str) -> str:
        return f"{channel}:{channel_user_id}:{lender_id}"

    def get_or_create(
        self,
        channel: str,
        channel_user_id: str,
        lender_id: str,
        segment: str | None = None,
        language: str = "hi",
    ) -> AgentSession:
        key = self._key(channel, channel_user_id, lender_id)
        if key not in self._sessions:
            self._sessions[key] = AgentSession(
                session_id=uuid.uuid4(),
                lender_id=lender_id,
                state=SessionState.UNVERIFIED,
                segment=segment,
                language=language,
            )
        return self._sessions[key]

    def get(
        self, channel: str, channel_user_id: str, lender_id: str
    ) -> AgentSession | None:
        return self._sessions.get(self._key(channel, channel_user_id, lender_id))

    def remove(self, channel: str, channel_user_id: str, lender_id: str) -> None:
        key = self._key(channel, channel_user_id, lender_id)
        self._sessions.pop(key, None)

    @property
    def active_count(self) -> int:
        return len(self._sessions)
