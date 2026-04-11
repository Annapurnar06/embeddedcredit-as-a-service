"""Insurance enrollment -- mock Pashu Bima/PMFBY."""
from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="enroll_insurance",
    description="Insurance enrollment (Pashu Bima, PMFBY, health)",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=10,
)
async def enroll_insurance(
    insurance_type: str = "PASHU_BIMA",
    sum_insured: float = 0,
    borrower_id: str = "",
) -> dict:
    return {
        "enrollment_id": str(uuid.uuid4()),
        "insurance_type": insurance_type,
        "sum_insured": sum_insured,
        "status": "ENROLLED",
        "policy_start": "2026-05-01",
    }
