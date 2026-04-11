"""Disbursement execution -- mock UPI/NEFT with maker-checker."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.schemas.loan import DisbursementResult
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="execute_disbursement",
    description="Initiate UPI/NEFT disbursement. Requires maker-checker approval.",
    category=ToolCategory.EXECUTION,
    authority_level=AuthorityLevel.WRITE,
    requires_confirmation=True,
    timeout_seconds=15,
)
async def execute_disbursement(
    loan_application_id: str = "",
    amount: float = 0,
    mode: str = "UPI",
    beneficiary_account: str = "",
) -> dict:
    return DisbursementResult(
        reference_id=f"DISB-{uuid.uuid4().hex[:12].upper()}",
        status="SUCCESS",
        amount=Decimal(str(amount)),
        mode=mode,
        beneficiary_account_masked=(
            f"XXXX{beneficiary_account[-4:]}" if beneficiary_account else "XXXX0000"
        ),
        timestamp=datetime.now(timezone.utc).isoformat(),
    ).model_dump()
