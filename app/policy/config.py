"""YAML-based policy configuration loader for per-lender, per-segment overrides."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_policy_config(path: str | Path) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def merge_policies(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge override into base. Override values win."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_policies(result[key], value)
        else:
            result[key] = value
    return result


def get_authority_boundary(
    config: dict[str, Any], boundary_name: str, default: Any = None
) -> Any:
    boundaries = config.get("authority_boundaries", {})
    return boundaries.get(boundary_name, default)
