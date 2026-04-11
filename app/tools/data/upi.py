"""UPI transaction data fetch -- mock for micro merchants."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import UPITransactionData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_upi_transactions",
    description="Fetch UPI merchant data: daily collections, regularity, customers",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_upi_transactions(
    merchant_id: str = "",
    months: int = 6,
) -> dict:
    if not merchant_id:
        return {"error": "merchant_id required"}

    return UPITransactionData(
        merchant_id=merchant_id,
        avg_daily_collections=Decimal("3500.00"),
        collection_regularity_pct=88.0,
        unique_customers_30d=120,
        avg_transaction_value=Decimal("185.00"),
        peak_hour_collections_pct=0.35,
    ).model_dump()
