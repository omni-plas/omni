"""Encode outgoing stack argument stores through RSP-relative addressing."""
from __future__ import annotations
import struct
from .native_machine_ops import MachineEncodingError

def store_rsp8(src, offset):
    if not 0 <= src <= 15: raise MachineEncodingError('register out of range')
    if not 0 <= offset <= 127: raise MachineEncodingError('stack offset out of supported range')
    rex=bytes([0x48 | ((src>>3)<<2)])
    return rex+b'\x89'+bytes([0x44|((src&7)<<3),0x24,offset])

def sub_rsp8(size):
    if size < 0 or size > 127 or size % 8: raise ValueError('stack adjustment must be an aligned small positive size')
    return b'\x48\x83\xec'+struct.pack('<B',size)

def add_rsp8(size):
    if size < 0 or size > 127 or size % 8: raise ValueError('stack adjustment must be an aligned small positive size')
    return b'\x48\x83\xc4'+struct.pack('<B',size)
