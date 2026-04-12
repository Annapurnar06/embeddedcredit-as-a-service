"""Poll external signals: bank txns, cooperative data, platform payout changes."""

from __future__ import annotations

import random

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="poll_monitoring_signals",
    description="Poll external monitoring signals for a loan portfolio",
    category=ToolCategory.MONITORING,
    authority_level=AuthorityLevel.GENERAL,
    timeout_seconds=15,
)
async def poll_monitoring_signals(
    loan_id: str = "",
    signal_types: list[str] | None = None,
) -> dict:
    types = signal_types or [
        "bank_txn_drop",
        "cooperative_pouring_drop",
        "platform_deactivation",
        "dpd_change",
        "bureau_alert",
    ]
    signals = []
    for stype in types:
        signals.append(
            {
                "signal_type": stype,
                "value": random.uniform(0.0, 1.0),
                "threshold": 0.7,
                "triggered": random.random() > 0.8,
                "source": f"mock_{stype}_api",
            }
        )
    return {
        "loan_id": loan_id or "LOAN-001",
        "signals_polled": len(signals),
        "signals": signals,
        "triggered_count": sum(1 for s in signals if s["triggered"]),
    }
