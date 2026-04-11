"""ULI (Unified Lending Interface) parallel data fetch -- mock implementation."""
from __future__ import annotations

from app.schemas.borrower import ULIData
from app.tools.registry import ToolCategory, lending_tool


@lending_tool(
    name="fetch_uli_parallel",
    description="Parallel fetch from ULI data services (land, satellite, weather, PMFBY)",
    category=ToolCategory.DATA,
    timeout_seconds=5,
    circuit_breaker_threshold=3,
)
async def fetch_uli_parallel(
    aadhaar_hash: str = "",
    pincode: str = "",
    sources: list[str] | None = None,
) -> dict:
    sources = sources or ["LAND_RECORDS", "SATELLITE_NDVI", "WEATHER_IMD", "PMFBY"]
    result = ULIData()

    if "LAND_RECORDS" in sources:
        result.land_records = {
            "district": "Banaskantha",
            "survey_numbers": ["45/A", "46/B"],
            "total_area_acres": 4.5,
            "irrigation": "borewell",
            "crop_current": "bajra",
            "encumbrance": False,
        }
    if "SATELLITE_NDVI" in sources:
        result.satellite_ndvi = {
            "avg_ndvi_6m": 0.42,
            "ndvi_trend": "stable",
            "vegetation_health": "moderate",
        }
    if "WEATHER_IMD" in sources:
        result.weather_imd = {
            "district": "Banaskantha",
            "avg_temp_celsius": 34.2,
            "rainfall_mm_ytd": 320,
            "drought_risk": "low",
            "flood_risk": "none",
        }
    if "PMFBY" in sources:
        result.pmfby_coverage = {
            "enrolled": True,
            "season": "kharif",
            "crop": "bajra",
            "sum_insured": 45000,
        }
    return result.model_dump()
