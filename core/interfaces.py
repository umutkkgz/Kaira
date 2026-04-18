from __future__ import annotations

from typing import Protocol

from kaira.core.types import DraftResponse, RoutingDecision, RuntimeState, UserInput, ValidationResult


class Generator(Protocol):
    name: str

    def generate(self, user_input: UserInput, state: RuntimeState, iteration: int) -> DraftResponse:
        ...


class Validator(Protocol):
    def validate(self, query: str, candidate: str, route: RoutingDecision) -> ValidationResult:
        ...


class Router(Protocol):
    def route(self, query: str) -> RoutingDecision:
        ...


class MemoryStore(Protocol):
    def get_state(self, session_id: str) -> RuntimeState:
        ...

    def append(self, session_id: str, content: str) -> None:
        ...

