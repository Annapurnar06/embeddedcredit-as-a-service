"""Repayment schedule retrieval."""
from __future__ import annotations

from decimal import Decimal

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="get_repayment_schedule",
    description="Get full repayment schedule with actual vs expected",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
)
async def get_repayment_schedule(loan_id: str = "") -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "schedule_type": "SEASONAL_DYNAMIC",
        "total_months": 18,
        "completed_months": 4,
        "on_time_rate": 1.0,
        "entries": [
            {
                "month": i + 1,
                "due_date": f"2026-{(i + 1) % 12 + 1:02d}-15",
                "emi_amount": str(Decimal("6500.00") if i % 3 != 2 else Decimal("4000.00")),
                "paid": i < 4,
                "paid_amount": str(Decimal("6500.00")) if i < 4 else None,
                "paid_on_time": True if i < 4 else None,
            }
            for i in range(18)
        ],
    }
