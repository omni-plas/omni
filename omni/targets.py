"""Extensible target descriptors for Omni compilation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping


class TargetError(ValueError):
    """Raised when a target descriptor cannot be represented safely."""


@dataclass(frozen=True)
class TargetDescriptor:
    """Describes a compilation target without a closed OS/CPU enumeration."""

    platform: str
    architecture: str | None = None
    abi: str | None = None
    capabilities: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.platform, str) or not self.platform.strip():
            raise TargetError("target platform cannot be empty")
        for label, value in (("architecture", self.architecture), ("abi", self.abi)):
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise TargetError(f"target {label} cannot be empty")
        if not isinstance(self.capabilities, Mapping):
            raise TypeError("target capabilities must be a mapping")
        if any(not isinstance(k, str) or not k.strip() for k in self.capabilities):
            raise TargetError("target capability names must be non-empty strings")
        if any(isinstance(v, str) and not v.strip() for v in self.capabilities.values()):
            raise TargetError("target capability values cannot be empty strings")
        object.__setattr__(self, "platform", self.platform.strip())
        object.__setattr__(self, "architecture", self.architecture.strip() if self.architecture else None)
        object.__setattr__(self, "abi", self.abi.strip() if self.abi else None)
        object.__setattr__(self, "capabilities", dict(self.capabilities))

    def identity(self) -> str:
        return "-".join(p for p in (self.platform, self.architecture, self.abi) if p)

    def capability(self, name: str, default: Any = None) -> Any:
        if not isinstance(name, str) or not name.strip():
            raise TargetError("capability name cannot be empty")
        return self.capabilities.get(name, default)

    def supports(self, capability: str, value: Any = None) -> bool:
        if not isinstance(capability, str) or not capability.strip():
            raise TargetError("capability name cannot be empty")
        actual = self.capabilities.get(capability)
        return actual is not None and (value is None or actual == value)

    def require(self, capability: str, value: Any = None) -> None:
        if not self.supports(capability, value):
            suffix = f"={value}" if value is not None else ""
            raise TargetError(f"target {self.identity()} lacks capability {capability}{suffix}")

    def with_capability(self, name: str, value: Any) -> "TargetDescriptor":
        if not isinstance(name, str) or not name.strip():
            raise TargetError("capability name cannot be empty")
        capabilities = dict(self.capabilities)
        capabilities[name.strip()] = value
        return TargetDescriptor(self.platform, self.architecture, self.abi, capabilities)

    def document(self) -> dict[str, Any]:
        """Return the canonical open-world target document."""
        return {
            "schema": "omni.target.v1",
            "platform": self.platform,
            "architecture": self.architecture,
            "abi": self.abi,
            "capabilities": dict(self.capabilities),
        }

    def serialize(self) -> bytes:
        """Serialize a deterministic target descriptor."""
        try:
            return (json.dumps(self.document(), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        except (TypeError, ValueError) as exc:
            raise TargetError(f"target capabilities are not JSON-serializable: {exc}") from exc

    @classmethod
    def from_document(cls, document: Mapping[str, Any]) -> "TargetDescriptor":
        if not isinstance(document, Mapping):
            raise TargetError("target document must be an object")
        if document.get("schema") != "omni.target.v1":
            raise TargetError("unsupported target document schema")
        try:
            return cls(document["platform"], document.get("architecture"), document.get("abi"), document.get("capabilities", {}))
        except (KeyError, TypeError, ValueError) as exc:
            raise TargetError(f"invalid target document: {exc}") from exc

    @classmethod
    def deserialize(cls, payload: bytes | str) -> "TargetDescriptor":
        try:
            document = json.loads(payload.decode("utf-8") if isinstance(payload, bytes) else payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TargetError(f"invalid target JSON: {exc}") from exc
        return cls.from_document(document)
