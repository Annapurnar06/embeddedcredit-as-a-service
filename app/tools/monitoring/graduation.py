"""Evaluate borrower for graduation to better terms or top-up."""

from __future__ import annotations

from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="evaluate_graduation",
    description="Check if borrower qualifies for graduation: rate/limit/top-up",
    category=ToolCategory.MONITORING,
    authority_level=AuthorityLevel.GENERAL,
    timeout_seconds=5,
)
async def evaluate_graduation(
    loan_id: str = "",
    months_on_book: int = 0,
    on_time_rate: float = 1.0,
    current_rate: float = 15.0,
    current_limit: float = 100000.0,
) -> dict:
    eligible = months_on_book >= 6 and on_time_rate >= 0.9

    offers = []
    if eligible:
        if on_time_rate >= 0.95:
            new_rate = max(current_rate - 2.0, 10.0)
            offers.append(
                {
                    "type": "RATE_REDUCTION",
                    "current_rate": current_rate,
                    "proposed_rate": new_rate,
                }
            )

        if months_on_book >= 9 and on_time_rate >= 0.95:
            offers.append(
                {
                    "type": "LIMIT_INCREASE",
                    "current_limit": current_limit,
                    "proposed_limit": current_limit * 1.25,
                }
            )

        if months_on_book >= 12:
            offers.append(
                {
                    "type": "TOP_UP",
                    "max_top_up": current_limit * 0.5,
                }
            )

    return {
        "loan_id": loan_id or "LOAN-001",
        "eligible": eligible,
        "months_on_book": months_on_book,
        "on_time_rate": on_time_rate,
        "offers": offers,
        "offer_count": len(offers),
    }
