"""Target-neutral memory operation constructors for Omni IR."""
from __future__ import annotations
from .ir import Operation

class MemoryIROperationError(ValueError):
    pass

def alloc(output: str, size: str, *, alignment: int = 8) -> Operation:
    if alignment <= 0 or alignment & (alignment - 1):
        raise MemoryIROperationError("alignment must be a positive power of two")
    return Operation("alloc", inputs=(size,), outputs=(output,), attributes={"alignment": alignment})

def load(output: str, pointer: str, *, size: int = 8, signed: bool = False) -> Operation:
    if size not in (1, 2, 4, 8): raise MemoryIROperationError("load size must be 1, 2, 4 or 8")
    return Operation("load", inputs=(pointer,), outputs=(output,), attributes={"size": size, "signed": signed})

def store(pointer: str, value: str, *, size: int = 8) -> Operation:
    if size not in (1, 2, 4, 8): raise MemoryIROperationError("store size must be 1, 2, 4 or 8")
    return Operation("store", inputs=(pointer, value), attributes={"size": size})

def ptr_add(output: str, pointer: str, offset: str) -> Operation:
    return Operation("ptr_add", inputs=(pointer, offset), outputs=(output,))

def free(pointer: str) -> Operation:
    return Operation("free", inputs=(pointer,))
