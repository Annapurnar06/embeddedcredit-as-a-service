"""Solar generation data fetch -- mock with realistic schema."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import SolarGenerationData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_solar_generation",
    description="Fetch solar panel data: generation kWh, savings, degradation, net metering",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_solar_generation(
    installation_id: str = "",
    customer_id: str = "",
) -> dict:
    if not installation_id:
        return {"error": "installation_id required"}

    return SolarGenerationData(
        installation_id=installation_id,
        capacity_kw=5.0,
        avg_daily_generation_kwh=18.5,
        grid_savings_monthly=Decimal("3500.00"),
        panel_degradation_pct=1.2,
        net_metering_active=True,
        installation_date="2024-06-15",
    ).model_dump()
