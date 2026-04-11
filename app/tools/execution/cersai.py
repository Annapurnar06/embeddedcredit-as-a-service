"""CERSAI charge registration for secured loans -- mock."""
from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="register_cersai",
    description="CERSAI charge registration for secured loans",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.ACCOUNT,
    requires_confirmation=False,
    timeout_seconds=10,
)
async def register_cersai(
    loan_application_id: str = "",
    asset_type: str = "",
    asset_description: str = "",
) -> dict:
    return {
        "cersai_id": str(uuid.uuid4()),
        "status": "REGISTERED",
        "asset_type": asset_type,
        "charge_type": "HYPOTHECATION",
    }
