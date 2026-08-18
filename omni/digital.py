"""Open-world model for any digital entity, including multimedia."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class DigitalSpec:
    """A language-neutral specification of any digital entity.

    ``kind`` is intentionally open-ended: applications, operating systems,
    programming languages, libraries, plugins, images, audio, video, 3D
    assets, documents, future formats, and previously unknown entity kinds
    can all be represented without changing this model.
    """
    kind: str
    name: str
    behavior: Mapping[str, Any] = field(default_factory=dict)
    interfaces: tuple[str, ...] = ()
    data: Mapping[str, Any] = field(default_factory=dict)
    requirements: Mapping[str, Any] = field(default_factory=dict)
    extensions: Mapping[str, Any] = field(default_factory=dict)
    media: Mapping[str, Any] = field(default_factory=dict)
    format: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.kind.strip() or not self.name.strip():
            raise ValueError("digital kind and name must be non-empty")
        for name, value in (("behavior", self.behavior), ("data", self.data),
                            ("requirements", self.requirements), ("extensions", self.extensions),
                            ("media", self.media), ("metadata", self.metadata)):
            if not isinstance(value, Mapping):
                raise TypeError(f"{name} must be an object")
        if not isinstance(self.interfaces, tuple):
            raise TypeError("interfaces must be a tuple")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "kind": self.kind, "name": self.name, "behavior": dict(self.behavior),
            "interfaces": list(self.interfaces), "data": dict(self.data),
            "requirements": dict(self.requirements), "extensions": dict(self.extensions),
            "media": dict(self.media), "format": self.format, "metadata": dict(self.metadata),
        }
