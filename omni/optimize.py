"""Deterministic semantics-preserving optimization passes."""

from __future__ import annotations

from dataclasses import replace

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation


def _remove_unreachable(blocks: tuple[BasicBlock, ...]) -> tuple[BasicBlock, ...]:
    if not blocks:
        return blocks
    by_name = {block.name: block for block in blocks}
    reachable: set[str] = set()
    stack = [blocks[0].name]
    while stack:
        name = stack.pop()
        if name in reachable:
            continue
        if name not in by_name:
            continue
        reachable.add(name)
        stack.extend(by_name[name].successors)
    return tuple(block for block in blocks if block.name in reachable)


def _fold_identity_operations(block: BasicBlock) -> BasicBlock:
    aliases: dict[str, str] = {}
    result: list[Operation] = []
    for op in block.operations:
        if op.opcode == "identity" and len(op.inputs) == 1 and len(op.outputs) == 1:
            aliases[op.outputs[0]] = aliases.get(op.inputs[0], op.inputs[0])
            continue
        inputs = tuple(aliases.get(value, value) for value in op.inputs)
        result.append(replace(op, inputs=inputs))
    return replace(block, operations=tuple(result))


def _fold_constants(block: BasicBlock) -> BasicBlock:
    constants: dict[str, object] = {}
    result: list[Operation] = []
    for op in block.operations:
        if op.opcode == "const" and len(op.outputs) == 1 and "value" in op.attributes:
            constants[op.outputs[0]] = op.attributes["value"]
            result.append(op)
            continue
        if op.opcode in {"add", "sub", "mul"} and len(op.inputs) == 2 and len(op.outputs) == 1:
            left, right = op.inputs
            if left in constants and right in constants and all(isinstance(constants[n], (int, float)) and not isinstance(constants[n], bool) for n in (left, right)):
                a, b = constants[left], constants[right]
                value = {"add": a + b, "sub": a - b, "mul": a * b}[op.opcode]
                folded = Operation("const", outputs=op.outputs, attributes={"value": value})
                constants[op.outputs[0]] = value
                result.append(folded)
                continue
        result.append(op)
    return replace(block, operations=tuple(result))


def optimize_module(module: ModuleIR) -> ModuleIR:
    """Apply deterministic reachability, identity, and constant-folding passes."""
    optimized_functions: list[FunctionIR] = []
    for function in module.functions:
        blocks = _remove_unreachable(function.blocks)
        blocks = tuple(_fold_identity_operations(block) for block in blocks)
        blocks = tuple(_fold_constants(block) for block in blocks)
        optimized_functions.append(replace(function, blocks=blocks))
    result = replace(module, functions=tuple(optimized_functions))
    result.validate()
    return result
