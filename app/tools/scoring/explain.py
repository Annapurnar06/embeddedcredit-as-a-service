"""Explainability -- reason codes for borrower-facing rejection reasons."""
from __future__ import annotations

from app.schemas.loan import ExplainabilityResult
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

REASON_CODE_MAP = {
    "SCORE_BELOW_MINIMUM": {
        "en": "Your credit score does not meet minimum requirements",
        "hi": "Aapka credit score nyuntam avashyakta se kam hai",
    },
    "HIGH_EXISTING_DEBT": {
        "en": "Your existing debt obligations are too high",
        "hi": "Aapka maujooda karz bahut zyada hai",
    },
    "LOW_CONFIDENCE_SCORE": {
        "en": "Insufficient data available for assessment",
        "hi": "Mulyankan ke liye paryapt data uplabdh nahi hai",
    },
    "FRAUD_FLAG_ACTIVE": {
        "en": "Application flagged for additional verification",
        "hi": "Aavedan ko aur jach ke liye flag kiya gaya",
    },
}


@lending_tool(
    name="generate_explainability",
    description="Generate reason codes and borrower-facing rejection reasons (RBI compliant)",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=3,
)
async def generate_explainability(
    decision: str = "",
    reason_codes: list[str] | None = None,
    feature_importance: dict | None = None,
    language: str = "hi",
) -> dict:
    codes = reason_codes or []
    borrower_reasons = []
    for code in codes:
        mapping = REASON_CODE_MAP.get(code, {})
        reason = mapping.get(language, mapping.get("en", code))
        borrower_reasons.append(reason)

    return ExplainabilityResult(
        decision=decision,
        reason_codes=codes,
        borrower_facing_reasons=borrower_reasons,
        feature_importance=feature_importance or {},
    ).model_dump()
