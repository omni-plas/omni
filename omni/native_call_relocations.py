"""Resolve direct x86-64 call rel32 relocations."""
from __future__ import annotations
from dataclasses import dataclass
import struct

@dataclass(frozen=True)
class CallRelocation:
    immediate_offset:int
    target_offset:int
    instruction_end:int

def apply_call_rel32(code:bytearray, relocations):
    for r in relocations:
        delta=r.target_offset-r.instruction_end
        code[r.immediate_offset:r.immediate_offset+4]=struct.pack("<i",delta)
    return code
