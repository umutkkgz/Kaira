from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PolicyConfig:
    allowed: set[str]
    approval_required: set[str]
    forbidden: set[str]
    out_of_domain: set[str]

    @classmethod
    def from_dict(cls, data: dict) -> "PolicyConfig":
        return cls(
            allowed=set(data.get("allowed", [])),
            approval_required=set(data.get("approval_required", [])),
            forbidden=set(data.get("forbidden", [])),
            out_of_domain=set(data.get("out_of_domain", [])),
        )

    def status_for(self, action: str) -> str:
        if action in self.forbidden:
            return "forbidden"
        if action in self.out_of_domain:
            return "out_of_domain"
        if action in self.approval_required:
            return "approval_required"
        if action in self.allowed:
            return "allowed"
        return "unknown"

