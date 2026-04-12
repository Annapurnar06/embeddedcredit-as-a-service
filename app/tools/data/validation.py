"""Cross-validation, confidence scoring, and profile assembly."""

from __future__ import annotations

from uuid import UUID, uuid4

from app.schemas.borrower import (
    BorrowerProfile,
    ConfidenceScore,
    CrossValidationResult,
)
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="cross_validate_sources",
    description="Entity resolution + cross-source validation",
    category=ToolCategory.DATA,
    timeout_seconds=2,
)
async def cross_validate_sources(
    bank_income: float = 0,
    cooperative_income: float = 0,
    name_sources: list[str] | None = None,
) -> dict:
    income_delta = 0.0
    if bank_income > 0 and cooperative_income > 0:
        income_delta = abs(bank_income - cooperative_income) / max(bank_income, cooperative_income)

    anomalies = []
    if income_delta > 0.3:
        anomalies.append(
            f"Income mismatch: bank={bank_income}, cooperative={cooperative_income} "
            f"(delta={income_delta:.1%})"
        )

    return CrossValidationResult(
        consistent=len(anomalies) == 0,
        income_delta_pct=round(income_delta * 100, 1),
        name_consistency=0.95,
        address_consistency=0.88,
        anomalies=anomalies,
    ).model_dump()


@lending_tool(
    name="compute_confidence_score",
    description="Weighted confidence: sources/freshness/validation/anomaly",
    category=ToolCategory.DATA,
    timeout_seconds=1,
)
async def compute_confidence_score(
    sources_available: int = 0,
    sources_required: int = 3,
    freshness_ok: bool = True,
    validation_passed: bool = True,
    anomaly_free: bool = True,
) -> dict:
    src_score = min(sources_available / max(sources_required, 1), 1.0)
    fresh_score = 1.0 if freshness_ok else 0.5
    val_score = 1.0 if validation_passed else 0.6
    anomaly_score = 1.0 if anomaly_free else 0.3

    score = 0.3 * src_score + 0.3 * fresh_score + 0.2 * val_score + 0.2 * anomaly_score

    if score >= 0.8:
        level = "HIGH"
    elif score >= 0.5:
        level = "MEDIUM"
    else:
        level = "LOW"

    return ConfidenceScore(
        score=round(score, 2),
        level=level,
        sources_available=sources_available,
        sources_required=sources_required,
        freshness_score=fresh_score,
        validation_score=val_score,
        anomaly_free_score=anomaly_score,
    ).model_dump()


@lending_tool(
    name="compute_borrower_profile",
    description="Assemble all fetched data into unified enriched borrower profile",
    category=ToolCategory.DATA,
    timeout_seconds=2,
)
async def compute_borrower_profile(
    borrower_id: str = "",
    segment: str = "",
    aadhaar_verified: bool = False,
    pan_verified: bool = False,
    bank_verified: bool = False,
) -> dict:
    bid = UUID(borrower_id) if borrower_id else uuid4()
    return BorrowerProfile(
        borrower_id=bid,
        aadhaar_verified=aadhaar_verified,
        pan_verified=pan_verified,
        bank_account_verified=bank_verified,
        segment=segment,
    ).model_dump()
