"""EV telematics data fetch -- mock with realistic schema."""
from __future__ import annotations

from app.schemas.borrower import EVTelematicsData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_ev_telematics",
    description="Fetch EV telematics: daily km, battery health, charging, trips",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_ev_telematics(
    vehicle_id: str = "",
    platform: str = "",
) -> dict:
    if not vehicle_id:
        return {"error": "vehicle_id required"}

    return EVTelematicsData(
        vehicle_id=vehicle_id,
        daily_km_avg=85.0,
        battery_health_pct=92.0,
        charging_regularity_pct=95.0,
        total_trips_30d=720,
        battery_cycles=280,
        vehicle_model="Ather 450X",
    ).model_dump()
