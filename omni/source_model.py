"""Language-neutral source representation owned by Omni itself."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SourceSpan:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid source span")


@dataclass(frozen=True)
class SourceNode:
    kind: str
    value: str | None = None
    children: tuple["SourceNode", ...] = ()
    attributes: Mapping[str, object] = ()
    span: SourceSpan | None = None

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ValueError("source node kind must not be empty")


@dataclass(frozen=True)
class SourceUnit:
    language: str
    root: SourceNode
    filename: str = "<source>"
    metadata: Mapping[str, object] = ()

    def __post_init__(self) -> None:
        if not self.language.strip():
            raise ValueError("source language must not be empty")

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
