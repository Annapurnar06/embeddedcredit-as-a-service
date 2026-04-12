"""Account Aggregator consent initiation (mock Setu AA schema)."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from app.schemas.borrower import AAConsentResult
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="initiate_aa_consent",
    description="Initiate Account Aggregator consent request (Setu AA)",
    category=ToolCategory.IDENTITY,
    requires_confirmation=True,
    timeout_seconds=10,
)
async def initiate_aa_consent(
    borrower_phone: str = "",
    data_range_months: int = 12,
    fi_types: list[str] | None = None,
) -> dict:
    if not borrower_phone:
        return {"error": "Phone number required for AA consent"}

    consent_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    return AAConsentResult(
        consent_id=consent_id,
        consent_url=f"https://aa.setu.co/consent/{consent_id}",
        status="PENDING",
        expires_at=now + timedelta(hours=24),
    ).model_dump()
