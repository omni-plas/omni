"""Deterministic semantic-IR optimization passes."""

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
        reachable.add(name)
        stack.extend(by_name[name].successors)
    return tuple(block for block in blocks if block.name in reachable)


def _fold_identity_operations(block: BasicBlock) -> BasicBlock:
    """Remove identity operations while preserving all other operations."""
    aliases: dict[str, str] = {}
    result: list[Operation] = []
    for op in block.operations:
        if op.opcode == "identity" and len(op.inputs) == 1 and len(op.outputs) == 1:
            aliases[op.outputs[0]] = op.inputs[0]
            continue
        inputs = tuple(aliases.get(value, value) for value in op.inputs)
        result.append(replace(op, inputs=inputs))
    return replace(block, operations=tuple(result))


def optimize_module(module: ModuleIR) -> ModuleIR:
    """Apply semantics-preserving deterministic optimizations."""
    optimized_functions: list[FunctionIR] = []
    for function in module.functions:
        blocks = _remove_unreachable(function.blocks)
        blocks = tuple(_fold_identity_operations(block) for block in blocks)
        optimized_functions.append(replace(function, blocks=blocks))
    result = replace(module, functions=tuple(optimized_functions))
    result.validate()
    return result
