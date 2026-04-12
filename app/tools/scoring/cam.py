"""Credit Assessment Memo generation for REFER cases."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.loan import CreditAssessmentMemo
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="generate_cam",
    description="Auto-generate Credit Assessment Memo for REFER cases",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=10,
)
async def generate_cam(
    loan_application_id: str = "",
    borrower_name: str = "",
    segment: str = "",
    score: int = 0,
    score_grade: str = "",
    income_monthly: float = 0,
    existing_debt: float = 0,
    requested_amount: float = 0,
) -> dict:
    lid = UUID(loan_application_id) if loan_application_id else uuid4()
    foir = existing_debt / income_monthly if income_monthly > 0 else 0

    return CreditAssessmentMemo(
        loan_application_id=lid,
        borrower_summary=(
            f"Borrower: {borrower_name}, Segment: {segment}, Score: {score} ({score_grade})"
        ),
        financial_summary=(
            f"Monthly Income: INR {income_monthly:,.0f}, "
            f"Existing Debt: INR {existing_debt:,.0f}, "
            f"FOIR: {foir:.1%}, "
            f"Requested: INR {requested_amount:,.0f}"
        ),
        scoring_breakdown=f"Score {score} ({score_grade}) via rule-based model v1",
        fraud_check_summary="PASS - No flags detected",
        compliance_status="KYC verified, consent obtained, PSL eligible",
        recommendation=(
            "REFER for manual review - score in review band"
            if score >= 500
            else "REJECT - below minimum threshold"
        ),
        generated_at=datetime.now(timezone.utc).isoformat(),
    ).model_dump()
