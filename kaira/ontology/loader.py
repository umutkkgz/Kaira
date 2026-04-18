from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class OntologyGraph:
    data: dict[str, Any]

    @classmethod
    def from_file(cls, path: str | Path) -> "OntologyGraph":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def summary(self) -> dict[str, Any]:
        hotel = self.data.get("hotel", {})
        catalog = hotel.get("service_catalog", {})
        policies = hotel.get("policies", {})
        routes = self.data.get("tool_policy", {}).get("routes", {})
        concepts = self.data.get("concepts", [])
        relations = self.data.get("relations", [])
        return {
            "domain": self.data.get("metadata", {}).get("domain", "unknown"),
            "services": len(catalog),
            "policies": len(policies),
            "routes": len(routes),
            "concepts": len(concepts),
            "relations": len(relations),
            "blocked_patterns": len(self.data.get("adversarial_blocks", [])),
        }

