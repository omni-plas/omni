"""Semantic compilation planning for open-ended Omni targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .schema import REQUIRED_SEMANTIC_FIELDS
from .targets import TargetDescriptor
from .uir import UIR, UIRValidationError, validate_uir


class CompilationError(ValueError):
    """Raised when a compilation request cannot be planned safely."""


@dataclass(frozen=True)
class CompilationPlan:
    source_language: str
    target: TargetDescriptor
    semantic_requirements: tuple[str, ...]

    def target_identity(self) -> str:
        return self.target.identity()

    def requires(self, name: str) -> bool:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("semantic requirement name must be non-empty")
        return name.strip() in self.semantic_requirements


def plan_compilation(document: Mapping[str, Any] | UIR) -> CompilationPlan:
    """Validate UIR and derive a target-independent semantic compilation plan."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    missing = [key for key in REQUIRED_SEMANTIC_FIELDS if key not in uir.semantics]
    if missing:
        raise CompilationError(
            "semantic model is incomplete; missing: " + ", ".join(missing)
        )

    platform = uir.target["platform"]
    architecture = uir.target.get("architecture")
    abi = uir.target.get("abi")
    if architecture is not None and (not isinstance(architecture, str) or not architecture.strip()):
        raise UIRValidationError("target.architecture must be a non-empty string when supplied")
    if abi is not None and (not isinstance(abi, str) or not abi.strip()):
        raise UIRValidationError("target.abi must be a non-empty string when supplied")

    capabilities = uir.target.get("capabilities", {})
    if not isinstance(capabilities, Mapping):
        raise UIRValidationError("target.capabilities must be an object when supplied")

    return CompilationPlan(
        source_language=str(uir.source["language"]),
        target=TargetDescriptor(
            platform=str(platform),
            architecture=architecture,
            abi=abi,
            capabilities=dict(capabilities),
        ),
        semantic_requirements=REQUIRED_SEMANTIC_FIELDS,
    )
