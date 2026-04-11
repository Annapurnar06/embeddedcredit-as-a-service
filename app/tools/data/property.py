"""Property records data fetch -- mock with realistic schema."""
from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import PropertyRecordsData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_property_records",
    description="Fetch property records: title, encumbrance, valuation, area",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_property_records(
    property_id: str = "",
    owner_name: str = "",
) -> dict:
    if not property_id:
        return {"error": "property_id required"}

    return PropertyRecordsData(
        property_id=property_id,
        clear_title=True,
        encumbrance_free=True,
        property_type="residential",
        area_sqft=450.0,
        market_valuation=Decimal("850000.00"),
        location_pin="400001",
    ).model_dump()
