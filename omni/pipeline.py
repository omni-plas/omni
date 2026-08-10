"""Composable Omni compilation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .compiler import CompilationPlan, plan_compilation
from .diagnostics import Diagnostic, Severity
from .ir import ModuleIR
from .uir import UIR, validate_uir


@dataclass(frozen=True)
class CompilationResult:
    plan: CompilationPlan
    ir: ModuleIR | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(d.severity == Severity.ERROR for d in self.diagnostics)


def validate_and_plan(document: Mapping[str, Any] | UIR) -> CompilationResult:
    """Run the front half of compilation without fabricating an output artifact."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    plan = plan_compilation(uir)
    diagnostics: Sequence[Diagnostic] = (
        Diagnostic(
            code="OMNI1000",
            severity=Severity.INFO,
            message="UIR validated and semantic compilation plan created",
            path=None,
        ),
    )
    return CompilationResult(plan=plan, ir=None, diagnostics=tuple(diagnostics))
