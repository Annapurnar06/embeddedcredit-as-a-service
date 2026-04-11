from __future__ import annotations

import enum
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any

from app.models.session import SessionState


class ToolCategory(str, enum.Enum):
    IDENTITY = "identity"
    DATA = "data"
    SCORING = "scoring"
    PRODUCT = "product"
    EXECUTION = "execution"
    SERVICING = "servicing"
    MONITORING = "monitoring"
    COLLECTIONS = "collections"


class AuthorityLevel(str, enum.Enum):
    GENERAL = "general"
    ACCOUNT = "account"
    WRITE = "write"


class ToolResultStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
    TIMEOUT = "TIMEOUT"


CATEGORY_MIN_STATE: dict[ToolCategory, SessionState] = {
    ToolCategory.IDENTITY: SessionState.UNVERIFIED,
    ToolCategory.DATA: SessionState.VERIFIED,
    ToolCategory.SCORING: SessionState.VERIFIED,
    ToolCategory.PRODUCT: SessionState.VERIFIED,
    ToolCategory.EXECUTION: SessionState.CONFIRMED,
    ToolCategory.SERVICING: SessionState.VERIFIED,
    ToolCategory.MONITORING: SessionState.VERIFIED,
    ToolCategory.COLLECTIONS: SessionState.VERIFIED,
}

STATE_ORDER = {
    SessionState.UNVERIFIED: 0,
    SessionState.VERIFIED: 1,
    SessionState.CONFIRMED: 2,
    SessionState.EXPIRED: -1,
}


@dataclass
class ToolDefinition:
    name: str
    description: str
    category: ToolCategory
    handler: Callable[..., Coroutine[Any, Any, Any]]
    requires_confirmation: bool = False
    authority_level: AuthorityLevel = AuthorityLevel.GENERAL
    circuit_breaker_threshold: int = 5
    timeout_seconds: int = 15
    min_session_state: SessionState | None = None
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.min_session_state is None:
            self.min_session_state = CATEGORY_MIN_STATE.get(
                self.category, SessionState.VERIFIED
            )


class ToolRegistry:
    _tools: dict[str, ToolDefinition] = {}

    @classmethod
    def register(cls, tool_def: ToolDefinition) -> None:
        cls._tools[tool_def.name] = tool_def

    @classmethod
    def get(cls, name: str) -> ToolDefinition | None:
        return cls._tools.get(name)

    @classmethod
    def get_all(cls) -> dict[str, ToolDefinition]:
        return dict(cls._tools)

    @classmethod
    def get_by_category(cls, category: ToolCategory) -> list[ToolDefinition]:
        return [t for t in cls._tools.values() if t.category == category]

    @classmethod
    def get_available_for_state(cls, state: SessionState) -> list[ToolDefinition]:
        state_level = STATE_ORDER.get(state, -1)
        return [
            t
            for t in cls._tools.values()
            if STATE_ORDER.get(t.min_session_state, 99) <= state_level  # type: ignore[arg-type]
        ]

    @classmethod
    def clear(cls) -> None:
        cls._tools.clear()


def lending_tool(
    name: str,
    description: str,
    category: ToolCategory,
    requires_confirmation: bool = False,
    authority_level: AuthorityLevel = AuthorityLevel.GENERAL,
    circuit_breaker_threshold: int = 5,
    timeout_seconds: int = 15,
    min_session_state: SessionState | None = None,
    tags: list[str] | None = None,
) -> Callable:  # type: ignore[type-arg]
    def decorator(
        func: Callable[..., Coroutine[Any, Any, Any]],
    ) -> Callable[..., Coroutine[Any, Any, Any]]:
        tool_def = ToolDefinition(
            name=name,
            description=description,
            category=category,
            handler=func,
            requires_confirmation=requires_confirmation,
            authority_level=authority_level,
            circuit_breaker_threshold=circuit_breaker_threshold,
            timeout_seconds=timeout_seconds,
            min_session_state=min_session_state,
            tags=tags or [],
        )
        ToolRegistry.register(tool_def)
        func._tool_definition = tool_def  # type: ignore[attr-defined]
        return func

    return decorator
