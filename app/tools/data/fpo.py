"""FPO entity data fetch -- mock with realistic schema."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import FPOEntityData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_fpo_data",
    description="Fetch FPO data: members, aggregation, NABARD grade, governance",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_fpo_data(
    registration_id: str = "",
    fpo_name: str = "",
) -> dict:
    if not registration_id:
        return {"error": "registration_id required"}

    return FPOEntityData(
        fpo_name=fpo_name or "Sahyadri Farmer Producer Company",
        registration_id=registration_id,
        member_count=850,
        aggregation_volume_trend="growing",
        nabard_grade="A",
        governance_score=0.82,
        avg_monthly_turnover=Decimal("4500000.00"),
    ).model_dump()
