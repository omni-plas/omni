"""Core type system primitives for Omni's semantic IR."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class TypeKind(str, Enum):
    VOID = "void"
    BOOL = "bool"
    INTEGER = "integer"
    INT = "integer"  # Backward-compatible alias
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
    bits: int | None = None
    signed: bool | None = None

    def validate(self) -> None:
        if self.name is not None and (not isinstance(self.name, str) or not self.name.strip()):
            raise ValueError("type name cannot be empty")
        if self.bits is not None and (not isinstance(self.bits, int) or isinstance(self.bits, bool) or self.bits <= 0):
            raise ValueError("type bit width must be a positive integer")
        if self.signed is not None and not isinstance(self.signed, bool):
            raise ValueError("type signedness must be boolean when supplied")
        if self.kind != TypeKind.INTEGER and (self.bits is not None or self.signed is not None):
            raise ValueError("bit width and signedness are only valid for integer types")
        if self.kind in {TypeKind.STRUCT} and not self.fields and not self.name:
            raise ValueError("struct type requires fields or a name")
        if self.kind in {TypeKind.ARRAY, TypeKind.POINTER, TypeKind.RESOURCE} and not self.parameters:
            raise ValueError(f"{self.kind.value} type requires a parameter")
        if self.kind == TypeKind.MAP and len(self.parameters) != 2:
            raise ValueError("map type requires key and value parameters")
        if self.kind == TypeKind.FUNCTION and len(self.parameters) < 1:
            raise ValueError("function type requires at least a return type")
        if self.kind == TypeKind.VOID and (self.parameters or self.fields):
            raise ValueError("void type cannot have parameters or fields")
        for parameter in self.parameters:
            parameter.validate()
        for field_name, field_type in self.fields.items():
            if not isinstance(field_name, str) or not field_name.strip():
                raise ValueError("struct field names cannot be empty")
            field_type.validate()

    def signature(self) -> str:
        """Return a stable structural signature useful for caches and diagnostics."""
        parts = [self.kind.value]
        if self.name:
            parts.append(f"name={self.name}")
        if self.bits is not None:
            parts.append(f"bits={self.bits}")
        if self.signed is not None:
            parts.append(f"signed={self.signed}")
        if self.nullable:
            parts.append("nullable")
        if self.parameters:
            parts.append("params=" + ",".join(parameter.signature() for parameter in self.parameters))
        if self.fields:
            fields = ",".join(f"{name}:{self.fields[name].signature()}" for name in sorted(self.fields))
            parts.append(f"fields={fields}")
        return "<" + ";".join(parts) + ">"

    def is_numeric(self) -> bool:
        return self.kind in {TypeKind.INTEGER, TypeKind.FLOAT}

    def is_scalar(self) -> bool:
        return self.kind in {TypeKind.BOOL, TypeKind.INTEGER, TypeKind.FLOAT, TypeKind.STRING, TypeKind.BYTES}
