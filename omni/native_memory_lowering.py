"""Lower stack-backed native loads and stores."""
from __future__ import annotations
from dataclasses import dataclass
from .native_machine_ops import load_rbp8, store_rbp8

@dataclass(frozen=True)
class MemoryOp:
    kind:str
    register:int
    offset:int

def load_stack(register:int,offset:int)->MemoryOp:
    return MemoryOp("load",register,offset)

def store_stack(register:int,offset:int)->MemoryOp:
    return MemoryOp("store",register,offset)

def encode_memory(op:MemoryOp)->bytes:
    if op.kind=="load": return load_rbp8(op.register,op.offset)
    if op.kind=="store": return store_rbp8(op.offset,op.register)
    raise ValueError("unknown memory operation")
