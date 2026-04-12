"""Dairy cooperative data fetch -- mock with realistic schema."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import CooperativeData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_cooperative_data",
    description="Fetch dairy cooperative data: pouring, fat%, payments, tenure",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_cooperative_data(
    membership_id: str = "",
    cooperative_id: str = "",
) -> dict:
    if not membership_id:
        return {"error": "membership_id required"}

    return CooperativeData(
        cooperative_name="Banaskantha Dairy Cooperative",
        membership_id=membership_id,
        membership_tenure_months=48,
        avg_daily_pouring_liters=12.5,
        avg_fat_percentage=6.2,
        pouring_regularity_pct=92.0,
        last_payment_amount=Decimal("15000.00"),
        payment_regularity_pct=95.0,
        total_payouts_6m=Decimal("90000.00"),
    ).model_dump()
