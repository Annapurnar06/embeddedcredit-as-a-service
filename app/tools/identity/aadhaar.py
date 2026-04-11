"""Aadhaar eKYC verification tools (mock implementation with realistic schemas)."""
from __future__ import annotations

import hashlib
import random

from app.schemas.borrower import AadhaarVerifyResult
from app.tools.registry import ToolCategory, lending_tool

MOCK_PROFILES = [
    {
        "name": "Ramesh Patel",
        "dob": "1985-03-15",
        "gender": "M",
        "address_state": "Gujarat",
        "address_district": "Banaskantha",
        "address_pincode": "385001",
    },
    {
        "name": "Priya Sharma",
        "dob": "1990-07-22",
        "gender": "F",
        "address_state": "Gujarat",
        "address_district": "Mehsana",
        "address_pincode": "384001",
    },
    {
        "name": "Suresh Kumar",
        "dob": "1978-11-05",
        "gender": "M",
        "address_state": "Maharashtra",
        "address_district": "Pune",
        "address_pincode": "411001",
    },
]


def _generate_photo_hash(name: str) -> str:
    return hashlib.sha256(f"photo_{name}".encode()).hexdigest()[:16]


@lending_tool(
    name="verify_aadhaar_otp",
    description="Verify borrower identity via Aadhaar OTP (UIDAI eKYC)",
    category=ToolCategory.IDENTITY,
    requires_confirmation=False,
    timeout_seconds=15,
)
async def verify_aadhaar_otp(
    aadhaar_number: str = "",
    otp: str = "",
) -> dict:
    if not aadhaar_number or len(aadhaar_number.replace(" ", "")) != 12:
        return AadhaarVerifyResult(verified=False).model_dump()

    if otp and len(otp) == 6 and otp.isdigit():
        profile = random.choice(MOCK_PROFILES)
        return AadhaarVerifyResult(
            verified=True,
            name=profile["name"],
            dob=profile["dob"],
            gender=profile["gender"],
            address_state=profile["address_state"],
            address_district=profile["address_district"],
            address_pincode=profile["address_pincode"],
            photo_hash=_generate_photo_hash(profile["name"]),
        ).model_dump()

    if not otp:
        return {"otp_sent": True, "message": "OTP sent to registered mobile"}

    return AadhaarVerifyResult(verified=False).model_dump()


@lending_tool(
    name="verify_aadhaar_voice_otp",
    description="Verify borrower identity via Aadhaar voice OTP (voice channel)",
    category=ToolCategory.IDENTITY,
    requires_confirmation=False,
    timeout_seconds=20,
)
async def verify_aadhaar_voice_otp(
    aadhaar_number: str = "",
    spoken_otp: str = "",
) -> dict:
    if not aadhaar_number or len(aadhaar_number.replace(" ", "")) != 12:
        return AadhaarVerifyResult(verified=False).model_dump()

    if spoken_otp and len(spoken_otp) >= 4:
        profile = random.choice(MOCK_PROFILES)
        return AadhaarVerifyResult(
            verified=True,
            name=profile["name"],
            dob=profile["dob"],
            gender=profile["gender"],
            address_state=profile["address_state"],
            address_district=profile["address_district"],
            address_pincode=profile["address_pincode"],
            photo_hash=_generate_photo_hash(profile["name"]),
        ).model_dump()

    if not spoken_otp:
        return {"otp_sent": True, "voice_call_initiated": True}

    return AadhaarVerifyResult(verified=False).model_dump()
