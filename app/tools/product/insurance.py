"""Insurance premium computation."""

from __future__ import annotations

from decimal import Decimal

from app.tools.registry import ToolCategory, lending_tool

PREMIUM_RATES = {
    "PASHU_BIMA": Decimal("0.03"),
    "CROP_PMFBY": Decimal("0.02"),
    "HEALTH": Decimal("0.04"),
}


@lending_tool(
    name="compute_insurance_premium",
    description="Compute insurance premium (Pashu Bima, PMFBY, health)",
    category=ToolCategory.PRODUCT,
    timeout_seconds=2,
)
async def compute_insurance_premium(
    insurance_type: str = "PASHU_BIMA",
    sum_insured: float = 100000,
) -> dict:
    rate = PREMIUM_RATES.get(insurance_type, Decimal("0.03"))
    premium = Decimal(str(sum_insured)) * rate

    return {
        "insurance_type": insurance_type,
        "sum_insured": str(Decimal(str(sum_insured))),
        "premium_rate": str(rate),
        "annual_premium": str(premium.quantize(Decimal("0.01"))),
        "gst": str((premium * Decimal("0.18")).quantize(Decimal("0.01"))),
        "total_premium": str((premium * Decimal("1.18")).quantize(Decimal("0.01"))),
    }
