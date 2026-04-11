from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.audit import AuditLog, ToolExecution

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/logs/{session_id}")
async def get_audit_logs(session_id: UUID, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.session_id == session_id)
        .order_by(AuditLog.created_at.asc())
    )
    logs = result.scalars().all()
    return {
        "session_id": str(session_id),
        "count": len(logs),
        "logs": [
            {
                "id": str(log.id),
                "event_type": log.event_type,
                "actor": log.actor,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ],
    }


@router.get("/tools/{session_id}")
async def get_tool_executions(session_id: UUID, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(
        select(ToolExecution)
        .where(ToolExecution.session_id == session_id)
        .order_by(ToolExecution.created_at.asc())
    )
    executions = result.scalars().all()
    return {
        "session_id": str(session_id),
        "count": len(executions),
        "executions": [
            {
                "id": str(ex.id),
                "tool_name": ex.tool_name,
                "tool_category": ex.tool_category,
                "result_status": ex.result_status,
                "latency_ms": ex.latency_ms,
                "session_state_before": ex.session_state_before,
                "session_state_after": ex.session_state_after,
                "created_at": ex.created_at.isoformat(),
            }
            for ex in executions
        ],
    }


@router.get("/loan/{loan_application_id}")
async def get_loan_audit_trail(
    loan_application_id: UUID, db: AsyncSession = Depends(get_db)
) -> dict:
    logs_result = await db.execute(
        select(AuditLog)
        .where(AuditLog.loan_application_id == loan_application_id)
        .order_by(AuditLog.created_at.asc())
    )
    tools_result = await db.execute(
        select(ToolExecution)
        .where(ToolExecution.loan_application_id == loan_application_id)
        .order_by(ToolExecution.created_at.asc())
    )
    logs = logs_result.scalars().all()
    tools = tools_result.scalars().all()
    return {
        "loan_application_id": str(loan_application_id),
        "audit_logs": len(logs),
        "tool_executions": len(tools),
        "timeline": sorted(
            [
                {
                    "type": "audit_log",
                    "event": log.event_type,
                    "actor": log.actor,
                    "timestamp": log.created_at.isoformat(),
                }
                for log in logs
            ]
            + [
                {
                    "type": "tool_execution",
                    "event": f"{ex.tool_name} -> {ex.result_status}",
                    "actor": "agent",
                    "timestamp": ex.created_at.isoformat(),
                }
                for ex in tools
            ],
            key=lambda x: x["timestamp"],
        ),
    }
