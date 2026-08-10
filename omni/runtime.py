"""Deterministic reference runtime for the portable semantic IR subset."""

from __future__ import annotations

from typing import Any

from .ir import FunctionIR, ModuleIR, Operation


class RuntimeErrorBase(RuntimeError):
    """Base error raised by the reference Omni runtime."""


def _value(env: dict[str, Any], name: str) -> Any:
    if name not in env:
        raise RuntimeErrorBase(f"undefined value: {name}")
    return env[name]


def _execute_operation(operation: Operation, env: dict[str, Any]) -> Any:
    opcode = operation.opcode
    args = [_value(env, name) for name in operation.inputs]
    attrs = operation.attributes

    if opcode == "const":
        if not operation.outputs:
            raise RuntimeErrorBase("const requires an output")
        env[operation.outputs[0]] = attrs.get("value")
        return None
    if opcode in {"add", "sub", "mul", "div"}:
        if len(args) != 2 or len(operation.outputs) != 1:
            raise RuntimeErrorBase(f"{opcode} requires two inputs and one output")
        if opcode == "add":
            result = args[0] + args[1]
        elif opcode == "sub":
            result = args[0] - args[1]
        elif opcode == "mul":
            result = args[0] * args[1]
        else:
            if args[1] == 0:
                raise RuntimeErrorBase("division by zero")
            result = args[0] / args[1]
        env[operation.outputs[0]] = result
        return None
    if opcode == "return":
        if len(args) > 1:
            raise RuntimeErrorBase("return accepts at most one input")
        return args[0] if args else None
    raise RuntimeErrorBase(f"unsupported operation: {opcode}")


def execute(function: FunctionIR, arguments: dict[str, Any] | None = None) -> Any:
    """Execute a validated FunctionIR using the reference runtime."""
    env = dict(arguments or {})
    for name in function.parameters:
        if name not in env:
            raise RuntimeErrorBase(f"missing argument: {name}")

    blocks = {block.name: block for block in function.blocks}
    current = function.blocks[0].name
    visited = 0
    while True:
        visited += 1
        if visited > 100_000:
            raise RuntimeErrorBase("execution step limit exceeded")
        block = blocks[current]
        for operation in block.operations:
            result = _execute_operation(operation, env)
            if operation.opcode == "return":
                return result
        if not block.successors:
            raise RuntimeErrorBase(f"function ended without return: {function.name}")
        if len(block.successors) != 1:
            raise RuntimeErrorBase("reference runtime requires one successor per block")
        current = block.successors[0]


def execute_module(module: ModuleIR, entry: str, arguments: dict[str, Any] | None = None) -> Any:
    """Execute a named function from a validated module."""
    module.validate()
    for function in module.functions:
        if function.name == entry:
            return execute(function, arguments)
    raise RuntimeErrorBase(f"entry function not found: {entry}")
