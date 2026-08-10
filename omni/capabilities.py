"""Capability matching between semantic requirements and concrete targets."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True)
class CapabilityGap:
    capability: str
    required: str
    available: str | None

@dataclass(frozen=True)
class CapabilityReport:
    satisfied: tuple[str, ...]
    missing: tuple[CapabilityGap, ...]

    @property
    def is_satisfied(self) -> bool:
        return not self.missing


def match(requirements: Mapping[str, str], capabilities: Mapping[str, str]) -> CapabilityReport:
    satisfied: list[str] = []
    missing: list[CapabilityGap] = []
    for key, required in requirements.items():
        available = capabilities.get(key)
        if available == required or (available is not None and required == "*"):
            satisfied.append(key)
        else:
            missing.append(CapabilityGap(key, required, available))
    return CapabilityReport(tuple(satisfied), tuple(missing))
