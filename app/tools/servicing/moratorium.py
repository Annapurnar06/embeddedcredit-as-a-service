"""Moratorium application."""
from __future__ import annotations

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="apply_moratorium",
    description="Pause EMI for N months. Recalculate remaining schedule.",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=5,
)
async def apply_moratorium(
    loan_id: str = "",
    months: int = 1,
    reason: str = "",
) -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "moratorium_months": months,
        "reason": reason,
        "start_date": "2026-05-01",
        "end_date": f"2026-{5 + months:02d}-01",
        "revised_tenure_months": 18 + months,
        "status": "APPLIED",
        "no_late_fees": True,
        "no_npa_classification": True,
    }
