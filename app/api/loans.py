from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.loan import LoanApplication

router = APIRouter(prefix="/api/loans", tags=["loans"])


@router.get("/{loan_id}")
async def get_loan(loan_id: UUID, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(LoanApplication).where(LoanApplication.id == loan_id))
    loan = result.scalar_one_or_none()
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {
        "id": str(loan.id),
        "borrower_id": str(loan.borrower_id),
        "lender_id": loan.lender_id,
        "segment": loan.segment,
        "status": loan.status.value,
        "amount": str(loan.amount) if loan.amount else None,
        "interest_rate": str(loan.interest_rate) if loan.interest_rate else None,
        "tenure_months": loan.tenure_months,
        "score": loan.score,
        "score_grade": loan.score_grade,
        "decision": loan.decision,
        "created_at": loan.created_at.isoformat(),
    }


@router.get("/")
async def list_loans(
    lender_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> dict:
    query = select(LoanApplication).limit(limit).order_by(LoanApplication.created_at.desc())
    if lender_id:
        query = query.where(LoanApplication.lender_id == lender_id)
    if status:
        query = query.where(LoanApplication.status == status)
    result = await db.execute(query)
    loans = result.scalars().all()
    return {
        "count": len(loans),
        "loans": [
            {
                "id": str(loan.id),
                "borrower_id": str(loan.borrower_id),
                "segment": loan.segment,
                "status": loan.status.value,
                "amount": str(loan.amount) if loan.amount else None,
                "created_at": loan.created_at.isoformat(),
            }
            for loan in loans
        ],
    }
