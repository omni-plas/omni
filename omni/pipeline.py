"""Composable Omni compilation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .compiler import CompilationPlan, plan_compilation
from .diagnostics import Diagnostic, Severity
from .ir import ModuleIR
from .lower import lower_to_ir
from .typecheck import check_module
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
    """Validate UIR, plan targets, lower to IR, and verify typed data flow."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    plan = plan_compilation(uir)
    ir = lower_to_ir(uir)
    diagnostics: list[Diagnostic] = [
        Diagnostic(
            code="OMNI1000",
            severity=Severity.INFO,
            message="UIR validated, planned, and lowered into semantic IR",
        ),
    ]
    for diagnostic in check_module(ir):
        diagnostics.append(
            Diagnostic(
                code=diagnostic.code,
                severity=Severity.ERROR,
                message=diagnostic.message,
                path=f"{diagnostic.function or 'module'}:{diagnostic.block}" if diagnostic.block else diagnostic.function,
            )
        )
    return CompilationResult(plan=plan, ir=ir, diagnostics=tuple(diagnostics))
