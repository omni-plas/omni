"""Deterministic linear-scan allocation for Omni virtual values."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Allocation:
    registers: dict[str,int]
    spills: dict[str,int]

def allocate(values, registers):
    values=tuple(dict.fromkeys(values)); registers=tuple(registers)
    assigned={}; spills={};
    for i,value in enumerate(values):
        if i < len(registers): assigned[value]=registers[i]
        else: spills[value]=(i-len(registers))*8
    return Allocation(assigned,spills)
