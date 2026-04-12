"""Document OCR and extraction -- mock for Indian document types."""

from __future__ import annotations

from app.tools.registry import ToolCategory, lending_tool

SUPPORTED_TYPES = [
    "AADHAAR",
    "PAN",
    "SALARY_SLIP",
    "ITR",
    "GST_RETURN",
    "PROPERTY_DOC",
    "VEHICLE_RC",
    "GOLD_APPRAISAL",
    "BANK_STATEMENT",
]


@lending_tool(
    name="extract_document",
    description="OCR + structured extraction for Indian document types",
    category=ToolCategory.DATA,
    timeout_seconds=15,
    circuit_breaker_threshold=3,
)
async def extract_document(
    document_type: str = "",
    document_data: str = "",
) -> dict:
    if document_type not in SUPPORTED_TYPES:
        return {"error": f"Unsupported type. Supported: {SUPPORTED_TYPES}"}

    base = {
        "document_type": document_type,
        "extraction_confidence": 0.92,
        "fields_extracted": 0,
    }

    if document_type == "ITR":
        base.update(
            {
                "fields_extracted": 8,
                "data": {
                    "assessment_year": "2025-26",
                    "total_income": "450000",
                    "tax_paid": "12500",
                    "filing_date": "2025-07-15",
                    "itr_form": "ITR-1",
                },
            }
        )
    elif document_type == "GST_RETURN":
        base.update(
            {
                "fields_extracted": 6,
                "data": {
                    "gstin": "24AAAAA0000A1Z5",
                    "period": "Jan-2026",
                    "turnover": "250000",
                    "tax_payable": "45000",
                    "filing_status": "FILED",
                },
            }
        )
    elif document_type == "VEHICLE_RC":
        base.update(
            {
                "fields_extracted": 5,
                "data": {
                    "registration_number": "GJ01AB1234",
                    "owner_name": "RAMESH PATEL",
                    "vehicle_class": "LMV",
                    "fuel_type": "DIESEL",
                    "hypothecation": None,
                },
            }
        )
    else:
        base["fields_extracted"] = 3
        base["data"] = {"raw_text": "Extracted document content"}

    return base
