"""Bridge target-neutral allocation results to native code generation."""
from __future__ import annotations
from dataclasses import dataclass
from .register_alloc import Allocation
from .native_spill import plan_spills

@dataclass(frozen=True)
class NativeAllocation:
    registers: dict[str,int]
    spill_offsets: dict[str,int]
    stack_size: int

def adapt_allocation(allocation: Allocation) -> NativeAllocation:
    plan = plan_spills(allocation)
    return NativeAllocation(dict(allocation.registers), {a.value:a.stack_offset for a in plan.actions}, plan.stack_size)
