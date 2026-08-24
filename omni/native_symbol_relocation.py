"""Symbol-relative relocation records used by the native linker."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SymbolRelocation:
    kind: str
    immediate_offset: int
    symbol: str
    addend: int = 0
    instruction_end: int|None = None
