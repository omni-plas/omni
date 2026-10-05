"""Compatibility IR facade for legacy native builder APIs.

The canonical IR now lives in :mod:`omni.ir`. This facade keeps the older
FunctionIR constructor usable by native build tests while delegating richer
modules to the canonical representation.
"""
from __future__ import annotations

from dataclasses import dataclass

from .ir import BasicBlock, FunctionIR as CanonicalFunctionIR, Operation
from .types import TypeKind, TypeRef

@dataclass(frozen=True)
class FunctionIR:
    name: str
    parameters: tuple[str, ...] = ()
    blocks: tuple[BasicBlock, ...] = ()

    def to_canonical(self) -> CanonicalFunctionIR:
        integer = TypeRef(TypeKind.INTEGER)
        blocks = self.blocks or (
            BasicBlock(
                "entry",
                (
                    Operation("const", outputs=("%legacy_return",), attributes={"value": 0}),
                    Operation("return", inputs=("%legacy_return",)),
                ),
            ),
        )
        return CanonicalFunctionIR(self.name, {name: integer for name in self.parameters}, integer, blocks)
