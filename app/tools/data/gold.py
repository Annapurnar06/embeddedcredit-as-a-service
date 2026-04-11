"""Gold appraisal data fetch -- mock with realistic schema."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import GoldAppraisalData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_gold_appraisal",
    description="Fetch gold appraisal: weight, purity, market rate, appraised value",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_gold_appraisal(
    appraisal_id: str = "",
    customer_id: str = "",
) -> dict:
    if not appraisal_id:
        return {"error": "appraisal_id required"}

    return GoldAppraisalData(
        appraisal_id=appraisal_id,
        gold_weight_grams=45.5,
        purity_karats=22.0,
        market_rate_per_gram=Decimal("6200.00"),
        appraised_value=Decimal("282100.00"),
        ornament_description="Gold bangles (2) + chain (1)",
        hallmark_verified=True,
    ).model_dump()
