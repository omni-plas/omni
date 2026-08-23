"""Emit a direct x86-64 relative call with a typed relocation."""
from __future__ import annotations
from .native_symbol_reloc import call_rel32, SymbolRelocation

def emit_call(symbol:str)->tuple[bytes,SymbolRelocation]:
    # E8 rel32; immediate begins at byte 1 and instruction ends at byte 5.
    return b'\xe8\x00\x00\x00\x00', call_rel32(1,symbol,5)
