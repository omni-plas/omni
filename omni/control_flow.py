"""Control-flow analysis utilities for Omni IR.

The analysis is target-neutral and deliberately independent of Python's compiler.
It validates reachable blocks, predecessor relationships, and terminator shape,
providing the foundation for native branch lowering and self-hosting.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ir import BasicBlock, FunctionIR


class ControlFlowError(ValueError):
    pass


@dataclass(frozen=True)
class ControlFlowGraph:
    entry: str
    blocks: tuple[str, ...]
    predecessors: dict[str, tuple[str, ...]]
    reachable: tuple[str, ...]


def _terminator(block: BasicBlock) -> str | None:
    if not block.operations:
        return None
    return block.operations[-1].opcode


def analyze_control_flow(function: FunctionIR) -> ControlFlowGraph:
    function.validate()
    names = tuple(block.name for block in function.blocks)
    by_name = {block.name: block for block in function.blocks}
    entry = names[0]
    predecessors: dict[str, list[str]] = {name: [] for name in names}

    for block in function.blocks:
        terminator = _terminator(block)
        if terminator in {"return", "ret"} and block.successors:
            raise ControlFlowError(f"return block has successors: {block.name}")
        if terminator in {"branch", "cond_branch", "jump"} and not block.successors:
            raise ControlFlowError(f"branch block has no successors: {block.name}")
        if terminator not in {None, "return", "ret", "branch", "cond_branch", "jump"} and block.successors:
            raise ControlFlowError(f"block {block.name} has successors without a control-flow terminator")
        for successor in block.successors:
            predecessors[successor].append(block.name)

    seen: set[str] = set()
    stack = [entry]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(reversed(by_name[current].successors))

    unreachable = [name for name in names if name not in seen]
    if unreachable:
        raise ControlFlowError(f"unreachable blocks: {', '.join(unreachable)}")

    return ControlFlowGraph(
        entry=entry,
        blocks=names,
        predecessors={name: tuple(preds) for name, preds in predecessors.items()},
        reachable=tuple(name for name in names if name in seen),
    )
