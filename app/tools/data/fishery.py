"""Fishery cooperative data fetch -- mock with realistic schema."""
from __future__ import annotations

from app.schemas.borrower import FisheryCooperativeData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_fishery_data",
    description="Fetch fishery cooperative data: catch regularity, volume, vessel, tenure",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_fishery_data(
    member_id: str = "",
    cooperative_id: str = "",
) -> dict:
    if not member_id:
        return {"error": "member_id required"}

    return FisheryCooperativeData(
        cooperative_name="Kerala Fishermen Cooperative Society",
        member_id=member_id,
        catch_regularity_pct=85.0,
        avg_monthly_catch_kg=450.0,
        catch_volume_trend="stable",
        vessel_owned=True,
        cooperative_tenure_months=48,
    ).model_dump()
