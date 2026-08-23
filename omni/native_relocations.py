"""Resolve relative x86-64 branch relocations after code layout."""
from __future__ import annotations
from dataclasses import dataclass
import struct

@dataclass(frozen=True)
class Relocation:
    offset:int
    target:int
    size:int=1

def apply_rel8(code:bytearray, relocations):
    for r in relocations:
        delta=r.target-(r.offset+r.size)
        if not -128 <= delta <= 127: raise ValueError("relative branch out of range")
        code[r.offset:r.offset+r.size]=struct.pack("<b",delta)
    return code
