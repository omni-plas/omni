"""x86-64 RBP-relative spill/reload encoders."""
from __future__ import annotations

def _check(r):
    if not 0 <= r <= 15: raise ValueError("register out of range")

def _rex(r=0,b=0): return bytes([0x40|(r<<2)|b])

def store_rbp(offset:int, src:int)->bytes:
    _check(src)
    if offset >= 0 or offset < -128: raise ValueError("offset must fit signed disp8 and be negative")
    return _rex(r=(src>>3)&1)+b"\x89"+bytes([0x45, offset & 0xff]) if (src&7)!=4 else _rex(r=(src>>3)&1)+b"\x89"+bytes([0x65, offset & 0xff])

def load_rbp(dst:int, offset:int)->bytes:
    _check(dst)
    if offset >= 0 or offset < -128: raise ValueError("offset must fit signed disp8 and be negative")
    return _rex(r=(dst>>3)&1)+b"\x8b"+bytes([0x45|((dst&7)<<3), offset & 0xff])
