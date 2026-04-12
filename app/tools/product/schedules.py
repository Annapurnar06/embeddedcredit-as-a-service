"""EMI schedule generators for different segment types."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from app.schemas.loan import EMIScheduleEntry
from app.tools.registry import ToolCategory, lending_tool

FLUSH_MONTHS = {10, 11, 12, 1, 2}
LEAN_MONTHS = {4, 5, 6}


@lending_tool(
    name="generate_seasonal_schedule",
    description="Generate seasonal EMI schedule for dairy/agriculture",
    category=ToolCategory.PRODUCT,
    timeout_seconds=3,
)
async def generate_seasonal_schedule(
    amount: float = 100000,
    rate: float = 15.0,
    tenure_months: int = 18,
    start_date: str = "2026-05-01",
) -> dict:
    total = Decimal(str(amount))
    monthly_rate = Decimal(str(rate / 1200))
    total_interest = total * monthly_rate * tenure_months
    total_repayment = total + total_interest
    avg_emi = total_repayment / tenure_months

    schedule = []
    balance = total
    start = date.fromisoformat(start_date)

    for i in range(tenure_months):
        due = start + timedelta(days=30 * (i + 1))
        month_num = due.month

        if month_num in FLUSH_MONTHS:
            emi = avg_emi * Decimal("1.3")
            season = "flush"
        elif month_num in LEAN_MONTHS:
            emi = avg_emi * Decimal("0.6")
            season = "lean"
        else:
            emi = avg_emi
            season = "transition"

        interest = balance * monthly_rate
        principal = emi - interest
        if principal > balance:
            principal = balance
            emi = principal + interest
        balance -= principal

        schedule.append(
            EMIScheduleEntry(
                month=i + 1,
                due_date=due,
                principal=principal.quantize(Decimal("0.01")),
                interest=interest.quantize(Decimal("0.01")),
                emi_amount=emi.quantize(Decimal("0.01")),
                outstanding_balance=max(Decimal("0"), balance).quantize(Decimal("0.01")),
                season=season,
            ).model_dump()
        )

    return {"schedule_type": "SEASONAL_DYNAMIC", "entries": schedule}


@lending_tool(
    name="generate_daily_micro_schedule",
    description="Generate daily micro-repayment schedule for kirana/gig",
    category=ToolCategory.PRODUCT,
    timeout_seconds=3,
)
async def generate_daily_micro_schedule(
    amount: float = 100000,
    rate: float = 16.0,
    tenure_months: int = 12,
) -> dict:
    total = Decimal(str(amount))
    total_interest = total * Decimal(str(rate / 100)) * Decimal(str(tenure_months / 12))
    total_repayment = total + total_interest
    tenure_days = tenure_months * 26
    daily_amount = total_repayment / tenure_days

    return {
        "schedule_type": "DAILY_MICRO",
        "daily_amount": str(daily_amount.quantize(Decimal("0.01"))),
        "working_days_per_month": 26,
        "tenure_days": tenure_days,
        "total_repayment": str(total_repayment.quantize(Decimal("0.01"))),
        "skip_days": ["sunday"],
    }


@lending_tool(
    name="generate_payout_linked_schedule",
    description="Generate platform payout-linked schedule for gig workers",
    category=ToolCategory.PRODUCT,
    timeout_seconds=3,
)
async def generate_payout_linked_schedule(
    amount: float = 100000,
    rate: float = 16.0,
    tenure_months: int = 12,
    avg_monthly_payout: float = 22000,
    deduction_rate: float = 0.15,
) -> dict:
    deduction = Decimal(str(avg_monthly_payout * deduction_rate))
    total = Decimal(str(amount))
    total_interest = total * Decimal(str(rate / 100))
    total_repayment = total + total_interest
    est_months = int(total_repayment / deduction) + 1

    return {
        "schedule_type": "PAYOUT_LINKED",
        "deduction_rate": deduction_rate,
        "avg_deduction_per_payout": str(deduction.quantize(Decimal("0.01"))),
        "estimated_tenure_months": est_months,
        "total_repayment": str(total_repayment.quantize(Decimal("0.01"))),
    }
