"""Validated x86-64 operation encoders used by native lowering."""
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

def add_rr(dst, src): return _rr(b"\x01", dst, src)
def sub_rr(dst, src): return _rr(b"\x29", dst, src)
def imul_rr(dst, src): return _rr(b"\x0f\xaf", dst, src)

def cmp_rr(left, right): return _rr(b"\x39", left, right)
def test_rr(left, right): return _rr(b"\x85", left, right)

def _rr(op, dst, src):
    _check(dst); _check(src)
    return rex(r=src>>3,b=dst>>3)+op+bytes([0xC0|((src&7)<<3)|(dst&7)])

def jmp_rel8(delta):
    if not -128 <= delta <= 127: raise MachineEncodingError("short jump out of range")
    return b"\xeb"+struct.pack("<b",delta)

def je_rel8(delta):
    if not -128 <= delta <= 127: raise MachineEncodingError("short jump out of range")
    return b"\x74"+struct.pack("<b",delta)

def jne_rel8(delta):
    if not -128 <= delta <= 127: raise MachineEncodingError("short jump out of range")
    return b"\x75"+struct.pack("<b",delta)

def load_rbp8(dst, offset):
    _check(dst)
    if not -128 <= offset <= 127: raise MachineEncodingError("RBP displacement out of range")
    return rex(r=dst>>3)+b"\x8b"+bytes([0x45|((dst&7)<<3), offset & 255])

def store_rbp8(offset, src):
    _check(src)
    if not -128 <= offset <= 127: raise MachineEncodingError("RBP displacement out of range")
    return rex(r=src>>3)+b"\x89"+bytes([0x45|((src&7)<<3), offset & 255])
