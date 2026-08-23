"""Native-facing allocation contract derived from Omni's target-neutral allocator."""
from __future__ import annotations
from dataclasses import dataclass
from .register_alloc import Allocation, allocate

@dataclass(frozen=True)
class NativeAllocationPlan:
    registers: dict[str, int]
    spills: dict[str, int]
    stack_size: int


def plan_native_allocation(function, registers: tuple[int, ...]) -> NativeAllocationPlan:
    result: Allocation = allocate(function, registers)
    return NativeAllocationPlan(dict(result.registers), dict(result.spills), result.stack_size)
