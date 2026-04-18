"""Backward-compatible import shim for older demo code."""

from kaira.ontology.loader import OntologyGraph
from kaira.policies.router import ToolRouter
from kaira.runtime.generator import DemoGenerator as BaseGenerator
from kaira.runtime.idl import InternalDeliberationLoop

__all__ = ["OntologyGraph", "ToolRouter", "BaseGenerator", "InternalDeliberationLoop"]
