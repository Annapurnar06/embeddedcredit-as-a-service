"""Warehouse receipt data fetch -- mock with realistic schema."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import WarehouseReceiptData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_warehouse_receipt",
    description="Fetch warehouse receipt details: commodity, quantity, grade, value",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_warehouse_receipt(
    receipt_id: str = "",
    warehouse_id: str = "",
) -> dict:
    if not receipt_id:
        return {"error": "receipt_id required"}

    return WarehouseReceiptData(
        receipt_id=receipt_id,
        warehouse_name="Central Warehousing Corporation - Indore",
        commodity="Soybean",
        quantity_quintals=150.0,
        quality_grade="FAQ",
        storage_date="2025-11-15",
        warehouse_grade="A",
        estimated_value=Decimal("675000.00"),
        insurance_active=True,
    ).model_dump()
