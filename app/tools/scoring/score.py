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
    "WAREHOUSE_RECEIPT": {
        "commodity_value_stability": 0.20,
        "warehouse_grade": 0.15,
        "storage_duration": 0.10,
        "commodity_liquidity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.15,
        "past_repayment_history": 0.10,
    },
    "GOLD_LOAN": {
        "gold_purity": 0.25,
        "gold_weight_grams": 0.20,
        "market_gold_price": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.15,
        "past_gold_loan_history": 0.10,
    },
    "EV_FINANCING": {
        "daily_km_driven": 0.20,
        "battery_health_pct": 0.15,
        "charging_regularity": 0.10,
        "platform_earnings_trend": 0.15,
        "bureau_score": 0.20,
        "bank_stability": 0.20,
    },
    "SOLAR_FINANCING": {
        "solar_generation_kwh": 0.20,
        "grid_savings_monthly": 0.15,
        "installation_capacity_kw": 0.10,
        "panel_degradation_rate": 0.10,
        "net_metering_active": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "SHG_MEMBER": {
        "group_repayment_rate": 0.25,
        "group_meeting_attendance": 0.15,
        "individual_savings_regularity": 0.15,
        "group_tenure_months": 0.10,
        "nrlm_grading": 0.10,
        "bureau_score": 0.10,
        "bank_stability": 0.15,
    },
    "TRADER_AGRI": {
        "mandi_turnover_trend": 0.25,
        "gst_filing_regularity": 0.15,
        "commodity_diversification": 0.10,
        "trading_tenure_years": 0.10,
        "bureau_score": 0.20,
        "bank_stability": 0.20,
    },
    "MSE_MANUFACTURING": {
        "gst_turnover_trend": 0.20,
        "power_consumption_trend": 0.15,
        "udyam_registration_vintage": 0.10,
        "gst_filing_regularity": 0.10,
        "bank_inflow_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.15,
    },
    "STREET_VENDOR": {
        "upi_daily_collections": 0.25,
        "upi_collection_regularity": 0.15,
        "svep_vintage_months": 0.10,
        "location_stability": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "STUDENT_HOUSING": {
        "university_tier": 0.20,
        "course_completion_likelihood": 0.15,
        "scholarship_coverage_pct": 0.15,
        "parent_income_stability": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "TRUCK_OPERATOR": {
        "monthly_km_driven": 0.20,
        "fastag_trip_regularity": 0.15,
        "fuel_efficiency": 0.10,
        "load_utilization_pct": 0.10,
        "platform_earnings_trend": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "AUTO_RICKSHAW": {
        "daily_trips": 0.20,
        "daily_km_driven": 0.15,
        "upi_daily_collections": 0.15,
        "platform_rating": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "BEAUTY_SALON": {
        "upi_daily_collections": 0.25,
        "booking_regularity": 0.15,
        "customer_retention_rate": 0.10,
        "gst_turnover_trend": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "DHABA_RESTAURANT": {
        "upi_daily_collections": 0.25,
        "aggregator_orders_trend": 0.15,
        "fssai_compliance": 0.05,
        "bank_inflow_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "POULTRY_FARMER": {
        "batch_mortality_rate": 0.20,
        "feed_conversion_ratio": 0.15,
        "integrator_tenure_months": 0.10,
        "batch_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "FISHERY": {
        "catch_regularity": 0.20,
        "catch_volume_trend": 0.15,
        "cooperative_tenure": 0.10,
        "vessel_ownership": 0.10,
        "weather_risk_score": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "HANDLOOM_WEAVER": {
        "production_regularity": 0.20,
        "order_pipeline_value": 0.15,
        "cooperative_tenure": 0.10,
        "ecommerce_sales_trend": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "TAILORING_UNIT": {
        "upi_daily_collections": 0.25,
        "seasonal_demand_index": 0.10,
        "ecommerce_order_trend": 0.15,
        "customer_repeat_rate": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "MEDICAL_SHOP": {
        "gst_turnover_trend": 0.20,
        "drug_license_validity": 0.10,
        "distributor_credit_terms": 0.10,
        "bank_inflow_regularity": 0.15,
        "gst_filing_regularity": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "SUGARCANE_FARMER": {
        "supply_regularity": 0.20,
        "sugarcane_yield_trend": 0.15,
        "mill_payment_regularity": 0.15,
        "land_area_acres": 0.10,
        "ndvi_crop_health": 0.05,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "VEGETABLE_GROWER": {
        "fpo_supply_regularity": 0.20,
        "mandi_price_realization": 0.15,
        "crop_diversification": 0.10,
        "land_area_acres": 0.10,
        "ndvi_crop_health": 0.05,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "FPO_ENTITY": {
        "member_count": 0.10,
        "aggregation_volume_trend": 0.20,
        "gst_turnover_trend": 0.15,
        "nabard_grading": 0.10,
        "governance_score": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "NBFC_BC": {
        "transaction_volume_trend": 0.25,
        "active_customers": 0.15,
        "bc_tenure_months": 0.10,
        "commission_regularity": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "CONSTRUCTION_WORKER": {
        "epfo_contribution_regularity": 0.20,
        "employer_stability": 0.15,
        "bocw_registration_active": 0.10,
        "upi_inflow_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "DOMESTIC_WORKER": {
        "employer_count": 0.15,
        "employment_tenure_months": 0.15,
        "upi_inflow_regularity": 0.15,
        "monthly_income_estimate": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "E_RICKSHAW": {
        "daily_trips": 0.20,
        "battery_health_pct": 0.15,
        "upi_daily_collections": 0.20,
        "route_consistency": 0.05,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "MICRO_HOUSING": {
        "property_clear_title": 0.15,
        "property_valuation": 0.15,
        "income_stability": 0.20,
        "existing_rent_payment": 0.10,
        "bureau_score": 0.20,
        "bank_stability": 0.20,
    },
    "DAIRY_PROCESSOR": {
        "gst_turnover_trend": 0.20,
        "fssai_compliance": 0.10,
        "procurement_volume_trend": 0.15,
        "buyer_diversification": 0.10,
        "cold_chain_capacity": 0.05,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "AGRI_INPUT_DEALER": {
        "gst_turnover_trend": 0.20,
        "seasonal_inventory_pattern": 0.10,
        "fertilizer_license_active": 0.10,
        "distributor_credit_limit": 0.10,
        "bank_inflow_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.20,
    },
    "RENTAL_INCOME": {
        "rental_income_regularity": 0.25,
        "property_count": 0.10,
        "occupancy_rate": 0.15,
        "rental_yield_pct": 0.10,
        "bureau_score": 0.20,
        "bank_stability": 0.20,
    },
    "COTTON_FARMER": {
        "cotton_yield_trend": 0.20,
        "sale_regularity": 0.15,
        "land_area_acres": 0.10,
        "msp_utilization": 0.10,
        "ndvi_crop_health": 0.05,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "RICE_MILLER": {
        "milling_capacity_utilization": 0.15,
        "gst_turnover_trend": 0.20,
        "procurement_regularity": 0.15,
        "warehouse_stock_turnover": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "EDTECH_STUDENT": {
        "course_completion_rate": 0.20,
        "placement_track_record": 0.20,
        "course_value_index": 0.10,
        "student_engagement_score": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "HEALTH_CLINIC": {
        "patient_footfall_trend": 0.20,
        "medical_license_validity": 0.10,
        "gst_turnover_trend": 0.15,
        "bank_inflow_regularity": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "MICRO_CONTRACTOR": {
        "work_order_pipeline": 0.20,
        "gem_portal_rating": 0.10,
        "gst_turnover_trend": 0.15,
        "project_completion_rate": 0.15,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
    },
    "CAB_DRIVER": {
        "platform_earnings_trend": 0.25,
        "platform_rating": 0.10,
        "active_days_pct": 0.15,
        "daily_trips_avg": 0.10,
        "bureau_score": 0.15,
        "bank_stability": 0.25,
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
