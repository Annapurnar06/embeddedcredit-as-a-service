"""AML/sanctions/fraud blacklist check (mock implementation)."""
from __future__ import annotations

from app.schemas.borrower import NegativeListResult
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="check_negative_list",
    description="AML/sanctions/fraud blacklist check against Aadhaar hash",
    category=ToolCategory.IDENTITY,
    requires_confirmation=False,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def check_negative_list(
    aadhaar_hash: str = "",
) -> dict:
    if not aadhaar_hash:
        return NegativeListResult(
            clear=False, flags=["MISSING_IDENTIFIER"]
        ).model_dump()

    return NegativeListResult(
        clear=True,
        flags=[],
        sources_checked=["RBI_WILFUL_DEFAULTER", "CIBIL_FRAUD", "SANCTIONS_LIST", "PEP_LIST"],
    ).model_dump()
