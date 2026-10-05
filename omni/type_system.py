"""Extensible target-neutral type model for Omni IR."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Type:
    name: str
    bits: int | None = None
    signed: bool | None = None

I1 = Type("i1", 1, False)
I8 = Type("i8", 8, False)
I32 = Type("i32", 32, True)
I64 = Type("i64", 64, True)
VOID = Type("void")
Void = VOID

@dataclass(frozen=True)
class ValueType:
    value: str
    type: Type

def require_same_type(left: Type, right: Type) -> Type:
    if left != right:
        raise TypeError(f"type mismatch: {left.name} != {right.name}")
    return left
