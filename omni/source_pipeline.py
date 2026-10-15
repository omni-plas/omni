""""Open-world source-to-artifact orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import BackendRegistry
from .compile_engine import CompilationResult, compile_uir
from .frontend import FrontendRegistry
from .target_context import apply_target_context
from .targets import TargetDescriptor
from .uir import UIR


class SourcePipelineError(ValueError):
    """Raised when source cannot be transformed into a target artifact."""


@dataclass(frozen=True)
class SourceCompilationResult:
    frontend_language: str
    compilation: CompilationResult


def compile_source(
    source: str,
    *,
    language: str,
    frontends: FrontendRegistry,
    backends: BackendRegistry,
    filename: str = "<source>",
    version: str | None = None,
    extension: str | None = None,
    target: TargetDescriptor | None = None,
) -> SourceCompilationResult:
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    try:
        frontend = frontends.resolve(language, version=version, extension=extension)
    except (LookupError, ValueError) as exc:
        raise SourcePipelineError(f"unable to resolve source language {language!r}: {exc}") from exc

    try:
        uir: UIR = frontend.parse(source, filename=filename)
        if target is not None:
            uir = apply_target_context(uir, target)
    except Exception as exc:
        raise SourcePipelineError(f"frontend {frontend.language} failed to parse source: {exc}") from exc

    try:
        result = compile_uir(uir, backends)
    except Exception as exc:
        raise SourcePipelineError(f"compilation failed for {language}: {exc}") from exc
    if target is not None and result.plan.target != target:
        raise SourcePipelineError("compiler produced an artifact for an unexpected target")
    return SourceCompilationResult(frontend.language, result)
