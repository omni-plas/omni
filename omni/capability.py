"""Capability requirements and deterministic gap reporting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class CapabilityRequirement:
    name: str
    parameters: Mapping[str, object] = ()


@dataclass(frozen=True)
class CapabilityGap:
    requirement: CapabilityRequirement
    reason: str


@dataclass(frozen=True)
class CapabilityReport:
    satisfied: tuple[CapabilityRequirement, ...]
    gaps: tuple[CapabilityGap, ...]

    @property
    def complete(self) -> bool:
        return not self.gaps


def evaluate_capabilities(
    required: Iterable[CapabilityRequirement],
    available: Iterable[str],
) -> CapabilityReport:
    available_set = frozenset(available)
    satisfied: list[CapabilityRequirement] = []
    gaps: list[CapabilityGap] = []
    for requirement in required:
        if requirement.name in available_set:
            satisfied.append(requirement)
        else:
            gaps.append(CapabilityGap(requirement, f"capability not installed: {requirement.name}"))
    return CapabilityReport(tuple(satisfied), tuple(gaps))
