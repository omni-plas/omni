"""Open-world target specification contracts for languages and platforms."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .targets import TargetDescriptor


@dataclass(frozen=True)
class TargetSpecification:
    """Formal information Omni may need before materializing a target."""

    target: TargetDescriptor
    semantics: Mapping[str, object] = field(default_factory=dict)
    abi: str | None = None
    executable_format: str | None = None
    boot_protocol: str | None = None
    runtime: str | None = None
    package_format: str | None = None
    installation_protocol: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TargetDescriptor):
            raise TypeError("target must be a TargetDescriptor")
        if not isinstance(self.semantics, Mapping):
            raise TypeError("semantics must be a mapping")
        for name in ("abi", "executable_format", "boot_protocol", "runtime", "package_format", "installation_protocol"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be non-empty when supplied")

    def capability(self, name: str) -> object | None:
        return self.semantics.get(name)

    def can_boot(self) -> bool:
        return bool(self.boot_protocol)

    def can_install(self) -> bool:
        return bool(self.installation_protocol or self.package_format)
