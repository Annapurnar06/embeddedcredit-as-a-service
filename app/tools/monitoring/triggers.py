"""Evaluate monitoring triggers against segment-specific thresholds."""

from __future__ import annotations

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

SEGMENT_THRESHOLDS: dict[str, dict[str, float]] = {
    "DAIRY_FARMER": {
        "bank_txn_drop": 0.3,
        "cooperative_pouring_drop": 0.25,
        "dpd_change": 0.5,
    },
    "KIRANA_SHOP": {
        "bank_txn_drop": 0.35,
        "inflow_drop": 0.30,
        "dpd_change": 0.5,
    },
    "GIG_WORKER": {
        "platform_deactivation": 0.1,
        "payout_drop": 0.4,
        "dpd_change": 0.5,
    },
}


@lending_tool(
    name="evaluate_monitoring_triggers",
    description="Check if signals breach segment-specific thresholds",
    category=ToolCategory.MONITORING,
    authority_level=AuthorityLevel.GENERAL,
    timeout_seconds=5,
)
async def evaluate_monitoring_triggers(
    loan_id: str = "",
    segment: str = "DAIRY_FARMER",
    signals: list[dict] | None = None,
) -> dict:
    thresholds = SEGMENT_THRESHOLDS.get(segment, {})
    triggered = []
    safe = []

    for signal in signals or []:
        stype = signal.get("signal_type", "")
        value = signal.get("value", 0.0)
        threshold = thresholds.get(stype, 0.7)

        if value > threshold:
            triggered.append(
                {
                    "signal_type": stype,
                    "value": value,
                    "threshold": threshold,
                    "severity": "HIGH" if value > threshold * 1.5 else "MEDIUM",
                }
            )
        else:
            safe.append(stype)

    action = "NONE"
    if len(triggered) >= 3:
        action = "ESCALATE"
    elif len(triggered) >= 1:
        action = "WATCH"

    return {
        "loan_id": loan_id or "LOAN-001",
        "segment": segment,
        "triggered": triggered,
        "safe": safe,
        "recommended_action": action,
    }
