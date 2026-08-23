"""Integration helpers for native function allocation and spill encoding."""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocator_bridge import NativeAllocationPlan, plan_native_allocation
from .native_spill_codegen import load_rbp, store_rbp

@dataclass(frozen=True)
class NativeSpillSequence:
    value: str
    register: int
    offset: int
    store_code: bytes
    reload_code: bytes

def build_spill_sequence(value: str, register: int, offset: int) -> NativeSpillSequence:
    return NativeSpillSequence(value, register, offset, store_rbp(offset, register), load_rbp(register, offset))

def plan_function(function, registers: tuple[int, ...]) -> NativeAllocationPlan:
    return plan_native_allocation(function, registers)
