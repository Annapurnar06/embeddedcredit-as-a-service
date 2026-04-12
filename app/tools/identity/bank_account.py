"""Bank account verification via penny drop (mock implementation)."""

from __future__ import annotations

from app.schemas.borrower import BankAccountVerifyResult
from app.tools.identity.pan import _jaro_winkler_similarity
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="verify_bank_account",
    description="Verify bank account via penny drop (INR 1 IMPS) + name match",
    category=ToolCategory.IDENTITY,
    requires_confirmation=False,
    timeout_seconds=15,
)
async def verify_bank_account(
    account_number: str = "",
    ifsc: str = "",
    aadhaar_name: str = "",
) -> dict:
    if not account_number or not ifsc:
        return BankAccountVerifyResult(account_valid=False).model_dump()

    mock_account_name = "RAMESH PATEL"
    name_match = _jaro_winkler_similarity(aadhaar_name, mock_account_name)

    return BankAccountVerifyResult(
        account_valid=True,
        name_on_account=mock_account_name,
        name_match_score=round(name_match, 3),
        ifsc=ifsc,
        bank_name="STATE BANK OF INDIA",
    ).model_dump()
