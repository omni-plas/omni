"""Portable stack-frame model for the Omni bootstrap runtime."""

from __future__ import annotations

from dataclasses import dataclass


class StackModelError(ValueError):
    pass


@dataclass(frozen=True)
class StackSlot:
    name: str
    offset: int
    size: int
    alignment: int = 1


@dataclass(frozen=True)
class StackFrame:
    slots: tuple[StackSlot, ...]
    size: int

    def offset_of(self, name: str) -> int:
        for slot in self.slots:
            if slot.name == name:
                return slot.offset
        raise StackModelError(f"unknown stack slot: {name}")


def layout_stack_slots(slots: list[tuple[str, int, int]], *, base_alignment: int = 16) -> StackFrame:
    if base_alignment <= 0 or base_alignment & (base_alignment - 1):
        raise StackModelError("base alignment must be a positive power of two")
    offset = 0
    result: list[StackSlot] = []
    names: set[str] = set()
    for name, size, alignment in slots:
        if not name or name in names:
            raise StackModelError(f"duplicate or empty stack slot: {name!r}")
        if size <= 0:
            raise StackModelError(f"invalid stack slot size: {name}")
        if alignment <= 0 or alignment & (alignment - 1):
            raise StackModelError(f"invalid stack slot alignment: {name}")
        offset = (offset + alignment - 1) & ~(alignment - 1)
        result.append(StackSlot(name, offset, size, alignment))
        names.add(name)
        offset += size
    frame_size = (offset + base_alignment - 1) & ~(base_alignment - 1)
    return StackFrame(tuple(result), frame_size)
