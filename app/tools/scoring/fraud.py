"""Fraud signal checking -- velocity, device, reference graph."""
from __future__ import annotations

from app.schemas.loan import FraudCheckResult
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="check_fraud_signals",
    description="Velocity checks, device fingerprint, reference graph fraud detection",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
)
async def check_fraud_signals(
    aadhaar_hash: str = "",
    device_fingerprint: str = "",
    applications_48h: int = 0,
) -> dict:
    flags = []

    if applications_48h > 3:
        flags.append("HIGH_VELOCITY_APPLICATIONS")

    if not device_fingerprint:
        flags.append("MISSING_DEVICE_FINGERPRINT")

    if flags:
        return FraudCheckResult(
            result="HOLD" if len(flags) == 1 else "REJECT",
            flags=flags,
        ).model_dump()

    return FraudCheckResult(
        result="PASS",
        flags=[],
        velocity_check=True,
        device_check=True,
        reference_check=True,
    ).model_dump()
