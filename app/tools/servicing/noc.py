"""No Objection Certificate on loan closure."""
from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="generate_noc",
    description="Generate No Objection Certificate on loan closure",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
)
async def generate_noc(loan_id: str = "") -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "noc_id": str(uuid.uuid4()),
        "status": "GENERATED",
        "closure_date": "2026-12-15",
        "download_url": f"/documents/noc_{uuid.uuid4().hex[:8]}.pdf",
    }
