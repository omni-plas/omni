"""Lower allocator spill locations into concrete memory operations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_memory_ops import load_rbp, store_rbp

@dataclass(frozen=True)
class SpillAction:
    kind: str
    offset: int
    register: int

def lower_spill(offset:int, register:int)->SpillAction:
    return SpillAction("spill", offset, register)

def lower_reload(offset:int, register:int)->SpillAction:
    return SpillAction("reload", offset, register)

def encode_spill_action(action:SpillAction)->bytes:
    if action.kind == "spill": return store_rbp(action.offset, action.register)
    if action.kind == "reload": return load_rbp(action.register, action.offset)
    raise ValueError("unknown spill action")
