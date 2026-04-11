"""Audit trail and trace system -- append-only logging for RBI compliance."""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)

PII_PATTERNS = [
    (re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"), "XXXX-XXXX-XXXX"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"), "XXXXX0000X"),
    (re.compile(r"\b\d{10,12}\b"), "XXXXXXXXXX"),
]


def mask_pii(text: str) -> str:
    result = text
    for pattern, replacement in PII_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def mask_dict(data: dict[str, Any]) -> dict[str, Any]:
    masked = {}
    sensitive_keys = {"aadhaar", "pan", "account_number", "phone", "otp"}
    fully_masked_keys = {"otp", "password", "secret", "token"}
    for key, value in data.items():
        key_lower = key.lower()
        if any(sk in key_lower for sk in fully_masked_keys):
            masked[key] = "***MASKED***"
        elif any(sk in key_lower for sk in sensitive_keys):
            if isinstance(value, str):
                masked[key] = mask_pii(value)
            else:
                masked[key] = "***MASKED***"
        elif isinstance(value, dict):
            masked[key] = mask_dict(value)
        elif isinstance(value, str):
            masked[key] = mask_pii(value)
        else:
            masked[key] = value
    return masked


class AuditTrail:
    """In-memory audit trail for use without DB. Production uses AuditLog table."""

    def __init__(self) -> None:
        self._logs: list[dict[str, Any]] = []
        self._tool_traces: list[dict[str, Any]] = []

    def log_event(
        self,
        session_id: uuid.UUID,
        event_type: str,
        event_data: dict[str, Any],
        actor: str = "agent",
        lender_id: str = "",
        loan_application_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        entry = {
            "id": str(uuid.uuid4()),
            "session_id": str(session_id),
            "loan_application_id": str(loan_application_id) if loan_application_id else None,
            "lender_id": lender_id,
            "event_type": event_type,
            "event_data": mask_dict(event_data),
            "actor": actor,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._logs.append(entry)
        return entry

    def log_tool_execution(
        self,
        session_id: uuid.UUID,
        tool_name: str,
        tool_category: str,
        input_data: dict[str, Any],
        output_data: Any,
        result_status: str,
        session_state_before: str,
        session_state_after: str,
        latency_ms: int,
        policy_checks: list[dict[str, Any]] | None = None,
        error_message: str | None = None,
        lender_id: str = "",
        loan_application_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        entry = {
            "id": str(uuid.uuid4()),
            "session_id": str(session_id),
            "loan_application_id": str(loan_application_id) if loan_application_id else None,
            "lender_id": lender_id,
            "tool_name": tool_name,
            "tool_category": tool_category,
            "input_masked": mask_dict(input_data),
            "output": output_data if result_status == "SUCCESS" else None,
            "result_status": result_status,
            "session_state_before": session_state_before,
            "session_state_after": session_state_after,
            "latency_ms": latency_ms,
            "policy_checks": policy_checks or [],
            "error_message": error_message,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._tool_traces.append(entry)
        return entry

    def log_state_transition(
        self,
        session_id: uuid.UUID,
        from_state: str,
        to_state: str,
        trigger: str,
        lender_id: str = "",
    ) -> dict[str, Any]:
        return self.log_event(
            session_id=session_id,
            event_type="SESSION_STATE_TRANSITION",
            event_data={
                "from_state": from_state,
                "to_state": to_state,
                "trigger": trigger,
            },
            actor="system",
            lender_id=lender_id,
        )

    def get_session_logs(self, session_id: uuid.UUID) -> list[dict[str, Any]]:
        sid = str(session_id)
        return [log for log in self._logs if log["session_id"] == sid]

    def get_session_tools(self, session_id: uuid.UUID) -> list[dict[str, Any]]:
        sid = str(session_id)
        return [t for t in self._tool_traces if t["session_id"] == sid]

    def get_loan_trail(self, loan_id: uuid.UUID) -> list[dict[str, Any]]:
        lid = str(loan_id)
        logs = [entry for entry in self._logs if entry["loan_application_id"] == lid]
        tools = [t for t in self._tool_traces if t["loan_application_id"] == lid]
        combined = logs + tools
        return sorted(combined, key=lambda x: x["created_at"])

    def get_full_trail(self, session_id: uuid.UUID) -> list[dict[str, Any]]:
        logs = self.get_session_logs(session_id)
        tools = self.get_session_tools(session_id)
        combined = [
            {**log, "_type": "audit_log"} for log in logs
        ] + [
            {**tool, "_type": "tool_execution"} for tool in tools
        ]
        return sorted(combined, key=lambda x: x["created_at"])

    @property
    def total_logs(self) -> int:
        return len(self._logs)

    @property
    def total_tool_traces(self) -> int:
        return len(self._tool_traces)


class EventEmitter:
    """In-memory event emitter (Redis Streams replacement for testing)."""

    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []

    def emit(self, topic: str, data: dict[str, Any]) -> None:
        self._events.append({
            "topic": topic,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def get_events(self, topic: str | None = None) -> list[dict[str, Any]]:
        if topic:
            return [e for e in self._events if e["topic"] == topic]
        return list(self._events)

    @property
    def total_events(self) -> int:
        return len(self._events)
