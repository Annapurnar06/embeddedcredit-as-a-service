"""SHG records data fetch -- mock with realistic schema."""
from __future__ import annotations

from app.schemas.borrower import SHGRecordsData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_shg_records",
    description="Fetch SHG data: group repayment, attendance, savings, NRLM grade",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_shg_records(
    group_id: str = "",
    member_id: str = "",
) -> dict:
    if not group_id:
        return {"error": "group_id required"}

    return SHGRecordsData(
        shg_name="Lakshmi Self Help Group",
        group_id=group_id,
        member_count=12,
        group_tenure_months=36,
        meeting_attendance_pct=92.0,
        group_repayment_rate=97.0,
        individual_savings_regularity=88.0,
        nrlm_grade="A",
    ).model_dump()
