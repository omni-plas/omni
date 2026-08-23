"""Plan prologue/epilogue metadata for native Omni functions."""
from __future__ import annotations
from dataclasses import dataclass
from .abi import SYSV_AMD64

@dataclass(frozen=True)
class NativeFrame:
    local_size: int
    saved_registers: tuple[int, ...]
    stack_size: int


def align_up(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


def plan_frame(local_size: int, saved_registers: tuple[int, ...] = ()) -> NativeFrame:
    if local_size < 0:
        raise ValueError("local_size must be non-negative")
    unknown = [r for r in saved_registers if r not in SYSV_AMD64.callee_saved_registers]
    if unknown:
        raise ValueError(f"registers are not callee-saved: {unknown}")
    raw = local_size + 8 * len(saved_registers)
    return NativeFrame(local_size, saved_registers, align_up(raw, SYSV_AMD64.stack_alignment))
