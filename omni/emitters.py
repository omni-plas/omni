"""Concrete emitters for the portable semantic IR."""

from __future__ import annotations

from .ir import FunctionIR, ModuleIR
from .targets import TargetDescriptor


class EmitterError(ValueError):
    """Raised when a target emitter cannot represent the requested IR."""


def _c_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)


def emit_c(module: ModuleIR, target: TargetDescriptor | None = None) -> bytes:
    """Emit a freestanding C99 translation unit for the portable IR subset."""
    if target is not None and target.platform not in {"c", "native", "portable-c"}:
        raise EmitterError(f"C emitter cannot target {target.identity()}")
    module.validate()
    if not module.functions:
        raise EmitterError("module contains no functions")
    lines = ["#include <stdint.h>", "#include <stdbool.h>", "#include <stdio.h>", ""]
    for function in module.functions:
        lines.extend(_emit_c_function(function))
        lines.append("")
    entry = module.functions[0]
    if entry.parameters:
        raise EmitterError("C executable wrapper requires a zero-argument first function")
    lines.extend([
        "int main(void) {",
        f"    printf(\"%lld\\n\", (long long){_c_name(entry.name)}());",
        "    return 0;",
        "}",
    ])
    return "\n".join(lines).encode("utf-8")


def _emit_c_function(function: FunctionIR) -> list[str]:
    if len(function.blocks) != 1:
        raise EmitterError("C reference emitter currently requires one basic block")
    params = ", ".join(f"int64_t {_c_name(name)}" for name in function.parameters)
    lines = [f"int64_t {_c_name(function.name)}({params}) {{"]
    declared = set(function.parameters)
    for op in function.blocks[0].operations:
        if op.opcode == "const":
            if len(op.outputs) != 1 or "value" not in op.attributes:
                raise EmitterError("const requires one output and value")
            value = op.attributes["value"]
            if isinstance(value, bool) or not isinstance(value, int):
                raise EmitterError("C const currently requires an integer value")
            name = _c_name(op.outputs[0])
            lines.append(f"    int64_t {name} = {value};")
            declared.add(op.outputs[0])
            continue
        if op.opcode in {"add", "sub", "mul", "div"}:
            if len(op.inputs) != 2 or len(op.outputs) != 1:
                raise EmitterError(f"{op.opcode} requires two inputs and one output")
            if any(name not in declared for name in op.inputs):
                raise EmitterError(f"undefined operand in {op.opcode}")
            symbol = {"add": "+", "sub": "-", "mul": "*", "div": "/"}[op.opcode]
            name = _c_name(op.outputs[0])
            lines.append(f"    int64_t {name} = {_c_name(op.inputs[0])} {symbol} {_c_name(op.inputs[1])};")
            declared.add(op.outputs[0])
            continue
        if op.opcode == "return":
            if len(op.inputs) != 1 or op.inputs[0] not in declared:
                raise EmitterError("return requires one defined input")
            lines.append(f"    return {_c_name(op.inputs[0])};")
            return lines
        raise EmitterError(f"unsupported C operation: {op.opcode}")
    raise EmitterError(f"function has no return: {function.name}")
