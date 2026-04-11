"""Priority Sector Lending classification."""
from __future__ import annotations

from app.schemas.loan import PSLClassification
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool

PSL_MAP = {
    "DAIRY_FARMER": ("Agriculture", "Animal Husbandry", True),
    "CROP_FARMER": ("Agriculture", "Crop Loan", True),
    "KIRANA_SHOP": ("MSME", "Micro Enterprise", True),
    "GIG_WORKER": ("Other", None, False),
    "PERSONAL_LOAN": ("Other", None, False),
}


@lending_tool(
    name="check_psl_classification",
    description="Auto-classify loan for Priority Sector Lending reporting",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=1,
)
async def check_psl_classification(
    segment: str = "",
    loan_purpose: str = "",
) -> dict:
    category, sub_cat, eligible = PSL_MAP.get(segment, ("Other", None, False))

    return PSLClassification(
        category=category,
        sub_category=sub_cat,
        eligible=eligible,
        reason=(
            f"Segment {segment} classifies as {category}"
            + (f" / {sub_cat}" if sub_cat else "")
        ),
    ).model_dump()
