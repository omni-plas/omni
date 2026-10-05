"""x86-64 stack spill/reload encoders used by the Omni native backend."""
from __future__ import annotations

class NativeSpillCodegenError(ValueError):
    pass

def _check(reg: int) -> None:
    if not 0 <= reg <= 15:
        raise NativeSpillCodegenError("invalid register")

def _check_offset(offset: int) -> None:
    if offset < -128 or offset > 127:
        raise NativeSpillCodegenError("stack displacement must fit signed byte")
    if offset % 8:
        raise NativeSpillCodegenError("stack displacement must be 8-byte aligned")

def _rex(w=1, r=0, b=0):
    return bytes([0x40 | (w << 3) | (r << 2) | b])

def load_rbp(reg: int, offset: int) -> bytes:
    _check(reg); _check_offset(offset)
    rex = _rex(r=reg >> 3)
    modrm = 0x40 | ((reg & 7) << 3) | 5
    return rex + b"\x8b" + bytes([modrm, offset & 0xff])

def store_rbp(offset: int, reg: int) -> bytes:
    _check(reg); _check_offset(offset)
    rex = _rex(r=reg >> 3)
    modrm = 0x40 | ((reg & 7) << 3) | 5
    return rex + b"\x89" + bytes([modrm, offset & 0xff])

def prologue(stack_size: int = 0) -> bytes:
    if stack_size < 0 or stack_size > 127 or stack_size % 8:
        raise NativeSpillCodegenError("stack size must be a non-negative 8-byte multiple")
    code = b"\x55\x48\x89\xe5"
    if stack_size:
        code += b"\x48\x83\xec" + bytes([stack_size])
    return code

def epilogue(stack_size: int = 0) -> bytes:
    if stack_size < 0 or stack_size > 127 or stack_size % 8:
        raise NativeSpillCodegenError("stack size must be a non-negative 8-byte multiple")
    code = b""
    if stack_size:
        code += b"\x48\x83\xc4" + bytes([stack_size])
    return code + b"\x5d\xc3"
