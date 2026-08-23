"""Target-neutral memory model used by the Omni IR and bootstrap compiler."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class MemoryModelError(ValueError):
    pass


@dataclass(frozen=True)
class MemoryObject:
    address: int
    size: int
    alignment: int = 1
    mutable: bool = True

    def validate(self) -> None:
        if self.address < 0 or self.size < 0:
            raise MemoryModelError("memory address and size must be non-negative")
        if self.alignment <= 0 or self.alignment & (self.alignment - 1):
            raise MemoryModelError("alignment must be a positive power of two")


class Memory:
    """Deterministic byte-addressable memory for portable execution and tests."""

    def __init__(self) -> None:
        self._objects: dict[int, bytearray] = {}
        self._next = 0x10000

    def allocate(self, size: int, *, alignment: int = 8, mutable: bool = True) -> MemoryObject:
        if size < 0:
            raise MemoryModelError("allocation size must be non-negative")
        if alignment <= 0 or alignment & (alignment - 1):
            raise MemoryModelError("alignment must be a positive power of two")
        address = (self._next + alignment - 1) & ~(alignment - 1)
        self._next = address + max(size, 1)
        self._objects[address] = bytearray(size)
        obj = MemoryObject(address, size, alignment, mutable)
        obj.validate()
        return obj

    def _locate(self, address: int, size: int) -> tuple[bytearray, int]:
        if size < 0:
            raise MemoryModelError("access size must be non-negative")
        for base, data in self._objects.items():
            if base <= address and address + size <= base + len(data):
                return data, address - base
        raise MemoryModelError(f"invalid memory access at 0x{address:x} size {size}")

    def load(self, address: int, size: int, *, signed: bool = False) -> int:
        data, offset = self._locate(address, size)
        return int.from_bytes(data[offset:offset + size], "little", signed=signed)

    def store(self, address: int, value: int, size: int) -> None:
        data, offset = self._locate(address, size)
        if size == 0:
            return
        if value < 0:
            value &= (1 << (size * 8)) - 1
        data[offset:offset + size] = int(value).to_bytes(size, "little", signed=False)

    def read_bytes(self, address: int, size: int) -> bytes:
        data, offset = self._locate(address, size)
        return bytes(data[offset:offset + size])

    def write_bytes(self, address: int, value: bytes) -> None:
        data, offset = self._locate(address, len(value))
        data[offset:offset + len(value)] = value
