"""Credit bureau pull -- DESTRUCTIVE tool (hard inquiry)."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import BureauReport
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="pull_credit_bureau",
    description="Pull credit bureau report (CIBIL/Experian). DESTRUCTIVE: hard inquiry.",
    category=ToolCategory.DATA,
    requires_confirmation=True,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def pull_credit_bureau(
    aadhaar_hash: str = "",
    bureau: str = "CIBIL",
    purpose: str = "ORIGINATION",
) -> dict:
    if not aadhaar_hash:
        return {"error": "aadhaar_hash required"}

    return BureauReport(
        bureau=bureau,
        score=720,
        grade="B1",
        total_accounts=5,
        active_accounts=3,
        overdue_accounts=0,
        total_outstanding=Decimal("85000.00"),
        enquiry_count_6m=1,
        dpd_max_12m=0,
        flags=[],
    ).model_dump()
