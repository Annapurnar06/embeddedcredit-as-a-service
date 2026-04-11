"""Account Aggregator bank data fetch -- mock Setu AA response."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import BankAccountData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_aa_bank_data",
    description="Fetch bank account data via Account Aggregator (post-consent)",
    category=ToolCategory.DATA,
    timeout_seconds=10,
    circuit_breaker_threshold=5,
)
async def fetch_aa_bank_data(
    consent_id: str = "",
    account_id: str = "",
) -> dict:
    if not consent_id:
        return {"error": "Valid consent_id required"}

    return BankAccountData(
        account_number_masked="XXXX1234",
        bank_name="STATE BANK OF INDIA",
        months_available=12,
        avg_monthly_balance=Decimal("28500.00"),
        avg_monthly_inflow=Decimal("42000.00"),
        avg_monthly_outflow=Decimal("35000.00"),
        bounce_count=1,
        bounce_rate=0.017,
        salary_detected=False,
        estimated_monthly_income=Decimal("42000.00"),
        foir=0.32,
        transaction_categories={
            "dairy_income": Decimal("15000.00"),
            "agriculture_income": Decimal("8000.00"),
            "transfers_in": Decimal("12000.00"),
            "household": Decimal("18000.00"),
            "utilities": Decimal("3000.00"),
            "emi_payments": Decimal("5000.00"),
        },
    ).model_dump()
