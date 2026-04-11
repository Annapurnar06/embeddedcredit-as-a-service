"""Key Fact Statement generation -- RBI mandatory before disbursement."""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.schemas.loan import KeyFactStatement
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="generate_kfs",
    description="Generate Key Fact Statement (RBI Digital Lending mandatory)",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.ACCOUNT,
    requires_confirmation=False,
    timeout_seconds=5,
)
async def generate_kfs(
    loan_application_id: str = "",
    borrower_name: str = "",
    lender_name: str = "",
    amount: float = 0,
    rate: float = 0,
    tenure_months: int = 0,
    processing_fee: float = 0,
    insurance_premium: float | None = None,
) -> dict:
    lid = UUID(loan_application_id) if loan_application_id else uuid4()
    amt = Decimal(str(amount))
    total_interest = amt * Decimal(str(rate / 100)) * Decimal(str(tenure_months / 12))
    total_repayment = amt + total_interest
    emi = total_repayment / tenure_months if tenure_months > 0 else Decimal("0")
    apr = Decimal(str(rate)) + Decimal("0.5")

    return KeyFactStatement(
        loan_application_id=lid,
        borrower_name=borrower_name,
        lender_name=lender_name,
        loan_amount=amt,
        interest_rate=Decimal(str(rate)),
        tenure_months=tenure_months,
        emi_amount=emi.quantize(Decimal("0.01")),
        total_interest=total_interest.quantize(Decimal("0.01")),
        total_repayment=total_repayment.quantize(Decimal("0.01")),
        processing_fee=Decimal(str(processing_fee)),
        insurance_premium=Decimal(str(insurance_premium)) if insurance_premium else None,
        annual_percentage_rate=apr,
        cooling_off_period_days=3,
        grievance_officer_name="Grievance Officer",
        grievance_officer_contact="grievance@lender.com",
        generated_at=datetime.now(timezone.utc).isoformat(),
    ).model_dump()
