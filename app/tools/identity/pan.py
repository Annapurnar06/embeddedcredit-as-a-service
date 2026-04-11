"""PAN verification tool (mock NSDL API with Jaro-Winkler name matching)."""
from __future__ import annotations

from app.schemas.borrower import PanVerifyResult
from app.tools.registry import ToolCategory, lending_tool


def _jaro_winkler_similarity(s1: str, s2: str) -> float:
    s1 = s1.upper().strip()
    s2 = s2.upper().strip()
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    max_dist = max(len(s1), len(s2)) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len(s1)
    s2_matches = [False] * len(s2)
    matches = 0
    transpositions = 0

    for i in range(len(s1)):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len(s2))
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len(s1)):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro = (
        matches / len(s1) + matches / len(s2) + (matches - transpositions / 2) / matches
    ) / 3

    prefix_len = 0
    for i in range(min(4, min(len(s1), len(s2)))):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break

    return jaro + prefix_len * 0.1 * (1 - jaro)


@lending_tool(
    name="verify_pan",
    description="Verify PAN card via NSDL API with name match against Aadhaar",
    category=ToolCategory.IDENTITY,
    requires_confirmation=False,
    timeout_seconds=10,
)
async def verify_pan(
    pan_number: str = "",
    aadhaar_name: str = "",
) -> dict:
    import re

    pan_pattern = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
    if not pan_number or not pan_pattern.match(pan_number.upper()):
        return PanVerifyResult(valid=False).model_dump()

    mock_pan_name = "RAMESH PATEL"
    name_match = _jaro_winkler_similarity(aadhaar_name, mock_pan_name)

    return PanVerifyResult(
        valid=True,
        name=mock_pan_name,
        name_match_score=round(name_match, 3),
        pan_status="ACTIVE",
    ).model_dump()
