"""Open-world orchestration from arbitrary source language to a target artifact."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .backend import BackendRegistry
from .compiler import CompilationPlan
from .frontend import FrontendRegistry
from .target_context import apply_target_context
from .targets import TargetDescriptor


class UniversalPipelineError(ValueError):
    """Raised when a universal compilation route cannot be completed."""


@dataclass(frozen=True)
class UniversalCompilationResult:
    language: str
    frontend_name: str
    plan: CompilationPlan
    backend_name: str
    artifact: Any


def compile_universal(
    source: str,
    language: str,
    target: TargetDescriptor,
    *,
    frontends: FrontendRegistry,
    backends: BackendRegistry,
    filename: str = "<source>",
) -> UniversalCompilationResult:
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    if not isinstance(language, str) or not language.strip():
        raise ValueError("language must be a non-empty string")
    if not isinstance(target, TargetDescriptor):
        raise TypeError("target must be a TargetDescriptor")
    frontend = frontends.resolve(language)
    raw_uir = frontend.parse(source, filename=filename)
    uir = apply_target_context(raw_uir, target)
    from .compile_engine import compile_uir
    result = compile_uir(uir, backends)
    if result.plan.target != target:
        raise UniversalPipelineError("compiler produced an artifact for an unexpected target")
    return UniversalCompilationResult(language, frontend.language, result.plan, result.backend_name, result.artifact)
