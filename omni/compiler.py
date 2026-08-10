"""Semantic compilation planning for open-ended Omni targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .uir import UIR, UIRValidationError, validate_uir


class CompilationError(ValueError):
    """Raised when a compilation request cannot be planned safely."""


@dataclass(frozen=True)
class CompilationPlan:
    source_language: str
    target_platform: str
    target_architecture: str | None
    semantic_requirements: tuple[str, ...]


def plan_compilation(document: Mapping[str, Any] | UIR) -> CompilationPlan:
    """Validate a UIR and derive a target-independent semantic compilation plan."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    required = (
        "types",
        "control_flow",
        "data_flow",
        "memory_model",
        "error_handling",
        "io",
        "dependencies",
        "security",
        "performance",
    )
    missing = [key for key in required if key not in uir.semantics]
    if missing:
        raise CompilationError(
            "semantic model is incomplete; missing: " + ", ".join(missing)
        )

    architecture = uir.target.get("architecture")
    if architecture is not None and (not isinstance(architecture, str) or not architecture.strip()):
        raise UIRValidationError("target.architecture must be a non-empty string when supplied")

    return CompilationPlan(
        source_language=str(uir.source["language"]),
        target_platform=str(uir.target["platform"]),
        target_architecture=architecture,
        semantic_requirements=required,
    )
