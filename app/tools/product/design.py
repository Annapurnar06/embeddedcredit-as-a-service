"""Dynamic product design based on approved decision + borrower profile."""

from __future__ import annotations

from decimal import Decimal

from app.schemas.loan import LoanProduct
from app.tools.registry import ToolCategory, lending_tool

MORATORIUM_TRIGGERS: dict[str, list[dict]] = {
    "DAIRY_FARMER": [
        {"type": "WEATHER_HEAT", "threshold_celsius": 38, "duration_months": 1},
        {"type": "PRODUCTION_DROP", "threshold_percent": 40, "duration_months": 1},
    ],
    "WAREHOUSE_RECEIPT": [
        {"type": "COMMODITY_PRICE_CRASH", "threshold_percent": 30, "intervention": "LTV_REVIEW"},
    ],
    "EV_FINANCING": [
        {"type": "BATTERY_FAILURE", "threshold": "detected", "duration_months": 1},
        {"type": "PLATFORM_DEACTIVATION", "threshold": 1, "duration_months": 1},
    ],
    "SOLAR_FINANCING": [
        {"type": "MONSOON_LOW_GENERATION", "threshold_pct": 40, "duration_months": 2},
    ],
    "SHG_MEMBER": [
        {"type": "NATURAL_DISASTER", "threshold": "declared", "duration_months": 3},
    ],
    "POULTRY_FARMER": [
        {"type": "DISEASE_OUTBREAK", "threshold": "declared", "duration_months": 2},
        {"type": "FEED_PRICE_SPIKE", "threshold_percent": 40, "duration_months": 1},
    ],
    "FISHERY": [
        {"type": "FISHING_BAN", "threshold": "declared", "duration_months": 2},
        {"type": "CYCLONE_WARNING", "threshold": "declared", "duration_months": 1},
    ],
    "SUGARCANE_FARMER": [
        {"type": "DROUGHT", "threshold": "declared", "duration_months": 3},
        {"type": "MILL_PAYMENT_DELAY", "threshold_days": 60, "duration_months": 2},
    ],
    "VEGETABLE_GROWER": [
        {"type": "UNSEASONAL_RAIN", "threshold": "declared", "duration_months": 1},
        {"type": "PEST_OUTBREAK", "threshold": "declared", "duration_months": 1},
    ],
    "COTTON_FARMER": [
        {"type": "BOLLWORM_OUTBREAK", "threshold": "declared", "duration_months": 2},
        {"type": "DROUGHT", "threshold": "declared", "duration_months": 3},
    ],
    "CONSTRUCTION_WORKER": [
        {"type": "MONSOON_WORK_STOPPAGE", "threshold": "heavy_rain", "duration_months": 1},
    ],
    "STREET_VENDOR": [
        {"type": "MUNICIPAL_EVICTION", "threshold": "declared", "duration_months": 1},
    ],
    "TRUCK_OPERATOR": [
        {"type": "VEHICLE_BREAKDOWN", "threshold": "detected", "duration_months": 1},
    ],
    "AUTO_RICKSHAW": [
        {"type": "VEHICLE_BREAKDOWN", "threshold": "detected", "duration_months": 1},
    ],
    "E_RICKSHAW": [
        {"type": "BATTERY_FAILURE", "threshold": "detected", "duration_months": 1},
    ],
    "CAB_DRIVER": [
        {"type": "VEHICLE_BREAKDOWN", "threshold": "detected", "duration_months": 1},
    ],
    "MICRO_HOUSING": [
        {"type": "NATURAL_DISASTER", "threshold": "declared", "duration_months": 3},
    ],
    "EDTECH_STUDENT": [
        {"type": "COURSE_IN_PROGRESS", "threshold": "active", "duration_months": 6},
    ],
}


def _moratorium_triggers(segment: str) -> list[dict]:
    return MORATORIUM_TRIGGERS.get(segment, [])


@lending_tool(
    name="design_dynamic_product",
    description="Design loan product: amount, rate, tenure, schedule type, insurance",
    category=ToolCategory.PRODUCT,
    timeout_seconds=5,
)
async def design_dynamic_product(
    segment: str = "DAIRY_FARMER",
    score: int = 650,
    interest_rate: float = 15.0,
    requested_amount: float = 100000,
    monthly_income: float = 42000,
) -> dict:
    max_emi = monthly_income * 0.4

    schedule_map = {
        "DAIRY_FARMER": ("SEASONAL_DYNAMIC", 18, "PASHU_BIMA"),
        "KIRANA_SHOP": ("DAILY_MICRO", 12, None),
        "GIG_WORKER": ("PAYOUT_LINKED", 12, None),
        "WAREHOUSE_RECEIPT": ("BULLET_AT_HARVEST", 9, "COMMODITY_INSURANCE"),
        "GOLD_LOAN": ("BULLET_OR_MONTHLY_INTEREST", 12, None),
        "EV_FINANCING": ("DAILY_PAYOUT_LINKED", 36, "EV_COMPREHENSIVE"),
        "SOLAR_FINANCING": ("SAVINGS_LINKED_MONTHLY", 60, "SOLAR_PANEL_WARRANTY"),
        "SHG_MEMBER": ("MONTHLY_GROUP", 18, None),
        "TRADER_AGRI": ("SEASONAL_BULLET", 9, None),
        "MSE_MANUFACTURING": ("MONTHLY_EMI", 48, "MACHINERY_INSURANCE"),
        "STREET_VENDOR": ("DAILY_UPI", 9, None),
        "STUDENT_HOUSING": ("SEMESTER_ALIGNED", 36, None),
        "TRUCK_OPERATOR": ("MONTHLY_EMI", 48, "CV_COMPREHENSIVE"),
        "AUTO_RICKSHAW": ("DAILY_PAYOUT_LINKED", 36, "THREE_WHEELER_COMPREHENSIVE"),
        "BEAUTY_SALON": ("DAILY_UPI", 18, None),
        "DHABA_RESTAURANT": ("DAILY_UPI", 12, None),
        "POULTRY_FARMER": ("BATCH_CYCLE", 6, "POULTRY_MORTALITY_COVER"),
        "FISHERY": ("SEASONAL_CATCH", 12, "VESSEL_INSURANCE"),
        "HANDLOOM_WEAVER": ("ORDER_CYCLE", 12, None),
        "TAILORING_UNIT": ("DAILY_UPI", 12, None),
        "MEDICAL_SHOP": ("MONTHLY_EMI", 18, None),
        "SUGARCANE_FARMER": ("HARVEST_LINKED", 12, "PMFBY"),
        "VEGETABLE_GROWER": ("CROP_CYCLE", 6, "PMFBY"),
        "FPO_ENTITY": ("SEASONAL_BULLET", 12, None),
        "NBFC_BC": ("DAILY_SETTLEMENT", 9, None),
        "CONSTRUCTION_WORKER": ("WEEKLY", 9, None),
        "DOMESTIC_WORKER": ("WEEKLY", 9, None),
        "E_RICKSHAW": ("DAILY_PAYOUT_LINKED", 24, "EV_COMPREHENSIVE"),
        "MICRO_HOUSING": ("MONTHLY_EMI", 84, "HOME_INSURANCE"),
        "DAIRY_PROCESSOR": ("MONTHLY_EMI", 18, "COLD_CHAIN_INSURANCE"),
        "AGRI_INPUT_DEALER": ("SEASONAL_BULLET", 6, None),
        "RENTAL_INCOME": ("MONTHLY_EMI", 48, None),
        "COTTON_FARMER": ("HARVEST_LINKED", 9, "PMFBY"),
        "RICE_MILLER": ("SEASONAL_BULLET", 6, "STOCK_INSURANCE"),
        "EDTECH_STUDENT": ("ISA_POST_PLACEMENT", 24, None),
        "HEALTH_CLINIC": ("MONTHLY_EMI", 36, "EQUIPMENT_INSURANCE"),
        "MICRO_CONTRACTOR": ("MILESTONE_LINKED", 18, None),
        "CAB_DRIVER": ("DAILY_PAYOUT_LINKED", 36, "MOTOR_COMPREHENSIVE"),
    }
    schedule_type, default_tenure, insurance = schedule_map.get(segment, ("EMI", 12, None))

    amount = Decimal(str(min(requested_amount, max_emi * default_tenure * 0.8)))
    total_interest = amount * Decimal(str(interest_rate / 100)) * Decimal(str(default_tenure / 12))
    total_repayment = amount + total_interest
    processing_fee = amount * Decimal("0.02")

    return LoanProduct(
        amount=amount.quantize(Decimal("0.01")),
        interest_rate=Decimal(str(interest_rate)),
        tenure_months=default_tenure,
        schedule_type=schedule_type,
        insurance_type=insurance,
        insurance_premium=Decimal("1500.00") if insurance else None,
        processing_fee=processing_fee.quantize(Decimal("0.01")),
        total_interest=total_interest.quantize(Decimal("0.01")),
        total_repayment=total_repayment.quantize(Decimal("0.01")),
        moratorium_triggers=_moratorium_triggers(segment),
    ).model_dump()
