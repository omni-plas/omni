"""Runtime representation of native spill/reload actions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SpillSlot:
    value: str
    offset: int

@dataclass(frozen=True)
class ReloadAction:
    value: str
    register: int
    offset: int

@dataclass(frozen=True)
class SpillAction:
    value: str
    register: int
    offset: int


def make_spill(value: str, register: int, offset: int) -> SpillAction:
    if not value.strip() or register < 0 or offset < 0:
        raise ValueError("invalid spill action")
    return SpillAction(value, register, offset)


def make_reload(value: str, register: int, offset: int) -> ReloadAction:
    if not value.strip() or register < 0 or offset < 0:
        raise ValueError("invalid reload action")
    return ReloadAction(value, register, offset)
