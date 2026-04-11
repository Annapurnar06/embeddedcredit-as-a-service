from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "lendingos-india",
        "version": "0.1.0",
    }
