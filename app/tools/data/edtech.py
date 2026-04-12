"""Edtech platform data fetch -- mock with realistic schema."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.borrower import EdtechPlatformData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_edtech_data",
    description="Fetch edtech platform data: completion rate, placement rate, salary",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_edtech_data(
    student_id: str = "",
    platform: str = "",
) -> dict:
    if not student_id:
        return {"error": "student_id required"}

    return EdtechPlatformData(
        platform_name=platform or "UpGrad",
        student_id=student_id,
        course_name="Full Stack Development",
        course_duration_months=9,
        completion_rate_pct=78.0,
        placement_rate_pct=72.0,
        avg_placement_salary=Decimal("600000.00"),
    ).model_dump()
