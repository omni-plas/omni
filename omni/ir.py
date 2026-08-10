"""Semantic intermediate representation for executable Omni programs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .types import TypeRef


@dataclass(frozen=True)
class Value:
    type: TypeRef
    data: Any = None


@dataclass(frozen=True)
class Operation:
    opcode: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BasicBlock:
    name: str
    operations: tuple[Operation, ...] = ()
    successors: tuple[str, ...] = ()


@dataclass(frozen=True)
class FunctionIR:
    name: str
    parameters: Mapping[str, TypeRef]
    result: TypeRef
    blocks: tuple[BasicBlock, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModuleIR:
    name: str
    types: Mapping[str, TypeRef]
    functions: tuple[FunctionIR, ...]
    globals: Mapping[str, Value] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError("module name must not be empty")
        names: set[str] = set()
        for function in self.functions:
            if function.name in names:
                raise ValueError(f"duplicate function: {function.name}")
            names.add(function.name)
            function.result.validate()
            for parameter in function.parameters.values():
                parameter.validate()
            block_names = {block.name for block in function.blocks}
            if not function.blocks:
                raise ValueError(f"function has no blocks: {function.name}")
            for block in function.blocks:
                for successor in block.successors:
                    if successor not in block_names:
                        raise ValueError(f"unknown successor {successor!r} in {block.name!r}")
