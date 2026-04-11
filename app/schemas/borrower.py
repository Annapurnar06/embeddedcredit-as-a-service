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


class WarehouseReceiptData(BaseModel):
    receipt_id: str
    warehouse_name: str
    commodity: str
    quantity_quintals: float
    quality_grade: str
    storage_date: date
    warehouse_grade: str
    estimated_value: Decimal
    insurance_active: bool = False


class GoldAppraisalData(BaseModel):
    appraisal_id: str
    gold_weight_grams: float
    purity_karats: float
    market_rate_per_gram: Decimal
    appraised_value: Decimal
    ornament_description: str
    hallmark_verified: bool = False


class EVTelematicsData(BaseModel):
    vehicle_id: str
    daily_km_avg: float
    battery_health_pct: float
    charging_regularity_pct: float
    total_trips_30d: int
    battery_cycles: int
    vehicle_model: str


class SolarGenerationData(BaseModel):
    installation_id: str
    capacity_kw: float
    avg_daily_generation_kwh: float
    grid_savings_monthly: Decimal
    panel_degradation_pct: float
    net_metering_active: bool = False
    installation_date: date | None = None


class SHGRecordsData(BaseModel):
    shg_name: str
    group_id: str
    member_count: int
    group_tenure_months: int
    meeting_attendance_pct: float
    group_repayment_rate: float
    individual_savings_regularity: float
    nrlm_grade: str | None = None


class VehicleTelematicsData(BaseModel):
    vehicle_id: str
    vehicle_type: str
    monthly_km_driven: float
    daily_trips_avg: int
    fuel_efficiency_kmpl: float | None = None
    fastag_trips_30d: int = 0
    load_utilization_pct: float | None = None
    idle_days_30d: int = 0


class PoultryIntegratorData(BaseModel):
    integrator_name: str
    farmer_id: str
    batch_count_12m: int
    avg_mortality_rate_pct: float
    feed_conversion_ratio: float
    avg_batch_revenue: Decimal
    integrator_tenure_months: int


class FisheryCooperativeData(BaseModel):
    cooperative_name: str
    member_id: str
    catch_regularity_pct: float
    avg_monthly_catch_kg: float
    catch_volume_trend: str
    vessel_owned: bool
    cooperative_tenure_months: int


class FPOEntityData(BaseModel):
    fpo_name: str
    registration_id: str
    member_count: int
    aggregation_volume_trend: str
    nabard_grade: str | None = None
    governance_score: float | None = None
    avg_monthly_turnover: Decimal


class UPITransactionData(BaseModel):
    merchant_id: str
    avg_daily_collections: Decimal
    collection_regularity_pct: float
    unique_customers_30d: int
    avg_transaction_value: Decimal
    peak_hour_collections_pct: float


class PropertyRecordsData(BaseModel):
    property_id: str
    clear_title: bool
    encumbrance_free: bool
    property_type: str
    area_sqft: float
    market_valuation: Decimal
    location_pin: str


class EdtechPlatformData(BaseModel):
    platform_name: str
    student_id: str
    course_name: str
    course_duration_months: int
    completion_rate_pct: float
    placement_rate_pct: float
    avg_placement_salary: Decimal | None = None


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
    warehouse_receipt: WarehouseReceiptData | None = None
    gold_appraisal: GoldAppraisalData | None = None
    ev_telematics: EVTelematicsData | None = None
    solar_generation: SolarGenerationData | None = None
    shg_records: SHGRecordsData | None = None
    vehicle_telematics: VehicleTelematicsData | None = None
    poultry_data: PoultryIntegratorData | None = None
    fishery_data: FisheryCooperativeData | None = None
    fpo_data: FPOEntityData | None = None
    upi_transactions: UPITransactionData | None = None
    property_records: PropertyRecordsData | None = None
    edtech_data: EdtechPlatformData | None = None
    cross_validation: CrossValidationResult | None = None
    confidence: ConfidenceScore | None = None
    segment: str | None = None
