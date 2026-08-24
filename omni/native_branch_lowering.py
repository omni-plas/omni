"""Concrete short conditional branch encoders for native CFG lowering."""
from __future__ import annotations

def jz_rel8(delta:int)->bytes:
    if not -128 <= delta <= 127: raise ValueError('short branch displacement out of range')
    return b'\x74'+bytes([delta & 0xff])

def jnz_rel8(delta:int)->bytes:
    if not -128 <= delta <= 127: raise ValueError('short branch displacement out of range')
    return b'\x75'+bytes([delta & 0xff])

def jmp_rel8(delta:int)->bytes:
    if not -128 <= delta <= 127: raise ValueError('short branch displacement out of range')
    return b'\xeb'+bytes([delta & 0xff])
