"""Structured diagnostics for Omni validation and compilation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "path": self.path,
        }
