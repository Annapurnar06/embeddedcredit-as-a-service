"""Loan status inquiry."""

from __future__ import annotations

from decimal import Decimal

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="get_loan_status",
    description="Get loan balance, rate, next EMI, DPD, insurance status",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
)
async def get_loan_status(loan_id: str = "") -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "status": "ACTIVE",
        "outstanding_balance": str(Decimal("85000.00")),
        "interest_rate": "15.00",
        "next_emi_date": "2026-05-15",
        "next_emi_amount": str(Decimal("6500.00")),
        "dpd": 0,
        "insurance_status": "ACTIVE",
        "total_paid": str(Decimal("15000.00")),
        "total_remaining": str(Decimal("85000.00")),
        "months_remaining": 14,
    }
