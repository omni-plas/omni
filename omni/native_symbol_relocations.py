"""Symbol-named relocations resolved by the internal linker."""
from __future__ import annotations
from dataclasses import dataclass
import struct

@dataclass(frozen=True)
class SymbolCallRelocation:
    immediate_offset: int
    instruction_end: int
    symbol: str

@dataclass(frozen=True)
class SymbolDataRelocation:
    immediate_offset: int
    symbol: str
    width: int = 8

def apply_symbol_relocations(code: bytearray, calls=(), data=(), symbols=None):
    symbols = {} if symbols is None else symbols
    for r in calls:
        if r.symbol not in symbols: raise KeyError(f"unresolved symbol: {r.symbol}")
        delta = symbols[r.symbol] - r.instruction_end
        code[r.immediate_offset:r.immediate_offset+4] = struct.pack('<i', delta)
    for r in data:
        if r.symbol not in symbols: raise KeyError(f"unresolved symbol: {r.symbol}")
        if r.width == 8:
            code[r.immediate_offset:r.immediate_offset+8] = struct.pack('<Q', symbols[r.symbol])
        elif r.width == 4:
            code[r.immediate_offset:r.immediate_offset+4] = struct.pack('<I', symbols[r.symbol])
        else:
            raise ValueError('data relocation width must be 4 or 8')
    return code
