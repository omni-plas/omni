"""Control-flow analysis utilities for Omni IR."""

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
    names = tuple(block.name for block in function.blocks)
    by_name = {block.name: block for block in function.blocks}
    entry = names[0]
    predecessors: dict[str, list[str]] = {name: [] for name in names}

    for block in function.blocks:
        terminator = _terminator(block)
        if terminator in {"return", "ret"} and block.successors:
            raise ControlFlowError(f"return block has successors: {block.name}")
        if terminator in {"branch", "cond_branch", "jump"}:
            if not block.successors:
                raise ControlFlowError(f"branch block has no successors: {block.name}")
            if terminator == "branch" and len(block.successors) != 2:
                op = block.operations[-1]
                if len(block.successors) != 1 or "true" in op.attributes or "false" in op.attributes:
                    raise ControlFlowError(f"conditional branch requires two successors: {block.name}")
            if terminator == "jump" and len(block.successors) != 1:
                raise ControlFlowError(f"jump requires one successor: {block.name}")
        if terminator not in {None, "return", "ret", "branch", "cond_branch", "jump"} and block.successors:
            raise ControlFlowError(f"block {block.name} has successors without a control-flow terminator")
        if terminator == "branch":
            op = block.operations[-1]
            if op.opcode == "branch" and ("true" in op.attributes or "false" in op.attributes):
                true_target = op.attributes.get("true")
                false_target = op.attributes.get("false")
                if (true_target, false_target) != tuple(block.successors):
                    raise ControlFlowError(f"branch targets disagree with successors: {block.name}")
        if terminator == "jump":
            target = block.operations[-1].attributes.get("target")
            if target != block.successors[0]:
                raise ControlFlowError(f"jump target disagrees with successor: {block.name}")
        for successor in block.successors:
            if successor not in predecessors:
                raise ControlFlowError(f"unknown successor {successor!r} in {block.name!r}")
            predecessors[successor].append(block.name)

    function.validate()
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
