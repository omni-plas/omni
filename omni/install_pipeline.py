"""Validation pipeline from target specification to installation planning."""

from __future__ import annotations

from dataclasses import dataclass

from .installer import InstallationPlan, InstallerKind, plan_installation
from .install_format import InstallFormat
from .target_specs import TargetSpecification


class InstallPipelineError(ValueError):
    """Raised when target capabilities cannot satisfy installation requirements."""


@dataclass(frozen=True)
class InstallPipeline:
    specification: TargetSpecification
    format: InstallFormat
    plan: InstallationPlan

    def __post_init__(self) -> None:
        if self.format.target != self.specification.target:
            raise InstallPipelineError("install format target does not match specification")
        if self.plan.target != self.specification.target:
            raise InstallPipelineError("installation plan target does not match specification")
        if self.plan.bootable and not self.specification.can_boot():
            raise InstallPipelineError("bootable installation requires a boot protocol")


def create_install_pipeline(
    specification: TargetSpecification,
    *,
    name: str,
    version: str,
    artifact_format: str,
    bootable: bool = False,
    filesystem: str | None = None,
    kind: InstallerKind = InstallerKind.PACKAGE,
) -> InstallPipeline:
    if not isinstance(specification, TargetSpecification):
        raise TypeError("specification must be a TargetSpecification")
    if bootable and not specification.can_boot():
        raise InstallPipelineError("target specification does not define a boot protocol")
    fmt = InstallFormat(name, version, specification.target, bootable, filesystem)
    plan = plan_installation(
        specification.target,
        kind=kind,
        artifact_format=artifact_format,
        bootable=bootable,
        filesystem=filesystem,
    )
    return InstallPipeline(specification, fmt, plan)
