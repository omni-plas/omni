"""Structured validation reports for compiler clients and tooling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .diagnostics import Diagnostic, Severity


@dataclass(frozen=True)
class ValidationReport:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def valid(self) -> bool:
        return not any(item.severity == Severity.ERROR for item in self.diagnostics)

    @property
    def errors(self) -> tuple[Diagnostic, ...]:
        return tuple(item for item in self.diagnostics if item.severity == Severity.ERROR)

    @property
    def warnings(self) -> tuple[Diagnostic, ...]:
        return tuple(item for item in self.diagnostics if item.severity == Severity.WARNING)

    def to_dict(self) -> dict[str, object]:
        return {
            "valid": self.valid,
            "errors": [item.to_dict() for item in self.errors],
            "warnings": [item.to_dict() for item in self.warnings],
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }


def report(diagnostics: Iterable[Diagnostic]) -> ValidationReport:
    return ValidationReport(tuple(diagnostics))
