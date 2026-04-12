"""Part-prepayment processing."""

from __future__ import annotations

from decimal import Decimal

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="process_prepayment",
    description="Process part-payment. Recalculate schedule.",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=5,
)
async def process_prepayment(
    loan_id: str = "",
    amount: float = 0,
    mode: str = "reduce_tenure",
) -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "prepayment_amount": str(Decimal(str(amount))),
        "mode": mode,
        "new_outstanding": str(Decimal("75000.00")),
        "months_saved": 2 if mode == "reduce_tenure" else 0,
        "new_emi": str(Decimal("5800.00")) if mode == "reduce_emi" else None,
        "status": "PROCESSED",
    }
