"""eNACH/UPI autopay mandate setup -- mock."""

from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="setup_enach_mandate",
    description="Setup eNACH/UPI autopay mandate for EMI collection",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=10,
)
async def setup_enach_mandate(
    account_number: str = "",
    ifsc: str = "",
    max_amount: float = 0,
    frequency: str = "monthly",
) -> dict:
    return {
        "mandate_id": str(uuid.uuid4()),
        "status": "REGISTERED",
        "max_amount": max_amount,
        "frequency": frequency,
        "mode": "eNACH",
    }
