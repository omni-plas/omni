"""Deterministic register pool used by native lowering."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RegisterPool:
    registers: tuple[int, ...]
    _free: list[int] | None = None

    def __post_init__(self):
        if not self.registers or len(set(self.registers)) != len(self.registers):
            raise ValueError("register pool must contain unique registers")
        self._free = list(self.registers)

    def acquire(self) -> int:
        if not self._free:
            raise RuntimeError("register pool exhausted")
        return self._free.pop(0)

    def release(self, register: int) -> None:
        if register not in self.registers or register in self._free:
            raise ValueError("invalid or already-free register")
        self._free.append(register)
        self._free.sort(key=self.registers.index)

    @property
    def available(self) -> tuple[int, ...]:
        return tuple(self._free or ())
