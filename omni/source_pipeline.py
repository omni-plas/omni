"""Open-world source-to-artifact orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import BackendRegistry
from .compile_engine import CompilationResult, compile_uir
from .frontend import FrontendRegistry
from .uir import UIR


class SourcePipelineError(ValueError):
    """Raised when source cannot be transformed into a target artifact."""


@dataclass(frozen=True)
class SourceCompilationResult:
    frontend_language: str
    compilation: CompilationResult


def compile_source(source: str, *, language: str, frontends: FrontendRegistry, backends: BackendRegistry, filename: str = "<source>") -> SourceCompilationResult:
    if not isinstance(source, str):
        raise TypeError("source must be a string")
    frontend = frontends.resolve(language)
    try:
        uir: UIR = frontend.parse(source, filename=filename)
    except Exception as exc:
        raise SourcePipelineError(f"frontend {frontend.language} failed to parse source: {exc}") from exc
    try:
        result = compile_uir(uir, backends)
    except Exception as exc:
        raise SourcePipelineError(f"compilation failed for {language}: {exc}") from exc
    return SourceCompilationResult(frontend.language, result)
