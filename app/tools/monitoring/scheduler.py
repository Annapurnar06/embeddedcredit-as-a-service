"""Monitoring job scheduler -- cron-like for batch signal polling."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

SCHEDULE_PRESETS: dict[str, dict] = {
    "DAIRY_FARMER": {
        "frequency": "weekly",
        "signals": ["cooperative_pouring_drop", "bank_txn_drop"],
    },
    "KIRANA_SHOP": {"frequency": "daily", "signals": ["bank_txn_drop", "inflow_drop"]},
    "GIG_WORKER": {"frequency": "daily", "signals": ["platform_deactivation", "payout_drop"]},
}


@lending_tool(
    name="schedule_monitoring_job",
    description="Schedule a monitoring job for batch signal polling",
    category=ToolCategory.MONITORING,
    authority_level=AuthorityLevel.WRITE,
    timeout_seconds=5,
)
async def schedule_monitoring_job(
    loan_id: str = "",
    segment: str = "DAIRY_FARMER",
    override_frequency: str | None = None,
) -> dict:
    preset = SCHEDULE_PRESETS.get(segment, SCHEDULE_PRESETS["DAIRY_FARMER"])
    freq = override_frequency or preset["frequency"]
    return {
        "job_id": str(uuid.uuid4()),
        "loan_id": loan_id or "LOAN-001",
        "segment": segment,
        "frequency": freq,
        "signals": preset["signals"],
        "next_run": datetime.now(timezone.utc).isoformat(),
        "status": "SCHEDULED",
    }
