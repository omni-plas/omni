"""Linux x86-64 syscall ABI primitives."""
from __future__ import annotations
from .native_machine_ops import mov_imm64, mov_rr

RAX=0; RDI=7; RSI=6; RDX=2; R10=10; R8=8; R9=9

def syscall_number(number:int)->bytes:
    return mov_imm64(RAX,number)

def syscall6(number:int,args=())->bytes:
    if len(args)>6: raise ValueError("Linux x86-64 syscalls accept at most six arguments")
    regs=(RDI,RSI,RDX,R10,R8,R9)
    out=bytearray(syscall_number(number))
    for src,dst in zip(args,regs):
        if src != dst: out += mov_rr(dst,src)
    return bytes(out)+b"\x0f\x05"
