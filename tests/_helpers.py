from __future__ import annotations

from pathlib import Path

from kaira.ontology.loader import OntologyGraph
from kaira.runtime.controller import RuntimeController
from kaira.utils.config import load_config


ROOT = Path(__file__).resolve().parents[1]


def make_controller() -> RuntimeController:
    ontology = OntologyGraph.from_file(ROOT / "data" / "mini_ontology.json")
    policy = load_config(ROOT / "kaira" / "config" / "default_policy.json")
    return RuntimeController(ontology, policy)
