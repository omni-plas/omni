"""Target-neutral linear-scan register and spill planner for Omni IR values."""
from __future__ import annotations
from dataclasses import dataclass
from .ir import FunctionIR

class RegisterAllocationError(ValueError):
    pass

@dataclass(frozen=True)
class LiveInterval:
    value: str
    start: int
    end: int
    def validate(self):
        if not self.value.strip() or self.start < 0 or self.end < self.start:
            raise RegisterAllocationError("invalid live interval")

@dataclass(frozen=True)
class Allocation:
    registers: dict[str, int]
    spills: dict[str, int]
    stack_size: int


def compute_intervals(fn: FunctionIR) -> tuple[LiveInterval, ...]:
    positions: dict[str, list[int]] = {}
    pos = 0
    for block in fn.blocks:
        for op in block.operations:
            for name in op.inputs + op.outputs:
                positions.setdefault(name, []).append(pos)
            pos += 1
    intervals = [LiveInterval(name, min(points), max(points)) for name, points in positions.items()]
    for interval in intervals: interval.validate()
    return tuple(sorted(intervals, key=lambda item: (item.start, item.end, item.value)))


def allocate(fn: FunctionIR, registers: tuple[int, ...]) -> Allocation:
    if not registers:
        raise RegisterAllocationError("at least one register is required")
    active: list[LiveInterval] = []
    assigned: dict[str, int] = {}
    spills: dict[str, int] = {}
    next_slot = 0
    for current in compute_intervals(fn):
        active = [item for item in active if item.end >= current.start]
        used = {assigned[item.value] for item in active if item.value in assigned}
        free = [reg for reg in registers if reg not in used]
        if free:
            assigned[current.value] = free[0]
            active.append(current)
            active.sort(key=lambda item: item.end)
            continue
        victim = max(active, key=lambda item: item.end) if active else current
        if victim.end > current.end and victim.value in assigned:
            spills[victim.value] = next_slot; next_slot += 8
            assigned[current.value] = assigned.pop(victim.value)
            active.remove(victim); active.append(current); active.sort(key=lambda item: item.end)
        else:
            spills[current.value] = next_slot; next_slot += 8
    return Allocation(assigned, spills, next_slot)
