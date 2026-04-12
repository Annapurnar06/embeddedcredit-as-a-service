"""Poultry integrator data fetch -- mock with realistic schema."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import PoultryIntegratorData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_poultry_data",
    description="Fetch poultry integrator data: mortality, FCR, batches, revenue",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_poultry_data(
    farmer_id: str = "",
    integrator_id: str = "",
) -> dict:
    if not farmer_id:
        return {"error": "farmer_id required"}

    return PoultryIntegratorData(
        integrator_name="Suguna Poultry",
        farmer_id=farmer_id,
        batch_count_12m=6,
        avg_mortality_rate_pct=3.5,
        feed_conversion_ratio=1.72,
        avg_batch_revenue=Decimal("85000.00"),
        integrator_tenure_months=30,
    ).model_dump()
