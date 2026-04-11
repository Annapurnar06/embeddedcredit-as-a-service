from __future__ import annotations

import asyncio
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from app.core.logging import get_logger
from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.registry import (
    AuthorityLevel,
    ToolDefinition,
    ToolRegistry,
    ToolResultStatus,
)
from app.tools.session_machine import SessionMachine

logger = get_logger(__name__)

PII_PATTERNS = [
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"), "XXXX-XXXX-XXXX"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "XXXXX0000X"),
    (re.compile(r"\b\d{10,12}\b"), "XXXXXXXXXX"),
]


def mask_pii(data: str) -> str:
    result = data
    for pattern, replacement in PII_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


@dataclass
class ToolResult:
    tool_name: str
    status: ToolResultStatus
    data: Any = None
    error: str | None = None
    latency_ms: int = 0
    session_state_before: str = ""
    session_state_after: str = ""
    policy_checks: list[dict[str, Any]] = field(default_factory=list)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ExecutionContext:
    session_id: uuid.UUID
    session_state: SessionState
    lender_id: str
    loan_application_id: uuid.UUID | None = None
    borrower_confirmed: bool = False
    maker_approved: bool = False
    kfs_generated: bool = False
    bureau_pulls_48h: int = 0


class ToolExecutor:
    async def execute(
        self,
        tool_name: str,
        context: ExecutionContext,
        **kwargs: Any,
    ) -> ToolResult:
        start_time = time.monotonic()
        state_before = context.session_state.value

        tool_def = ToolRegistry.get(tool_name)
        if tool_def is None:
            return ToolResult(
                tool_name=tool_name,
                status=ToolResultStatus.BLOCKED,
                error=f"Tool '{tool_name}' not found in registry",
                session_state_before=state_before,
                session_state_after=state_before,
            )

        # Step 1: Session state check
        state_check = self._check_session_state(tool_def, context)
        if state_check is not None:
            return self._finalize(
                tool_name, state_check, start_time, state_before, state_before
            )

        # Step 2: Confirmation check
        confirm_check = self._check_confirmation(tool_def, context)
        if confirm_check is not None:
            return self._finalize(
                tool_name, confirm_check, start_time, state_before, state_before
            )

        # Step 3: Authority boundary checks
        authority_check = self._check_authority(tool_def, context)
        if authority_check is not None:
            return self._finalize(
                tool_name, authority_check, start_time, state_before, state_before
            )

        # Step 4: Circuit breaker check
        cb = CircuitBreakerManager.get_or_create(
            tool_name, tool_def.circuit_breaker_threshold
        )
        if cb.is_open():
            return self._finalize(
                tool_name,
                ToolResult(
                    tool_name=tool_name,
                    status=ToolResultStatus.DEGRADED,
                    error=f"Circuit breaker OPEN for {tool_name}",
                    policy_checks=[
                        {"check": "circuit_breaker", "result": "OPEN"}
                    ],
                ),
                start_time,
                state_before,
                state_before,
            )

        # Step 5: Execute the tool
        try:
            result_data = await asyncio.wait_for(
                tool_def.handler(**kwargs),
                timeout=tool_def.timeout_seconds,
            )
            cb.record_success()
            state_after = context.session_state.value
            return self._finalize(
                tool_name,
                ToolResult(
                    tool_name=tool_name,
                    status=ToolResultStatus.SUCCESS,
                    data=result_data,
                ),
                start_time,
                state_before,
                state_after,
            )
        except asyncio.TimeoutError:
            cb.record_failure()
            return self._finalize(
                tool_name,
                ToolResult(
                    tool_name=tool_name,
                    status=ToolResultStatus.TIMEOUT,
                    error=f"Tool timed out after {tool_def.timeout_seconds}s",
                ),
                start_time,
                state_before,
                state_before,
            )
        except Exception as e:
            cb.record_failure()
            return self._finalize(
                tool_name,
                ToolResult(
                    tool_name=tool_name,
                    status=ToolResultStatus.FAILURE,
                    error=str(e),
                ),
                start_time,
                state_before,
                state_before,
            )

    def _check_session_state(
        self, tool_def: ToolDefinition, context: ExecutionContext
    ) -> ToolResult | None:
        min_state = tool_def.min_session_state
        if min_state is None:
            return None
        if not SessionMachine.meets_minimum(context.session_state, min_state):
            return ToolResult(
                tool_name=tool_def.name,
                status=ToolResultStatus.BLOCKED,
                error=(
                    f"Tool '{tool_def.name}' requires session state "
                    f"{min_state.value} or above, current: {context.session_state.value}"
                ),
                policy_checks=[
                    {
                        "check": "session_state",
                        "required": min_state.value,
                        "current": context.session_state.value,
                        "result": "BLOCKED",
                    }
                ],
            )
        return None

    def _check_confirmation(
        self, tool_def: ToolDefinition, context: ExecutionContext
    ) -> ToolResult | None:
        if tool_def.requires_confirmation and not context.borrower_confirmed:
            return ToolResult(
                tool_name=tool_def.name,
                status=ToolResultStatus.BLOCKED,
                error=(
                    f"Tool '{tool_def.name}' requires explicit borrower confirmation"
                ),
                policy_checks=[
                    {"check": "confirmation", "result": "BLOCKED"}
                ],
            )
        return None

    def _check_authority(
        self, tool_def: ToolDefinition, context: ExecutionContext
    ) -> ToolResult | None:
        checks: list[dict[str, Any]] = []

        if (
            tool_def.authority_level == AuthorityLevel.WRITE
            and not context.maker_approved
        ):
            from app.core.config import settings

            if not settings.can_disburse_without_human:
                    checks.append(
                        {"check": "maker_checker", "result": "BLOCKED"}
                    )
                    return ToolResult(
                        tool_name=tool_def.name,
                        status=ToolResultStatus.BLOCKED,
                        error=(
                            f"Tool '{tool_def.name}' requires maker-checker "
                            f"approval (authority_level=write)"
                        ),
                        policy_checks=checks,
                    )
        return None

    def _finalize(
        self,
        tool_name: str,
        result: ToolResult,
        start_time: float,
        state_before: str,
        state_after: str,
    ) -> ToolResult:
        result.latency_ms = int((time.monotonic() - start_time) * 1000)
        result.session_state_before = state_before
        result.session_state_after = state_after
        return result
