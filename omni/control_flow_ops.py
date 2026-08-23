"""Helpers for explicit control-flow operations in Omni IR."""

from __future__ import annotations

from .ir import Operation


def branch(condition: str, true_block: str, false_block: str) -> Operation:
    return Operation("branch", inputs=(condition,), attributes={"true": true_block, "false": false_block})


def jump(target: str) -> Operation:
    return Operation("jump", attributes={"target": target})


def compare(operator: str, left: str, right: str, output: str) -> Operation:
    if operator not in {"eq", "ne", "lt", "le", "gt", "ge"}:
        raise ValueError(f"unsupported comparison: {operator}")
    return Operation("compare", inputs=(left, right), outputs=(output,), attributes={"operator": operator})
