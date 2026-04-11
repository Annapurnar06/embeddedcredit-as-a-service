"""Execute auto-interventions: moratorium, restructure, nudge."""
from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="execute_auto_intervention",
    description="Execute automated intervention based on monitoring triggers",
    category=ToolCategory.MONITORING,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=10,
)
async def execute_auto_intervention(
    loan_id: str = "",
    intervention_type: str = "nudge",
    reason: str = "",
) -> dict:
    actions = {
        "nudge": {
            "action": "SEND_NUDGE",
            "channel": "whatsapp",
            "message_template": "friendly_reminder",
            "auto_approved": True,
        },
        "moratorium": {
            "action": "AUTO_MORATORIUM",
            "months": 1,
            "requires_human_review": True,
            "auto_approved": False,
        },
        "restructure": {
            "action": "RESTRUCTURE_REFERRAL",
            "new_emi_estimate": "4500.00",
            "requires_human_review": True,
            "auto_approved": False,
        },
        "collection": {
            "action": "SOFT_COLLECTION",
            "channel": "whatsapp",
            "message_template": "payment_due_reminder",
            "auto_approved": True,
        },
    }
    detail = actions.get(intervention_type, actions["nudge"])
    return {
        "loan_id": loan_id or "LOAN-001",
        "intervention_id": str(uuid.uuid4()),
        "intervention_type": intervention_type,
        "reason": reason,
        "status": "EXECUTED" if detail.get("auto_approved") else "PENDING_REVIEW",
        **detail,
    }
