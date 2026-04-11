import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LoanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    DATA_ASSEMBLY = "DATA_ASSEMBLY"
    SCORING = "SCORING"
    APPROVED = "APPROVED"
    REFERRED = "REFERRED"
    REJECTED = "REJECTED"
    OFFER_PRESENTED = "OFFER_PRESENTED"
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    KFS_GENERATED = "KFS_GENERATED"
    ESIGNED = "ESIGNED"
    DISBURSED = "DISBURSED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    NPA = "NPA"
    WRITTEN_OFF = "WRITTEN_OFF"


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    borrower_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("borrowers.id"), index=True
    )
    lender_id: Mapped[str] = mapped_column(String(50), index=True)
    segment: Mapped[str] = mapped_column(String(50))
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus), default=LoanStatus.DRAFT, index=True
    )
    amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    interest_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    tenure_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    schedule_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score_grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    decision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    decision_reason_codes: Mapped[str | None] = mapped_column(Text, nullable=True)
    psl_category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    kfs_generated: Mapped[bool] = mapped_column(default=False)
    esigned: Mapped[bool] = mapped_column(default=False)
    maker_approved: Mapped[bool] = mapped_column(default=False)
    disbursement_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    enriched_profile_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_config_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    schedule_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
