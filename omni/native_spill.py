"""Translate target-neutral register allocations into x86-64 spill actions."""
from __future__ import annotations
from dataclasses import dataclass
from .register_alloc import Allocation

class NativeSpillError(ValueError):
    pass

@dataclass(frozen=True)
class SpillAction:
    value: str
    stack_offset: int
    kind: str

@dataclass(frozen=True)
class SpillPlan:
    stack_size: int
    actions: tuple[SpillAction, ...]


def plan_spills(allocation: Allocation, *, alignment: int = 16) -> SpillPlan:
    if alignment <= 0 or alignment & (alignment - 1):
        raise NativeSpillError("alignment must be a positive power of two")
    if any(offset < 0 or offset % 8 for offset in allocation.spills.values()):
        raise NativeSpillError("spill slots must be non-negative 8-byte aligned offsets")
    size = (allocation.stack_size + alignment - 1) & ~(alignment - 1)
    actions = tuple(
        SpillAction(value, offset, "spill")
        for value, offset in sorted(allocation.spills.items(), key=lambda item: (item[1], item[0]))
    )
    return SpillPlan(size, actions)


def stack_offset_from_rbp(offset: int) -> int:
    if offset < 0 or offset % 8:
        raise NativeSpillError("spill offset must be a non-negative multiple of 8")
    return -(offset + 8)
