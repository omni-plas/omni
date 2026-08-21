"""Composable Omni compilation pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .compiler import CompilationPlan, plan_compilation
from .diagnostics import Diagnostic, Severity
from .errors import ValidationError
from .ir import ModuleIR
from .lower import lower_to_ir
from .optimize import optimize_module
from .typecheck import check_module
from .uir import UIR, validate_uir
from .validation import SemanticValidationError, validate_module


@dataclass(frozen=True)
class CompilationResult:
    plan: CompilationPlan
    ir: ModuleIR | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(d.severity == Severity.ERROR for d in self.diagnostics)


def compile_semantics(document: Mapping[str, Any] | UIR) -> CompilationResult:
    """Validate, plan, lower, type-check, semantically validate, and optimize."""
    try:
        uir = document if isinstance(document, UIR) else validate_uir(document)
        plan = plan_compilation(uir)
        ir = lower_to_ir(uir)
    except (ValueError, TypeError) as exc:
        raise ValidationError(str(exc)) from exc

    diagnostics: list[Diagnostic] = []
    for diagnostic in check_module(ir):
        diagnostics.append(Diagnostic(
            code=diagnostic.code,
            severity=Severity.ERROR,
            message=diagnostic.message,
            path=f"{diagnostic.function or 'module'}:{diagnostic.block}" if diagnostic.block else diagnostic.function,
        ))
    if diagnostics:
        return CompilationResult(plan=plan, ir=ir, diagnostics=tuple(diagnostics))

    try:
        validate_module(ir)
    except SemanticValidationError as exc:
        diagnostics.append(Diagnostic(code="SEMANTIC_IR", severity=Severity.ERROR, message=str(exc), path=None))
        return CompilationResult(plan=plan, ir=ir, diagnostics=tuple(diagnostics))

    return CompilationResult(plan=plan, ir=optimize_module(ir), diagnostics=())
