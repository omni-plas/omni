"""Small target-specific native primitives for Omni memory operations.

This module intentionally exposes encoding helpers independently of the full
function compiler so the bootstrap compiler can grow memory support without
coupling the target-neutral IR to x86-64 details.
"""
from __future__ import annotations
import struct

class NativeMemoryCodegenError(ValueError):
    pass


def _rex(w=1, r=0, b=0):
    return bytes([0x40 | (w << 3) | (r << 2) | b])


def mov_imm64(reg: int, value: int) -> bytes:
    if not 0 <= reg <= 15: raise NativeMemoryCodegenError("invalid register")
    return _rex(b=reg >> 3) + bytes([0xB8 + (reg & 7)]) + struct.pack("<Q", value & 0xffffffffffffffff)


def mov_mem64(dst: int, base: int, offset: int = 0) -> bytes:
    if not all(0 <= r <= 15 for r in (dst, base)): raise NativeMemoryCodegenError("invalid register")
    if not -128 <= offset <= 127: raise NativeMemoryCodegenError("offset must fit signed byte")
    rex = _rex(r=dst >> 3, b=base >> 3)
    modrm = 0x40 | ((dst & 7) << 3) | (base & 7)
    if (base & 7) == 4:
        raise NativeMemoryCodegenError("rsp/r12 SIB addressing requires dedicated encoder")
    return rex + b"\x48"[0:0] + b"\x8b" + bytes([modrm, offset & 0xff])


def store_mem64(base: int, src: int, offset: int = 0) -> bytes:
    if not all(0 <= r <= 15 for r in (base, src)): raise NativeMemoryCodegenError("invalid register")
    if not -128 <= offset <= 127: raise NativeMemoryCodegenError("offset must fit signed byte")
    rex = _rex(r=src >> 3, b=base >> 3)
    modrm = 0x40 | ((src & 7) << 3) | (base & 7)
    if (base & 7) == 4:
        raise NativeMemoryCodegenError("rsp/r12 SIB addressing requires dedicated encoder")
    return rex + b"\x89" + bytes([modrm, offset & 0xff])


def add_imm64(reg: int, value: int) -> bytes:
    if not 0 <= reg <= 15 or not -(2**31) <= value < 2**31:
        raise NativeMemoryCodegenError("invalid add immediate")
    rex = _rex(b=reg >> 3)
    return rex + b"\x81" + bytes([0xC0 | (reg & 7)]) + struct.pack("<i", value)
