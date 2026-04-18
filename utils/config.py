from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if config_path.suffix == ".json":
        return json.loads(config_path.read_text(encoding="utf-8"))
    if config_path.suffix in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to load YAML config files.") from exc
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))
    raise ValueError(f"Unsupported config format: {config_path.suffix}")

