"""Self-build planning and validation primitives for Omni.

This module does not fake a self-hosting compiler. It models the contract that a
real self-build implementation must satisfy and validates produced artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256


class SelfBuildError(ValueError):
    """Raised when a self-build contract is invalid."""


class SelfBuildStage(str, Enum):
    SOURCE = "source"
    FRONTEND = "frontend"
    SEMANTICS = "semantics"
    COMPILER = "compiler"
    RUNTIME = "runtime"
    TOOLS = "tools"
    PACKAGE = "package"
    INSTALL = "install"
    VALIDATE = "validate"


@dataclass(frozen=True)
class SelfBuildSpec:
    source_digest: str
    target: str
    bootstrap_allowed: bool = True
    external_compiler_required: bool = False

    def __post_init__(self) -> None:
        if len(self.source_digest) != 64 or any(c not in "0123456789abcdef" for c in self.source_digest.lower()):
            raise SelfBuildError("source_digest must be a SHA-256 hexadecimal digest")
        if not self.target.strip():
            raise SelfBuildError("self-build target must be non-empty")
        if self.external_compiler_required and not self.bootstrap_allowed:
            raise SelfBuildError("a non-bootstrap self-build cannot require an external compiler")


@dataclass(frozen=True)
class SelfBuildResult:
    spec: SelfBuildSpec
    artifact_digest: str
    stages: tuple[SelfBuildStage, ...]
    self_hosted: bool

    @property
    def complete(self) -> bool:
        required = tuple(SelfBuildStage)
        return self.self_hosted and all(stage in self.stages for stage in required)


def source_digest(source: bytes) -> str:
    return sha256(source).hexdigest()


def validate_self_build_result(result: SelfBuildResult) -> None:
    if len(result.artifact_digest) != 64 or any(c not in "0123456789abcdef" for c in result.artifact_digest.lower()):
        raise SelfBuildError("artifact_digest must be a SHA-256 hexadecimal digest")
    if len(set(result.stages)) != len(result.stages):
        raise SelfBuildError("self-build stages must not be duplicated")
    if not result.complete:
        raise SelfBuildError("self-build result does not satisfy the complete self-hosting contract")


def plan_self_build(source: bytes, target: str, *, bootstrap_allowed: bool = True) -> SelfBuildSpec:
    """Create a deterministic self-build specification from Omni source."""
    return SelfBuildSpec(source_digest(source), target, bootstrap_allowed=bootstrap_allowed)
