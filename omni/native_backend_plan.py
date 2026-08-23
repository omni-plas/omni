"""Plan native backend integration without changing the existing emitter yet."""
from __future__ import annotations
from dataclasses import dataclass
from .native_allocator_bridge import NativeAllocationPlan, plan_native_allocation
from .native_spill_codegen import load_rbp, store_rbp

@dataclass(frozen=True)
class NativeValueLocation:
    register: int | None = None
    spill_offset: int | None = None

@dataclass(frozen=True)
class NativeBackendPlan:
    allocation: NativeAllocationPlan
    locations: dict[str, NativeValueLocation]

def build_plan(function, registers: tuple[int, ...]) -> NativeBackendPlan:
    allocation = plan_native_allocation(function, registers)
    locations = {name: NativeValueLocation(register=reg) for name, reg in allocation.registers.items()}
    locations.update({name: NativeValueLocation(spill_offset=offset) for name, offset in allocation.spills.items()})
    return NativeBackendPlan(allocation, locations)

def encode_reload(location: NativeValueLocation, register: int) -> bytes:
    if location.spill_offset is None: return b""
    return load_rbp(register, -location.spill_offset - 8)

def encode_spill(location: NativeValueLocation, register: int) -> bytes:
    if location.spill_offset is None: return b""
    return store_rbp(-location.spill_offset - 8, register)
