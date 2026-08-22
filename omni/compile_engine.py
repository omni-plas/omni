"""Backend-driven compilation orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .backend import BackendRegistry
from .compiler import CompilationPlan, plan_compilation
from .uir import UIR, validate_uir


@dataclass(frozen=True)
class CompilationResult:
    plan: CompilationPlan
    backend_name: str
    artifact: Any


def compile_uir(document: Mapping[str, Any] | UIR, registry: BackendRegistry) -> CompilationResult:
    """Validate UIR, select exactly one target backend, and generate an artifact."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    plan = plan_compilation(uir)
    selection = registry.select(plan.target)
    artifact = selection.backend.compile(uir, plan)
    return CompilationResult(plan, selection.backend.name, artifact)
