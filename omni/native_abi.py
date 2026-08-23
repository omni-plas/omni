"""Minimal x86-64 integer ABI helpers for native lowering."""
from __future__ import annotations
from .native_machine_ops import mov_rr

RAX=0
ARG_REGISTERS=(7,6,2,1,8,9)

def move_return_value(src:int)->bytes:
    return b"" if src==RAX else mov_rr(RAX,src)

def move_integer_args(args):
    if len(args)>len(ARG_REGISTERS): raise NotImplementedError("stack arguments are not yet lowered")
    out=bytearray()
    for src,dst in zip(args,ARG_REGISTERS):
        if src!=dst: out += mov_rr(dst,src)
    return bytes(out)
