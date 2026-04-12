"""GST returns fetch -- mock GSTN API."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from app.schemas.borrower import GSTData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_gst_returns",
    description="Fetch GST filing history from GSTN",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_gst_returns(
    gstin: str = "",
) -> dict:
    if not gstin or len(gstin) != 15:
        return {"error": "Valid 15-char GSTIN required"}

    return GSTData(
        gstin=gstin,
        business_name="PATEL KIRANA STORE",
        filing_regularity_pct=91.7,
        avg_monthly_turnover=Decimal("350000.00"),
        turnover_trend="growing",
        last_filing_date=date(2026, 3, 15),
    ).model_dump()
