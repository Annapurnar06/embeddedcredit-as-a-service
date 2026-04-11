"""Segment scoring -- rule-based v1 (weighted sum from YAML config)."""
from __future__ import annotations

from app.schemas.loan import ScoreResult
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

SEGMENT_WEIGHTS = {
    "DAIRY_FARMER": {
        "pouring_regularity": 0.25,
        "pouring_volume_trend": 0.18,
        "cooperative_tenure": 0.12,
        "land_area": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "KIRANA_SHOP": {
        "gst_turnover_trend": 0.30,
        "bank_inflow_regularity": 0.25,
        "bureau_score": 0.20,
        "gst_filing_regularity": 0.15,
        "device_score": 0.10,
    },
    "GIG_WORKER": {
        "platform_earnings_trend": 0.30,
        "platform_rating": 0.15,
        "active_days": 0.15,
        "bank_stability": 0.20,
        "bureau_score": 0.20,
    },
}


def _normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 0.5
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


@lending_tool(
    name="compute_segment_score",
    description="Run segment-specific scoring model (rule-based v1: weighted sum)",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=3,
)
async def compute_segment_score(
    segment: str = "DAIRY_FARMER",
    features: dict | None = None,
) -> dict:
    features = features or {}
    weights = SEGMENT_WEIGHTS.get(segment, SEGMENT_WEIGHTS["DAIRY_FARMER"])

    weighted_sum = 0.0
    contributions = {}
    for feature_name, weight in weights.items():
        value = features.get(feature_name, 0.5)
        normalized = _normalize(value, 0, 1) if isinstance(value, float) else value / 900
        contribution = normalized * weight
        weighted_sum += contribution
        contributions[feature_name] = round(contribution, 4)

    score = int(weighted_sum * 900)
    score = max(0, min(900, score))

    if score >= 750:
        grade = "A1"
    elif score >= 650:
        grade = "A2"
    elif score >= 550:
        grade = "B1"
    elif score >= 450:
        grade = "B2"
    else:
        grade = "REJECT"

    return ScoreResult(
        score=score,
        grade=grade,
        model_version=f"{segment.lower()}_score_v1",
        feature_contributions=contributions,
    ).model_dump()
