"""Structured diagnostics for Omni validation and compilation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


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
    source: str | None = None
    line: int | None = None
    column: int | None = None

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("diagnostic code cannot be empty")
        if not self.message.strip():
            raise ValueError("diagnostic message cannot be empty")
        if self.line is not None and self.line < 1:
            raise ValueError("diagnostic line must be positive")
        if self.column is not None and self.column < 1:
            raise ValueError("diagnostic column must be positive")

    def to_dict(self) -> dict[str, str | int | None]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "path": self.path,
            "source": self.source,
            "line": self.line,
            "column": self.column,
        }

    def format(self) -> str:
        location = self.path or self.source or "<unknown>"
        if self.line is not None:
            location += f":{self.line}"
            if self.column is not None:
                location += f":{self.column}"
        return f"{location}: {self.severity.value} {self.code}: {self.message}"


def format_diagnostics(diagnostics: Iterable[Diagnostic]) -> str:
    """Render diagnostics deterministically for CLI and tooling consumers."""
    return "\n".join(diagnostic.format() for diagnostic in diagnostics)
