"""Vehicle telematics data fetch -- mock for trucks, autos, cabs."""
from __future__ import annotations

from app.schemas.borrower import VehicleTelematicsData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_vehicle_telematics",
    description="Fetch vehicle telematics: km driven, trips, fuel, FASTag, load utilization",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_vehicle_telematics(
    vehicle_id: str = "",
    vehicle_type: str = "truck",
) -> dict:
    if not vehicle_id:
        return {"error": "vehicle_id required"}

    return VehicleTelematicsData(
        vehicle_id=vehicle_id,
        vehicle_type=vehicle_type,
        monthly_km_driven=8500.0 if vehicle_type == "truck" else 3200.0,
        daily_trips_avg=2 if vehicle_type == "truck" else 18,
        fuel_efficiency_kmpl=4.5 if vehicle_type == "truck" else 25.0,
        fastag_trips_30d=45 if vehicle_type == "truck" else 0,
        load_utilization_pct=82.0 if vehicle_type == "truck" else None,
        idle_days_30d=3,
    ).model_dump()
