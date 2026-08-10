"""Core type system primitives for Omni's semantic IR."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class TypeKind(str, Enum):
    VOID = "void"
    BOOL = "bool"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BYTES = "bytes"
    ARRAY = "array"
    MAP = "map"
    STRUCT = "struct"
    FUNCTION = "function"
    POINTER = "pointer"
    RESOURCE = "resource"
    ANY = "any"


@dataclass(frozen=True)
class TypeRef:
    """A recursive, target-neutral type reference."""

    kind: TypeKind
    name: str | None = None
    parameters: tuple["TypeRef", ...] = ()
    fields: Mapping[str, "TypeRef"] = field(default_factory=dict)
    nullable: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.kind in {TypeKind.STRUCT} and not self.fields and not self.name:
            raise ValueError("struct type requires fields or a name")
        if self.kind in {TypeKind.ARRAY, TypeKind.POINTER, TypeKind.RESOURCE} and not self.parameters:
            raise ValueError(f"{self.kind.value} type requires a parameter")
        if self.kind == TypeKind.FUNCTION and len(self.parameters) < 1:
            raise ValueError("function type requires at least a return type")
        for parameter in self.parameters:
            parameter.validate()
        for field_type in self.fields.values():
            field_type.validate()
