"""Language-neutral source representation owned by Omni itself."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class SourceSpan:
    start: int
    end: int

    def __post_init__(self) -> None:
        if not isinstance(self.start, int) or isinstance(self.start, bool) or not isinstance(self.end, int) or isinstance(self.end, bool):
            raise TypeError("source span offsets must be integers")
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid source span")

    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class SourceNode:
    kind: str
    value: str | None = None
    children: tuple["SourceNode", ...] = ()
    attributes: Mapping[str, object] = field(default_factory=dict)
    span: SourceSpan | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("source node kind must be a non-empty string")
        if self.value is not None and not isinstance(self.value, str):
            raise TypeError("source node value must be text or None")
        if not isinstance(self.attributes, Mapping):
            raise TypeError("source node attributes must be an object")
        if not isinstance(self.children, tuple):
            raise TypeError("source node children must be a tuple")
        if any(not isinstance(child, SourceNode) for child in self.children):
            raise TypeError("source node children must contain SourceNode values")
        if self.span is not None and not isinstance(self.span, SourceSpan):
            raise TypeError("source node span must be SourceSpan or None")


@dataclass(frozen=True)
class SourceUnit:
    language: str
    root: SourceNode
    filename: str = "<source>"
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.language, str) or not self.language.strip():
            raise ValueError("source language must be a non-empty string")
        if not isinstance(self.root, SourceNode):
            raise TypeError("source root must be SourceNode")
        if not isinstance(self.filename, str) or not self.filename.strip():
            raise ValueError("source filename must be a non-empty string")
        if not isinstance(self.metadata, Mapping):
            raise TypeError("source metadata must be an object")

    def to_dict(self) -> dict[str, object]:
        def encode(node: SourceNode) -> dict[str, object]:
            return {
                "kind": node.kind,
                "value": node.value,
                "children": [encode(child) for child in node.children],
                "attributes": dict(node.attributes),
                "span": None if node.span is None else {
                    "start": node.span.start,
                    "end": node.span.end,
                },
            }
        return {
            "language": self.language,
            "filename": self.filename,
            "root": encode(self.root),
            "metadata": dict(self.metadata),
        }
