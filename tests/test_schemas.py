from decimal import Decimal
from uuid import uuid4

from app.schemas.borrower import (
    AadhaarVerifyResult,
    BankAccountData,
    BorrowerProfile,
    BureauReport,
    ConfidenceScore,
    CooperativeData,
)
from app.schemas.loan import (
    ExplainabilityResult,
    LoanProduct,
    PolicyEvaluation,
    ScoreResult,
)


def test_aadhaar_verify_result():
    result = AadhaarVerifyResult(
        verified=True,
        name="Ramesh Patel",
        dob="1985-03-15",
        gender="M",
        address_state="Gujarat",
        address_district="Banaskantha",
        address_pincode="385001",
    )
    assert result.verified is True
    assert result.name == "Ramesh Patel"
    assert result.address_pincode == "385001"


def test_bureau_report():
    report = BureauReport(
        bureau="CIBIL",
        score=720,
        grade="B1",
        total_accounts=5,
        active_accounts=3,
        overdue_accounts=0,
        total_outstanding=Decimal("150000.00"),
        enquiry_count_6m=2,
        dpd_max_12m=0,
    )
    assert report.score == 720
    assert report.grade == "B1"
    assert len(report.flags) == 0


def test_cooperative_data():
    data = CooperativeData(
        cooperative_name="Banaskantha Dairy",
        membership_id="BD-2020-12345",
        membership_tenure_months=48,
        avg_daily_pouring_liters=12.5,
        avg_fat_percentage=6.2,
        pouring_regularity_pct=92.0,
        last_payment_amount=Decimal("15000.00"),
        payment_regularity_pct=95.0,
        total_payouts_6m=Decimal("90000.00"),
    )
    assert data.membership_tenure_months == 48
    assert data.pouring_regularity_pct == 92.0


def test_bank_account_data():
    data = BankAccountData(
        account_number_masked="XXXX1234",
        bank_name="SBI",
        months_available=12,
        avg_monthly_balance=Decimal("25000.00"),
        avg_monthly_inflow=Decimal("45000.00"),
        avg_monthly_outflow=Decimal("38000.00"),
        bounce_count=1,
        bounce_rate=0.02,
        salary_detected=False,
        estimated_monthly_income=Decimal("45000.00"),
        foir=0.35,
    )
    assert data.bank_name == "SBI"
    assert data.foir == 0.35


def test_borrower_profile():
    profile = BorrowerProfile(
        borrower_id=uuid4(),
        aadhaar_verified=True,
        pan_verified=True,
        bank_account_verified=True,
        segment="DAIRY_FARMER",
    )
    assert profile.aadhaar_verified is True
    assert profile.segment == "DAIRY_FARMER"
    assert profile.bureau_report is None


def test_score_result():
    result = ScoreResult(
        score=680,
        grade="B1",
        model_version="dairy_score_v1",
        feature_contributions={
            "pouring_regularity": 0.23,
            "bureau_score": 0.18,
            "bank_balance_stability": 0.15,
        },
    )
    assert result.score == 680
    assert result.grade == "B1"


def test_policy_evaluation():
    evaluation = PolicyEvaluation(
        decision="APPROVE",
        reason_codes=["SCORE_ABOVE_THRESHOLD", "ALL_REQUIRED_SOURCES"],
        policy_id="DAIRY_FARMER_v1",
        policy_version="1.0",
    )
    assert evaluation.decision == "APPROVE"
    assert len(evaluation.reason_codes) == 2


def test_loan_product():
    product = LoanProduct(
        amount=Decimal("100000.00"),
        interest_rate=Decimal("15.00"),
        tenure_months=18,
        schedule_type="SEASONAL_DYNAMIC",
        total_interest=Decimal("15000.00"),
        total_repayment=Decimal("115000.00"),
    )
    assert product.amount == Decimal("100000.00")
    assert product.schedule_type == "SEASONAL_DYNAMIC"


def test_confidence_score():
    confidence = ConfidenceScore(
        score=0.82,
        level="HIGH",
        sources_available=5,
        sources_required=3,
        freshness_score=0.9,
        validation_score=0.85,
        anomaly_free_score=1.0,
    )
    assert confidence.level == "HIGH"
    assert confidence.score == 0.82


def test_explainability_result():
    result = ExplainabilityResult(
        decision="REJECT",
        reason_codes=["LOW_BUREAU_SCORE", "HIGH_EXISTING_DEBT"],
        borrower_facing_reasons=[
            "Aapka credit score kam hai",
            "Aapka existing karz zyada hai",
        ],
        feature_importance={"bureau_score": 0.45, "existing_debt": 0.35},
    )
    assert result.decision == "REJECT"
    assert len(result.borrower_facing_reasons) == 2
