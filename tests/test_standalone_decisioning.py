"""Tests for standalone credit decisioning engine."""

import pytest

from app.policy.standalone_decisioning import (
    CreditDecision,
    StandaloneDecisionEngine,
)


@pytest.fixture
def engine():
    return StandaloneDecisionEngine()


class TestApproveRejectRefer:
    def test_approve_high_score(self, engine):
        d = engine.decide("B001", "DAIRY_FARMER", score=750, confidence=0.8)
        assert d.decision == "APPROVE"
        assert d.approved_amount > 0
        assert not d.requires_human_review
        assert "SCORE_ABOVE_THRESHOLD" in d.reason_codes

    def test_reject_low_score(self, engine):
        d = engine.decide("B002", "DAIRY_FARMER", score=200, confidence=0.8)
        assert d.decision == "REJECT"
        assert d.approved_amount == 0
        assert "SCORE_BELOW_MINIMUM" in d.reason_codes

    def test_refer_mid_score(self, engine):
        d = engine.decide("B003", "DAIRY_FARMER", score=500, confidence=0.8)
        assert d.decision == "REFER"
        assert d.requires_human_review
        assert "SCORE_IN_REVIEW_BAND" in d.reason_codes

    def test_refer_low_confidence(self, engine):
        d = engine.decide("B004", "DAIRY_FARMER", score=700, confidence=0.3)
        assert d.decision == "REFER"
        assert "LOW_CONFIDENCE" in d.reason_codes


class TestFraudGate:
    def test_fraud_rejection(self, engine):
        d = engine.decide("B005", "DAIRY_FARMER", score=800, fraud_score=0.8)
        assert d.decision == "REJECT"
        assert "FRAUD_SCORE_EXCEEDED" in d.reason_codes
        assert d.approved_amount == 0

    def test_fraud_below_threshold(self, engine):
        d = engine.decide("B006", "DAIRY_FARMER", score=700, fraud_score=0.3)
        assert d.decision == "APPROVE"


class TestDTIGate:
    def test_dti_exceeded_downgrades(self, engine):
        d = engine.decide(
            "B007", "DAIRY_FARMER", score=700,
            monthly_income=20000, existing_obligations=12000,
        )
        assert d.decision == "REFER"
        assert "DTI_EXCEEDED" in d.reason_codes

    def test_dti_ok(self, engine):
        d = engine.decide(
            "B008", "DAIRY_FARMER", score=700,
            monthly_income=50000, existing_obligations=10000,
        )
        assert d.decision == "APPROVE"


class TestAmountCalibration:
    def test_amount_capped_at_segment_max(self, engine):
        d = engine.decide("B009", "STREET_VENDOR", score=700, requested_amount=500000)
        assert d.approved_amount <= 50000

    def test_low_score_reduces_amount(self, engine):
        high = engine.decide("B010", "DAIRY_FARMER", score=800, requested_amount=200000)
        low = engine.decide("B011", "DAIRY_FARMER", score=550, requested_amount=200000)
        assert high.approved_amount >= low.approved_amount


class TestRatePricing:
    def test_high_score_lower_rate(self, engine):
        d = engine.decide("B012", "DAIRY_FARMER", score=800)
        assert d.interest_rate == 13.0

    def test_low_score_higher_rate(self, engine):
        d = engine.decide("B013", "DAIRY_FARMER", score=550)
        assert d.interest_rate == 17.0


class TestMultipleSegments:
    @pytest.mark.parametrize("segment", [
        "DAIRY_FARMER", "STREET_VENDOR", "GIG_WORKER", "KIRANA_SHOP",
        "SHG_MEMBER", "FISHERY", "CONSTRUCTION_WORKER", "EV_FINANCING",
    ])
    def test_all_segments_produce_valid_decision(self, engine, segment):
        d = engine.decide("B100", segment, score=600)
        assert d.decision in ("APPROVE", "REJECT", "REFER")
        assert d.segment == segment
        assert d.decision_id
        assert d.timestamp

    def test_unknown_segment_uses_default(self, engine):
        d = engine.decide("B101", "UNKNOWN_SEGMENT", score=700)
        assert d.decision in ("APPROVE", "REJECT", "REFER")


class TestAuditTrail:
    def test_has_audit_trail(self, engine):
        d = engine.decide("B200", "DAIRY_FARMER", score=700)
        assert d.audit_trail["engine"] == "standalone"
        assert d.audit_trail["decision_id"] == d.decision_id
        assert "policy_thresholds" in d.audit_trail

    def test_to_dict(self, engine):
        d = engine.decide("B201", "DAIRY_FARMER", score=700)
        data = d.to_dict()
        assert data["decision"] == "APPROVE"
        assert "explanation" in data
        assert "primary_reason" in data["explanation"]


class TestShadowCompare:
    def test_matching_decisions(self, engine):
        local = engine.decide("B300", "DAIRY_FARMER", score=700)
        sentinel_mock = {"decision": "APPROVE", "score": 710, "approved_amount": 100000}
        result = engine.shadow_compare(local, sentinel_mock)
        assert result["match"] is True

    def test_divergent_decisions(self, engine):
        local = engine.decide("B301", "DAIRY_FARMER", score=500)
        sentinel_mock = {"decision": "APPROVE", "score": 650, "approved_amount": 100000}
        result = engine.shadow_compare(local, sentinel_mock)
        assert result["match"] is False
        assert result["local_decision"] == "REFER"
        assert result["sentinel_decision"] == "APPROVE"
