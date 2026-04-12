"""Segment template loader -- reads YAML, validates schema, caches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class SegmentTemplate:
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        seg = config.get("segment", {})
        self.id: str = seg.get("id", "")
        self.version: int = seg.get("version", 1)
        self.channel: str = seg.get("channel", "whatsapp")
        self.languages: list[str] = seg.get("languages", ["hi"])

    @property
    def data_sources(self) -> dict[str, Any]:
        return self._config.get("data_sources", {})

    @property
    def scoring(self) -> dict[str, Any]:
        return self._config.get("scoring", {})

    @property
    def product(self) -> dict[str, Any]:
        return self._config.get("product", {})

    @property
    def monitoring(self) -> dict[str, Any]:
        return self._config.get("monitoring", {})

    @property
    def graduation(self) -> dict[str, Any]:
        return self._config.get("graduation", {})

    @property
    def journey(self) -> dict[str, Any]:
        return self._config.get("journey", {})

    @property
    def required_sources(self) -> list[str]:
        return self.data_sources.get("required", [])

    @property
    def optional_sources(self) -> list[str]:
        return self.data_sources.get("optional", [])

    @property
    def min_confidence(self) -> float:
        return self.data_sources.get("min_confidence", 0.5)

    @property
    def scoring_features(self) -> list[dict[str, Any]]:
        return self.scoring.get("features", [])

    @property
    def scoring_model(self) -> str:
        return self.scoring.get("model", "")

    def to_dict(self) -> dict[str, Any]:
        return dict(self._config)


class SegmentRegistry:
    _templates: dict[str, SegmentTemplate] = {}

    @classmethod
    def load_from_directory(cls, directory: str | Path) -> int:
        path = Path(directory)
        count = 0
        for yaml_file in path.glob("*.yaml"):
            if yaml_file.stem.startswith("."):
                continue
            with open(yaml_file) as f:
                config = yaml.safe_load(f) or {}
            seg_id = config.get("segment", {}).get("id", "")
            if seg_id:
                cls._templates[seg_id] = SegmentTemplate(config)
                count += 1
        return count

    @classmethod
    def get(cls, segment_id: str) -> SegmentTemplate | None:
        return cls._templates.get(segment_id)

    @classmethod
    def get_all(cls) -> dict[str, SegmentTemplate]:
        return dict(cls._templates)

    @classmethod
    def register(cls, template: SegmentTemplate) -> None:
        cls._templates[template.id] = template

    @classmethod
    def clear(cls) -> None:
        cls._templates.clear()
