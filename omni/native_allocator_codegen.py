"""Translate shared allocation results into native lowering locations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocator_bridge import plan_native_allocation
from .native_lowering import ValueLocation

@dataclass(frozen=True)
class AllocatedNativeValue:
    name: str
    location: ValueLocation

@dataclass(frozen=True)
class AllocatedNativeFunction:
    name: str
    values: tuple[AllocatedNativeValue, ...]
    stack_size: int

def allocate_function(fn, registers=(3,4,5,10,11,12,13,14,15)) -> AllocatedNativeFunction:
    plan = plan_native_allocation(fn, tuple(registers))
    values = tuple([AllocatedNativeValue(n, ValueLocation(register=r)) for n,r in sorted(plan.registers.items())] + [AllocatedNativeValue(n, ValueLocation(stack_offset=o)) for n,o in sorted(plan.spills.items())])
    return AllocatedNativeFunction(fn.name, values, plan.stack_size)
