from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AadhaarVerifyResult(BaseModel):
    verified: bool
    name: str | None = None
    dob: str | None = None
    gender: str | None = None
    address_state: str | None = None
    address_district: str | None = None
    address_pincode: str | None = None
    photo_hash: str | None = None


class PanVerifyResult(BaseModel):
    valid: bool
    name: str | None = None
    name_match_score: float = 0.0
    pan_status: str | None = None


class BankAccountVerifyResult(BaseModel):
    account_valid: bool
    name_on_account: str | None = None
    name_match_score: float = 0.0
    ifsc: str | None = None
    bank_name: str | None = None


class NegativeListResult(BaseModel):
    clear: bool
    flags: list[str] = Field(default_factory=list)
    sources_checked: list[str] = Field(default_factory=list)


class AAConsentResult(BaseModel):
    consent_id: str
    consent_url: str
    status: str
    expires_at: datetime


class BureauReport(BaseModel):
    bureau: str
    score: int | None = None
    grade: str | None = None
    total_accounts: int = 0
    active_accounts: int = 0
    overdue_accounts: int = 0
    total_outstanding: Decimal = Decimal("0")
    enquiry_count_6m: int = 0
    dpd_max_12m: int = 0
    flags: list[str] = Field(default_factory=list)


class BankAccountData(BaseModel):
    account_number_masked: str
    bank_name: str
    months_available: int
    avg_monthly_balance: Decimal
    avg_monthly_inflow: Decimal
    avg_monthly_outflow: Decimal
    bounce_count: int = 0
    bounce_rate: float = 0.0
    salary_detected: bool = False
    estimated_monthly_income: Decimal | None = None
    foir: float | None = None
    transaction_categories: dict[str, Decimal] = Field(default_factory=dict)


class CooperativeData(BaseModel):
    cooperative_name: str
    membership_id: str
    membership_tenure_months: int
    avg_daily_pouring_liters: float
    avg_fat_percentage: float
    pouring_regularity_pct: float
    last_payment_amount: Decimal
    payment_regularity_pct: float
    total_payouts_6m: Decimal


class PlatformEarnings(BaseModel):
    platform: str
    active_months: int
    avg_monthly_earnings: Decimal
    avg_monthly_deliveries: int
    avg_rating: float
    active_days_pct: float


class GSTData(BaseModel):
    gstin: str
    business_name: str
    filing_regularity_pct: float
    avg_monthly_turnover: Decimal
    turnover_trend: str
    last_filing_date: date | None = None


class DeviceScore(BaseModel):
    score: int = Field(ge=0, le=1000)
    confidence: float


class ULIData(BaseModel):
    land_records: dict | None = None
    satellite_ndvi: dict | None = None
    weather_imd: dict | None = None
    pmfby_coverage: dict | None = None


class CrossValidationResult(BaseModel):
    consistent: bool
    income_delta_pct: float | None = None
    name_consistency: float
    address_consistency: float
    anomalies: list[str] = Field(default_factory=list)


class ConfidenceScore(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    level: str
    sources_available: int
    sources_required: int
    freshness_score: float
    validation_score: float
    anomaly_free_score: float


class BorrowerProfile(BaseModel):
    borrower_id: UUID
    aadhaar_verified: bool = False
    pan_verified: bool = False
    bank_account_verified: bool = False
    bureau_report: BureauReport | None = None
    bank_data: BankAccountData | None = None
    cooperative_data: CooperativeData | None = None
    platform_earnings: PlatformEarnings | None = None
    gst_data: GSTData | None = None
    device_score: DeviceScore | None = None
    uli_data: ULIData | None = None
    cross_validation: CrossValidationResult | None = None
    confidence: ConfidenceScore | None = None
    segment: str | None = None
