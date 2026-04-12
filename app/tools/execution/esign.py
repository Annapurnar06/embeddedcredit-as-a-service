"""Aadhaar e-Sign initiation -- mock."""

from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="initiate_esign",
    description="Initiate Aadhaar e-Sign (OTP mode for digital, voice for voice channel)",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=15,
)
async def initiate_esign(
    loan_application_id: str = "",
    document_hash: str = "",
) -> dict:
    return {
        "esign_id": str(uuid.uuid4()),
        "status": "OTP_SENT",
        "document_hash": document_hash or "sha256:mock",
    }
