"""Patch fixed-width image-relative global references."""
from __future__ import annotations
import struct
from dataclasses import dataclass

@dataclass(frozen=True)
class GlobalRef:
    immediate_offset:int
    target_offset:int
    width:int=4

def apply_global_refs(code:bytearray, refs, base_offset=0):
    for ref in refs:
        value=base_offset+ref.target_offset
        if ref.width==4:
            code[ref.immediate_offset:ref.immediate_offset+4]=struct.pack('<I',value)
        elif ref.width==8:
            code[ref.immediate_offset:ref.immediate_offset+8]=struct.pack('<Q',value)
        else:
            raise ValueError('global reference width must be 4 or 8')
    return code
