"""Segment policy evaluation -- load YAML policy, evaluate against profile."""
from __future__ import annotations

from app.schemas.loan import PolicyEvaluation
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="evaluate_segment_policy",
    description="Load YAML policy for segment, evaluate against enriched profile",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=5,
)
async def evaluate_segment_policy(
    segment: str = "",
    score: int = 0,
    confidence_level: str = "LOW",
    fraud_clear: bool = True,
) -> dict:
    if not fraud_clear:
        return PolicyEvaluation(
            decision="REJECT",
            reason_codes=["FRAUD_FLAG_ACTIVE"],
            policy_id=f"{segment}_v1",
            policy_version="1.0",
        ).model_dump()

    if confidence_level == "LOW":
        return PolicyEvaluation(
            decision="REFER",
            reason_codes=["LOW_CONFIDENCE_SCORE"],
            policy_id=f"{segment}_v1",
            policy_version="1.0",
        ).model_dump()

    if score >= 650:
        return PolicyEvaluation(
            decision="APPROVE",
            reason_codes=["SCORE_ABOVE_THRESHOLD", "CONFIDENCE_SUFFICIENT"],
            policy_id=f"{segment}_v1",
            policy_version="1.0",
        ).model_dump()
    elif score >= 500:
        return PolicyEvaluation(
            decision="REFER",
            reason_codes=["SCORE_IN_REVIEW_BAND"],
            policy_id=f"{segment}_v1",
            policy_version="1.0",
        ).model_dump()
    else:
        return PolicyEvaluation(
            decision="REJECT",
            reason_codes=["SCORE_BELOW_MINIMUM"],
            policy_id=f"{segment}_v1",
            policy_version="1.0",
        ).model_dump()
