"""Confirmation detection -- parse borrower utterances for consent signals."""

from __future__ import annotations

import re

CONFIRM_PATTERNS = re.compile(
    r"\b(haan|ha+n|yes|theek hai|theek|confirm|agreed|accept|"
    r"ok|okay|chalega|kar do|karo|kijiye|manzoor|razi)\b",
    re.IGNORECASE,
)

DENY_PATTERNS = re.compile(
    r"\b(nahi|nah|no|reject|cancel|mat karo|mat kijiye|"
    r"ruk|rukiye|band|naa)\b",
    re.IGNORECASE,
)


def detect_confirmation(text: str) -> bool | None:
    """Returns True for confirm, False for deny, None for unclear."""
    text_clean = text.strip().lower()

    if DENY_PATTERNS.search(text_clean):
        return False
    if CONFIRM_PATTERNS.search(text_clean):
        return True
    return None


def extract_aadhaar(text: str) -> str | None:
    """Extract 12-digit Aadhaar number from text."""
    pattern = re.compile(r"\b(\d{4}\s?\d{4}\s?\d{4})\b")
    match = pattern.search(text)
    if match:
        return match.group(1).replace(" ", "")
    return None


def extract_otp(text: str) -> str | None:
    """Extract 6-digit OTP from text."""
    pattern = re.compile(r"\b(\d{6})\b")
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None


def extract_pan(text: str) -> str | None:
    """Extract PAN number from text."""
    pattern = re.compile(r"\b([A-Z]{5}\d{4}[A-Z])\b", re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return match.group(1).upper()
    return None
