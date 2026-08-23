"""Machine-code helpers for System V AMD64 argument and return movement."""
from __future__ import annotations
from .abi import SYSV_AMD64, ABIError

class NativeABICodegenError(ValueError): pass

def _rex(w=1,r=0,b=0): return bytes([0x40|(w<<3)|(r<<2)|b])
def mov_rr(dst:int,src:int)->bytes:
    if not 0<=dst<=15 or not 0<=src<=15: raise NativeABICodegenError("invalid register")
    return _rex(r=src>>3,b=dst>>3)+b"\x89"+bytes([0xC0|((src&7)<<3)|(dst&7)])

def move_integer_arguments(source_registers:tuple[int,...])->bytes:
    if len(source_registers)>len(SYSV_AMD64.integer_argument_registers): raise ABIError("too many register arguments")
    out=bytearray()
    for src,dst in zip(source_registers,SYSV_AMD64.integer_argument_registers):
        if src!=dst: out+=mov_rr(dst,src)
    return bytes(out)

def move_return_to(register:int)->bytes:
    return b"" if register==SYSV_AMD64.return_register else mov_rr(SYSV_AMD64.return_register,register)
