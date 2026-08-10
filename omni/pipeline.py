"""Composable Omni compilation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .compiler import CompilationPlan, plan_compilation
from .diagnostics import Diagnostic, Severity
from .ir import ModuleIR
from .lower import lower_to_ir
from .uir import UIR, validate_uir


@dataclass(frozen=True)
class CompilationResult:
    plan: CompilationPlan
    ir: ModuleIR
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(d.severity == Severity.ERROR for d in self.diagnostics)


def compile_semantics(document: Mapping[str, Any] | UIR) -> CompilationResult:
    """Validate UIR, derive a target plan, and lower it into semantic IR."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    plan = plan_compilation(uir)
    ir = lower_to_ir(uir)
    diagnostics = (
        Diagnostic(
            code="OMNI1000",
            severity=Severity.INFO,
            message="UIR validated, planned, and lowered into semantic IR",
        ),
    )
    return CompilationResult(plan=plan, ir=ir, diagnostics=diagnostics)
