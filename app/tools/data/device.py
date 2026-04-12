"""Device score computation -- DeviceConnect equivalent."""

from __future__ import annotations

from app.schemas.borrower import DeviceScore
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="compute_device_score",
    description="Compute behavioral device score (0-1000 inclusion score)",
    category=ToolCategory.DATA,
    timeout_seconds=3,
    circuit_breaker_threshold=5,
)
async def compute_device_score(
    device_fingerprint: str = "",
) -> dict:
    return DeviceScore(
        score=680,
        confidence=0.75,
    ).model_dump()
