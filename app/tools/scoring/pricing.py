"""Risk-based pricing -- score to rate band mapping."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.loan import RiskPricing
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

RATE_BANDS = [
    (750, 900, "A1", Decimal("12.00"), Decimal("0.00")),
    (650, 749, "A2", Decimal("14.00"), Decimal("2.00")),
    (550, 649, "B1", Decimal("16.00"), Decimal("4.00")),
    (450, 549, "B2", Decimal("18.00"), Decimal("6.00")),
    (0, 449, "C", Decimal("22.00"), Decimal("10.00")),
]

BASE_RATE = Decimal("12.00")


@lending_tool(
    name="compute_risk_pricing",
    description="Map score to interest rate band",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=1,
)
async def compute_risk_pricing(score: int = 0) -> dict:
    for low, high, band, rate, premium in RATE_BANDS:
        if low <= score <= high:
            return RiskPricing(
                interest_rate=rate,
                rate_band=band,
                risk_premium=premium,
                base_rate=BASE_RATE,
            ).model_dump()

    return RiskPricing(
        interest_rate=Decimal("22.00"),
        rate_band="C",
        risk_premium=Decimal("10.00"),
        base_rate=BASE_RATE,
    ).model_dump()
