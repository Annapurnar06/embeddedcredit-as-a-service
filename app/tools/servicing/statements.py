"""Account statement generation."""
from __future__ import annotations

import uuid

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="generate_statement",
    description="Generate account statement, interest certificate, or schedule PDF",
    category=ToolCategory.SERVICING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=10,
)
async def generate_statement(
    loan_id: str = "",
    statement_type: str = "account_statement",
    period: str = "FY2025-26",
) -> dict:
    return {
        "loan_id": loan_id or "LOAN-001",
        "statement_type": statement_type,
        "period": period,
        "document_id": str(uuid.uuid4()),
        "download_url": f"/documents/{uuid.uuid4().hex[:12]}.pdf",
        "generated": True,
    }
