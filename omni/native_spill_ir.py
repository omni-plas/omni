"""Materialize spilled IR values into registers around operations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_memory_ops import load_rbp, store_rbp
from .native_machine_ops import mov_rr

@dataclass(frozen=True)
class MaterializedLocation:
    name: str
    register: int
    spill_offset: int | None


def materialize_locations(resolved, scratch_register: int = 11):
    """Assign every value a usable register while retaining spill metadata."""
    out=[]
    for value in resolved:
        if value.register is not None:
            out.append(MaterializedLocation(value.name, value.register, None))
        elif value.rbp_offset is not None:
            out.append(MaterializedLocation(value.name, scratch_register, value.rbp_offset))
        else:
            raise ValueError(f"value has no location: {value.name}")
    return tuple(out)


def reload(value: MaterializedLocation) -> bytes:
    if value.spill_offset is None:
        return b""
    return load_rbp(value.register, value.spill_offset)


def spill(value: MaterializedLocation) -> bytes:
    if value.spill_offset is None:
        return b""
    return store_rbp(value.spill_offset, value.register)
