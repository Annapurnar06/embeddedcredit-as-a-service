"""Gig platform earnings fetch -- mock Swiggy/Zomato/Uber schema."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import PlatformEarnings
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_platform_earnings",
    description="Fetch gig platform earnings (Swiggy/Zomato/Uber)",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_platform_earnings(
    platform: str = "swiggy",
    platform_user_id: str = "",
) -> dict:
    if not platform_user_id:
        return {"error": "platform_user_id required"}

    return PlatformEarnings(
        platform=platform,
        active_months=18,
        avg_monthly_earnings=Decimal("22000.00"),
        avg_monthly_deliveries=280,
        avg_rating=4.6,
        active_days_pct=0.82,
    ).model_dump()
