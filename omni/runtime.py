"""Deterministic reference runtime for the portable semantic IR subset."""

from __future__ import annotations

from typing import Any

from .ir import FunctionIR, ModuleIR, Operation
from .validation import SemanticValidationError, validate_function, validate_module


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
        env[operation.outputs[0]] = attrs["value"]
        return None
    if opcode in {"add", "sub", "mul", "div"}:
        if opcode == "div" and args[1] == 0:
            raise RuntimeErrorBase("division by zero")
        env[operation.outputs[0]] = {"add": args[0] + args[1], "sub": args[0] - args[1], "mul": args[0] * args[1], "div": args[0] / args[1]}[opcode]
        return None
    if opcode in {"cmp_eq", "cmp_lt", "cmp_ge", "cmp_le", "cmp_gt", "cmp_ne"}:
        env[operation.outputs[0]] = {
            "cmp_eq": args[0] == args[1], "cmp_lt": args[0] < args[1], "cmp_ge": args[0] >= args[1],
            "cmp_le": args[0] <= args[1], "cmp_gt": args[0] > args[1], "cmp_ne": args[0] != args[1],
        }[opcode]
        return None
    if opcode in {"and", "or"}:
        env[operation.outputs[0]] = (bool(args[0]) and bool(args[1])) if opcode == "and" else (bool(args[0]) or bool(args[1]))
        return None
    if opcode == "not":
        env[operation.outputs[0]] = not bool(args[0])
        return None
    if opcode == "branch":
        return attrs["true"] if bool(args[0]) else attrs["false"]
    if opcode == "return":
        return args[0] if args else None
    raise RuntimeErrorBase(f"unsupported operation: {opcode}")


def execute(function: FunctionIR, arguments: dict[str, Any] | None = None) -> Any:
    """Execute a semantically validated FunctionIR with conditional control flow."""
    try:
        validate_function(function)
    except SemanticValidationError as exc:
        raise RuntimeErrorBase(str(exc)) from exc
    env = dict(arguments or {})
    missing = [name for name in function.parameters if name not in env]
    if missing:
        raise RuntimeErrorBase(f"missing argument: {missing[0]}")
    blocks = {block.name: block for block in function.blocks}
    current = function.blocks[0].name
    for _ in range(100_000):
        block = blocks[current]
        for operation in block.operations:
            result = _execute_operation(operation, env)
            if operation.opcode == "return":
                return result
            if operation.opcode == "branch":
                current = result
                break
        else:
            if not block.successors:
                raise RuntimeErrorBase(f"function ended without return: {function.name}")
            if len(block.successors) != 1:
                raise RuntimeErrorBase("non-branch block requires one successor")
            current = block.successors[0]
    raise RuntimeErrorBase("execution step limit exceeded")


def execute_module(module: ModuleIR, entry: str, arguments: dict[str, Any] | None = None) -> Any:
    """Execute a named function from a validated module."""
    try:
        validate_module(module)
    except SemanticValidationError as exc:
        raise RuntimeErrorBase(str(exc)) from exc
    function = next((candidate for candidate in module.functions if candidate.name == entry), None)
    if function is None:
        raise RuntimeErrorBase(f"entry function not found: {entry}")
    return execute(function, arguments)
