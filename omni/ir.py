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

    def validate(self) -> None:
        if not isinstance(self.opcode, str) or not self.opcode.strip():
            raise ValueError("operation opcode must not be empty")
        for label, names in (("input", self.inputs), ("output", self.outputs)):
            if any(not isinstance(name, str) or not name.strip() for name in names):
                raise ValueError(f"operation {label} names must be non-empty")
        if len(self.outputs) != len(set(self.outputs)):
            raise ValueError(f"duplicate operation output: {self.opcode}")


@dataclass(frozen=True)
class BasicBlock:
    name: str
    operations: tuple[Operation, ...] = ()
    successors: tuple[str, ...] = ()

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("basic block name must not be empty")
        if len(self.successors) != len(set(self.successors)):
            raise ValueError(f"duplicate successor in block: {self.name}")
        if any(not isinstance(name, str) or not name.strip() for name in self.successors):
            raise ValueError(f"successor names must be non-empty in block: {self.name}")
        for operation in self.operations:
            operation.validate()


@dataclass(frozen=True)
class FunctionIR:
    name: str
    parameters: Mapping[str, TypeRef]
    result: TypeRef
    blocks: tuple[BasicBlock, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("function name must not be empty")
        if not self.blocks:
            raise ValueError(f"function has no blocks: {self.name}")
        self.result.validate()
        for parameter_name, parameter in self.parameters.items():
            if not isinstance(parameter_name, str) or not parameter_name.strip():
                raise ValueError(f"parameter name must not be empty: {self.name}")
            parameter.validate()
        block_names = [block.name for block in self.blocks]
        if len(block_names) != len(set(block_names)):
            raise ValueError(f"duplicate block in function: {self.name}")
        for block in self.blocks:
            block.validate()
        known = set(block_names)
        for block in self.blocks:
            for successor in block.successors:
                if successor not in known:
                    raise ValueError(f"unknown successor {successor!r} in {block.name!r}")


@dataclass(frozen=True)
class ModuleIR:
    name: str
    types: Mapping[str, TypeRef]
    functions: tuple[FunctionIR, ...]
    globals: Mapping[str, Value] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("module name must not be empty")
        for type_name, type_ref in self.types.items():
            if not isinstance(type_name, str) or not type_name.strip():
                raise ValueError("module type name must not be empty")
            type_ref.validate()
        names: set[str] = set()
        for function in self.functions:
            if function.name in names:
                raise ValueError(f"duplicate function: {function.name}")
            names.add(function.name)
            function.validate()
        for global_name, value in self.globals.items():
            if not isinstance(global_name, str) or not global_name.strip():
                raise ValueError("global name must not be empty")
            value.type.validate()
