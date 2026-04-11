from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ScoreResult(BaseModel):
    score: int = Field(ge=0, le=900)
    grade: str
    model_version: str
    feature_contributions: dict[str, float] = Field(default_factory=dict)


class PolicyEvaluation(BaseModel):
    decision: str  # APPROVE, REFER, REJECT
    reason_codes: list[str] = Field(default_factory=list)
    policy_id: str
    policy_version: str
    overrides_applied: list[str] = Field(default_factory=list)


class RiskPricing(BaseModel):
    interest_rate: Decimal
    rate_band: str
    risk_premium: Decimal
    base_rate: Decimal


class FraudCheckResult(BaseModel):
    result: str  # PASS, HOLD, REJECT
    flags: list[str] = Field(default_factory=list)
    velocity_check: bool = True
    device_check: bool = True
    reference_check: bool = True


class PSLClassification(BaseModel):
    category: str
    sub_category: str | None = None
    eligible: bool
    reason: str


class ExplainabilityResult(BaseModel):
    decision: str
    reason_codes: list[str]
    borrower_facing_reasons: list[str]
    feature_importance: dict[str, float] = Field(default_factory=dict)


class CreditAssessmentMemo(BaseModel):
    loan_application_id: UUID
    borrower_summary: str
    financial_summary: str
    scoring_breakdown: str
    fraud_check_summary: str
    compliance_status: str
    recommendation: str
    generated_at: str


class EMIScheduleEntry(BaseModel):
    month: int
    due_date: date
    principal: Decimal
    interest: Decimal
    emi_amount: Decimal
    outstanding_balance: Decimal
    season: str | None = None
    is_moratorium: bool = False


class LoanProduct(BaseModel):
    amount: Decimal
    interest_rate: Decimal
    tenure_months: int
    schedule_type: str
    schedule: list[EMIScheduleEntry] = Field(default_factory=list)
    insurance_premium: Decimal | None = None
    insurance_type: str | None = None
    moratorium_triggers: list[dict] = Field(default_factory=list)
    processing_fee: Decimal = Decimal("0")
    total_interest: Decimal = Decimal("0")
    total_repayment: Decimal = Decimal("0")


class KeyFactStatement(BaseModel):
    loan_application_id: UUID
    borrower_name: str
    lender_name: str
    loan_amount: Decimal
    interest_rate: Decimal
    tenure_months: int
    emi_amount: Decimal
    total_interest: Decimal
    total_repayment: Decimal
    processing_fee: Decimal
    insurance_premium: Decimal | None = None
    annual_percentage_rate: Decimal
    cooling_off_period_days: int
    grievance_officer_name: str
    grievance_officer_contact: str
    generated_at: str


class DisbursementResult(BaseModel):
    reference_id: str
    status: str
    amount: Decimal
    mode: str
    beneficiary_account_masked: str
    timestamp: str


class WhatIfResult(BaseModel):
    parameter_changes: dict[str, str]
    projected_approval_rate: float
    projected_npa_rate: float
    projected_portfolio_size: int
    comparison_with_current: dict[str, str]
