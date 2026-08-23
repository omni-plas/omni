"""Small, validated x86-64 operation encoders used by native lowering."""
from __future__ import annotations
import struct

class MachineEncodingError(ValueError): pass

def _check(r):
    if not 0 <= r <= 15: raise MachineEncodingError("register out of range")

def rex(w=1,r=0,b=0): return bytes([0x40 | (w<<3) | (r<<2) | b])

def mov_rr(dst, src):
    _check(dst); _check(src)
    return rex(r=src>>3,b=dst>>3)+b"\x89"+bytes([0xC0|((src&7)<<3)|(dst&7)])

def mov_imm64(dst, value):
    _check(dst)
    return rex(b=dst>>3)+bytes([0xB8+(dst&7)])+struct.pack("<Q", value & 0xffffffffffffffff)

def add_rr(dst, src):
    return _rr(b"\x01", dst, src)

def sub_rr(dst, src):
    return _rr(b"\x29", dst, src)

def imul_rr(dst, src):
    return _rr(b"\x0f\xaf", dst, src)

def _rr(op, dst, src):
    _check(dst); _check(src)
    return rex(r=src>>3,b=dst>>3)+op+bytes([0xC0|((src&7)<<3)|(dst&7)])
