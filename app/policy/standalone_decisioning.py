"""Standalone credit decisioning engine — removes Finbox Sentinel MCP hard dependency.

Solves: Sentinel MCP has no public docs and requires enterprise onboarding.
This engine provides full credit decisioning locally: segment policy evaluation,
multi-factor scoring, fraud gating, DTI checks, amount calibration, and
explainability — all with audit trail. Falls back to Sentinel when available.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class DecisionExplanation:
    primary_reason: str
    contributing_factors: list[str] = field(default_factory=list)
    risk_factors: list[dict[str, Any]] = field(default_factory=list)
    feature_importance: dict[str, float] = field(default_factory=dict)


@dataclass
class CreditDecision:
    decision_id: str
    borrower_id: str
    segment: str
    decision: str  # APPROVE, REJECT, REFER
    score: int
    grade: str
    confidence: float
    approved_amount: float
    interest_rate: float
    reason_codes: list[str]
    explanation: DecisionExplanation
    requires_human_review: bool
    policy_version: str
    model_version: str
    timestamp: str
    audit_trail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "borrower_id": self.borrower_id,
            "segment": self.segment,
            "decision": self.decision,
            "score": self.score,
            "grade": self.grade,
            "confidence": self.confidence,
            "approved_amount": self.approved_amount,
            "interest_rate": self.interest_rate,
            "reason_codes": self.reason_codes,
            "requires_human_review": self.requires_human_review,
            "explanation": {
                "primary_reason": self.explanation.primary_reason,
                "contributing_factors": self.explanation.contributing_factors,
                "risk_factors": self.explanation.risk_factors,
                "feature_importance": self.explanation.feature_importance,
            },
            "policy_version": self.policy_version,
            "model_version": self.model_version,
            "timestamp": self.timestamp,
            "audit_trail": self.audit_trail,
        }


# Per-segment thresholds — extend easily by adding keys
SEGMENT_POLICY: dict[str, dict[str, Any]] = {
    "DAIRY_FARMER": {
        "auto_approve": 650, "auto_reject": 350, "max_amount": 200_000,
        "min_confidence": 0.55, "max_dti": 0.50, "fraud_threshold": 0.50,
        "rate_grid": [(750, 13.0), (650, 15.0), (550, 17.0), (0, 20.0)],
    },
    "STREET_VENDOR": {
        "auto_approve": 600, "auto_reject": 300, "max_amount": 50_000,
        "min_confidence": 0.50, "max_dti": 0.40, "fraud_threshold": 0.50,
        "rate_grid": [(750, 16.0), (650, 18.0), (550, 20.0), (0, 22.0)],
    },
    "GIG_WORKER": {
        "auto_approve": 620, "auto_reject": 320, "max_amount": 100_000,
        "min_confidence": 0.55, "max_dti": 0.45, "fraud_threshold": 0.50,
        "rate_grid": [(750, 14.0), (650, 16.0), (550, 18.0), (0, 22.0)],
    },
    "KIRANA_SHOP": {
        "auto_approve": 640, "auto_reject": 350, "max_amount": 300_000,
        "min_confidence": 0.60, "max_dti": 0.50, "fraud_threshold": 0.50,
        "rate_grid": [(750, 14.0), (650, 16.0), (550, 18.0), (0, 20.0)],
    },
    "SHG_MEMBER": {
        "auto_approve": 580, "auto_reject": 300, "max_amount": 50_000,
        "min_confidence": 0.50, "max_dti": 0.50, "fraud_threshold": 0.50,
        "rate_grid": [(750, 12.0), (650, 14.0), (550, 16.0), (0, 18.0)],
    },
    "FISHERY": {
        "auto_approve": 620, "auto_reject": 350, "max_amount": 300_000,
        "min_confidence": 0.55, "max_dti": 0.50, "fraud_threshold": 0.50,
        "rate_grid": [(750, 14.0), (650, 16.0), (550, 18.0), (0, 20.0)],
    },
    "CONSTRUCTION_WORKER": {
        "auto_approve": 600, "auto_reject": 300, "max_amount": 75_000,
        "min_confidence": 0.50, "max_dti": 0.45, "fraud_threshold": 0.50,
        "rate_grid": [(750, 16.0), (650, 18.0), (550, 20.0), (0, 24.0)],
    },
    "EV_FINANCING": {
        "auto_approve": 650, "auto_reject": 380, "max_amount": 500_000,
        "min_confidence": 0.60, "max_dti": 0.50, "fraud_threshold": 0.50,
        "rate_grid": [(750, 10.0), (650, 12.0), (550, 14.0), (0, 16.0)],
    },
}

DEFAULT_POLICY: dict[str, Any] = {
    "auto_approve": 650, "auto_reject": 350, "max_amount": 100_000,
    "min_confidence": 0.60, "max_dti": 0.50, "fraud_threshold": 0.50,
    "rate_grid": [(750, 14.0), (650, 16.0), (550, 18.0), (0, 22.0)],
}


class StandaloneDecisionEngine:
    """Full credit decisioning without Sentinel MCP dependency.

    Pipeline: fraud gate -> score gate -> confidence gate -> DTI gate ->
    amount calibration -> rate assignment -> explainability -> audit trail
    """

    def decide(
        self,
        borrower_id: str,
        segment: str,
        score: int,
        grade: str = "",
        confidence: float = 1.0,
        fraud_score: float = 0.0,
        requested_amount: float = 0.0,
        monthly_income: float = 0.0,
        existing_obligations: float = 0.0,
        feature_contributions: dict[str, float] | None = None,
    ) -> CreditDecision:
        decision_id = str(uuid.uuid4())
        policy = SEGMENT_POLICY.get(segment, DEFAULT_POLICY)
        reasons: list[str] = []
        risk_factors: list[dict[str, Any]] = []

        # Gate 1: Fraud
        if fraud_score > policy["fraud_threshold"]:
            return self._build(
                decision_id, borrower_id, segment, "REJECT", score, grade,
                confidence, 0, 0.0, ["FRAUD_SCORE_EXCEEDED"],
                DecisionExplanation(
                    primary_reason="FRAUD_SCORE_EXCEEDED",
                    risk_factors=[{"type": "fraud", "score": fraud_score}],
                ),
                policy,
            )

        # Gate 2: Score band
        if score >= policy["auto_approve"]:
            decision = "APPROVE"
            reasons.append("SCORE_ABOVE_THRESHOLD")
        elif score <= policy["auto_reject"]:
            return self._build(
                decision_id, borrower_id, segment, "REJECT", score, grade,
                confidence, 0, 0.0, ["SCORE_BELOW_MINIMUM"],
                DecisionExplanation(primary_reason="SCORE_BELOW_MINIMUM"),
                policy,
            )
        else:
            decision = "REFER"
            reasons.append("SCORE_IN_REVIEW_BAND")

        # Gate 3: Confidence
        if confidence < policy["min_confidence"]:
            if decision == "APPROVE":
                decision = "REFER"
            reasons.append("LOW_CONFIDENCE")
            risk_factors.append({"type": "low_confidence", "value": confidence})

        # Gate 4: DTI
        if monthly_income > 0 and existing_obligations > 0:
            dti = existing_obligations / monthly_income
            if dti > policy["max_dti"]:
                if decision == "APPROVE":
                    decision = "REFER"
                reasons.append("DTI_EXCEEDED")
                risk_factors.append({"type": "high_dti", "ratio": round(dti, 2)})

        # Amount calibration
        max_amt = policy["max_amount"]
        amount = min(requested_amount or max_amt, max_amt)
        score_ratio = max(0.0, min(score / 900, 1.0))
        if score_ratio < 0.70:
            amount = min(amount, max_amt * score_ratio)
        if decision == "REJECT":
            amount = 0

        # Rate assignment
        rate = self._lookup_rate(score, policy["rate_grid"])

        # Explainability
        explanation = DecisionExplanation(
            primary_reason=reasons[0] if reasons else "UNKNOWN",
            contributing_factors=reasons,
            risk_factors=risk_factors,
            feature_importance=feature_contributions or {},
        )

        return self._build(
            decision_id, borrower_id, segment, decision, score, grade,
            confidence, amount, rate, reasons, explanation, policy,
        )

    def shadow_compare(
        self,
        local_decision: CreditDecision,
        sentinel_decision: dict[str, Any],
    ) -> dict[str, Any]:
        """Compare local engine vs Sentinel for shadow testing."""
        sentinel_dec = sentinel_decision.get("decision", "")
        match = local_decision.decision == sentinel_dec
        return {
            "local_decision": local_decision.decision,
            "sentinel_decision": sentinel_dec,
            "match": match,
            "local_score": local_decision.score,
            "sentinel_score": sentinel_decision.get("score", 0),
            "local_amount": local_decision.approved_amount,
            "sentinel_amount": sentinel_decision.get("approved_amount", 0),
        }

    @staticmethod
    def _lookup_rate(score: int, grid: list[tuple[int, float]]) -> float:
        for threshold, rate in grid:
            if score >= threshold:
                return rate
        return grid[-1][1] if grid else 18.0

    @staticmethod
    def _build(
        decision_id: str,
        borrower_id: str,
        segment: str,
        decision: str,
        score: int,
        grade: str,
        confidence: float,
        amount: float,
        rate: float,
        reasons: list[str],
        explanation: DecisionExplanation,
        policy: dict[str, Any],
    ) -> CreditDecision:
        now = datetime.now(timezone.utc).isoformat()
        return CreditDecision(
            decision_id=decision_id,
            borrower_id=borrower_id,
            segment=segment,
            decision=decision,
            score=score,
            grade=grade or ("A1" if score >= 750 else "A2" if score >= 650 else "B1" if score >= 550 else "B2" if score >= 450 else "C"),
            confidence=confidence,
            approved_amount=round(amount, 2),
            interest_rate=rate,
            reason_codes=reasons,
            explanation=explanation,
            requires_human_review=decision == "REFER",
            policy_version=f"{segment}_standalone_v1",
            model_version=f"{segment.lower()}_score_v1",
            timestamp=now,
            audit_trail={
                "decision_id": decision_id,
                "engine": "standalone",
                "timestamp": now,
                "policy_thresholds": {
                    "auto_approve": policy["auto_approve"],
                    "auto_reject": policy["auto_reject"],
                    "max_amount": policy["max_amount"],
                },
            },
        )
