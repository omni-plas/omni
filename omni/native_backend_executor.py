"""Prepare a native function for code generation from the shared allocator."""
from __future__ import annotations
from dataclasses import dataclass
from .native_backend_plan import NativeBackendPlan, build_plan
from .native_spill_codegen import load_rbp, store_rbp

@dataclass(frozen=True)
class PreparedValue:
    name: str
    register: int | None
    rbp_offset: int | None

@dataclass(frozen=True)
class PreparedFunction:
    plan: NativeBackendPlan
    values: tuple[PreparedValue, ...]

def prepare_function(function, registers: tuple[int, ...]) -> PreparedFunction:
    plan = build_plan(function, registers)
    values = tuple(
        PreparedValue(name, loc.register, None if loc.spill_offset is None else -(loc.spill_offset + 8))
        for name, loc in sorted(plan.locations.items())
    )
    return PreparedFunction(plan, values)

def emit_reload(value: PreparedValue, scratch_register: int) -> bytes:
    if value.rbp_offset is None: return b""
    return load_rbp(scratch_register, value.rbp_offset)

def emit_spill(value: PreparedValue, register: int) -> bytes:
    if value.rbp_offset is None: return b""
    return store_rbp(value.rbp_offset, register)
