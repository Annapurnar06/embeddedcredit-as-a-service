"""Dynamic product design based on approved decision + borrower profile."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.loan import LoanProduct
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="design_dynamic_product",
    description="Design loan product: amount, rate, tenure, schedule type, insurance",
    category=ToolCategory.PRODUCT,
    timeout_seconds=5,
)
async def design_dynamic_product(
    segment: str = "DAIRY_FARMER",
    score: int = 650,
    interest_rate: float = 15.0,
    requested_amount: float = 100000,
    monthly_income: float = 42000,
) -> dict:
    max_emi = monthly_income * 0.4

    schedule_map = {
        "DAIRY_FARMER": ("SEASONAL_DYNAMIC", 18, "PASHU_BIMA"),
        "KIRANA_SHOP": ("DAILY_MICRO", 12, None),
        "GIG_WORKER": ("PAYOUT_LINKED", 12, None),
    }
    schedule_type, default_tenure, insurance = schedule_map.get(
        segment, ("EMI", 12, None)
    )

    amount = Decimal(str(min(requested_amount, max_emi * default_tenure * 0.8)))
    total_interest = amount * Decimal(str(interest_rate / 100)) * Decimal(
        str(default_tenure / 12)
    )
    total_repayment = amount + total_interest
    processing_fee = amount * Decimal("0.02")

    return LoanProduct(
        amount=amount.quantize(Decimal("0.01")),
        interest_rate=Decimal(str(interest_rate)),
        tenure_months=default_tenure,
        schedule_type=schedule_type,
        insurance_type=insurance,
        insurance_premium=Decimal("1500.00") if insurance else None,
        processing_fee=processing_fee.quantize(Decimal("0.01")),
        total_interest=total_interest.quantize(Decimal("0.01")),
        total_repayment=total_repayment.quantize(Decimal("0.01")),
        moratorium_triggers=(
            [
                {"type": "WEATHER_HEAT", "threshold_celsius": 38, "duration_months": 1},
                {"type": "PRODUCTION_DROP", "threshold_percent": 40, "duration_months": 1},
            ]
            if segment == "DAIRY_FARMER"
            else []
        ),
    ).model_dump()
