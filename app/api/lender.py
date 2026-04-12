"""Lender API -- multi-tenant lender management, webhooks, and API key authentication."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from app.core.logging import get_logger

router = APIRouter(prefix="/api/lender", tags=["lender"])
logger = get_logger(__name__)


class LenderConfig(BaseModel):
    lender_id: str
    name: str
    api_key_hash: str = ""
    webhook_url: str = ""
    webhook_secret: str = ""
    segments_enabled: list[str] = Field(default_factory=list)
    max_loan_amount: int = 500_000
    auto_approve_enabled: bool = False
    languages: list[str] = Field(default_factory=lambda: ["hi", "en"])
    created_at: str = ""
    active: bool = True


class LenderCreateRequest(BaseModel):
    name: str
    webhook_url: str = ""
    segments_enabled: list[str] = Field(default_factory=list)
    max_loan_amount: int = 500_000
    languages: list[str] = Field(default_factory=lambda: ["hi", "en"])


class LenderCreateResponse(BaseModel):
    lender_id: str
    name: str
    api_key: str
    webhook_url: str = ""
    segments_enabled: list[str] = []


class WebhookPayload(BaseModel):
    event: str
    lender_id: str
    data: dict = Field(default_factory=dict)
    timestamp: str = ""


_lender_store: dict[str, LenderConfig] = {}
_api_key_index: dict[str, str] = {}


def _hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


async def verify_api_key(x_api_key: str = Header(default="")) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    lender_id = _api_key_index.get(_hash_key(x_api_key))
    if not lender_id:
        raise HTTPException(status_code=401, detail="Invalid API key")
    lender = _lender_store.get(lender_id)
    if not lender or not lender.active:
        raise HTTPException(status_code=403, detail="Lender inactive")
    return lender_id


@router.post("/register", response_model=LenderCreateResponse)
async def register_lender(req: LenderCreateRequest) -> LenderCreateResponse:
    if not req.name.strip():
        raise HTTPException(status_code=400, detail="Lender name required")

    lender_id = f"lndr_{uuid.uuid4().hex[:12]}"
    api_key = f"lk_{secrets.token_urlsafe(32)}"
    webhook_secret = secrets.token_urlsafe(24)

    config = LenderConfig(
        lender_id=lender_id,
        name=req.name,
        api_key_hash=_hash_key(api_key),
        webhook_url=req.webhook_url,
        webhook_secret=webhook_secret,
        segments_enabled=req.segments_enabled,
        max_loan_amount=req.max_loan_amount,
        languages=req.languages,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    _lender_store[lender_id] = config
    _api_key_index[_hash_key(api_key)] = lender_id

    logger.info("lender_registered", lender_id=lender_id, name=req.name)

    return LenderCreateResponse(
        lender_id=lender_id,
        name=req.name,
        api_key=api_key,
        webhook_url=req.webhook_url,
        segments_enabled=req.segments_enabled,
    )


@router.get("/profile")
async def get_lender_profile(lender_id: str = Depends(verify_api_key)) -> dict:
    lender = _lender_store[lender_id]
    return {
        "lender_id": lender.lender_id,
        "name": lender.name,
        "segments_enabled": lender.segments_enabled,
        "max_loan_amount": lender.max_loan_amount,
        "languages": lender.languages,
        "active": lender.active,
        "created_at": lender.created_at,
    }


@router.get("/list")
async def list_lenders() -> dict:
    return {
        "lenders": [
            {
                "lender_id": lndr.lender_id,
                "name": lndr.name,
                "active": lndr.active,
                "segments": len(lndr.segments_enabled),
            }
            for lndr in _lender_store.values()
        ],
        "total": len(_lender_store),
    }


async def send_webhook(lender_id: str, event: str, data: dict) -> bool:
    """Send webhook notification to lender. Called internally after key events."""
    lender = _lender_store.get(lender_id)
    if not lender or not lender.webhook_url:
        return False

    import httpx

    payload = WebhookPayload(
        event=event,
        lender_id=lender_id,
        data=data,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    signature = hmac.new(
        lender.webhook_secret.encode(),
        payload.model_dump_json().encode(),
        hashlib.sha256,
    ).hexdigest()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                lender.webhook_url,
                json=payload.model_dump(),
                headers={
                    "X-Webhook-Signature": signature,
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            logger.info("webhook_sent", lender_id=lender_id, event=event, status=resp.status_code)
            return True
    except Exception as e:
        logger.error("webhook_error", lender_id=lender_id, event=event, error=str(e))
        return False
