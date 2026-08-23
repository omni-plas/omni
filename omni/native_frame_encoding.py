"""Encode the minimal x86-64 function frame operations."""
from __future__ import annotations
from .native_machine_ops import mov_rr

class FrameEncodingError(ValueError): pass

RBP=5
RSP=4

def prologue(stack_size:int)->bytes:
    if stack_size < 0 or stack_size % 16: raise FrameEncodingError("stack size must be non-negative and 16-byte aligned")
    code=mov_rr(RBP,RSP)
    if stack_size:
        # sub rsp, imm32: 48 81 ec imm32
        code += b"\x48\x81\xec" + int(stack_size).to_bytes(4,"little",signed=True)
    return code

def epilogue(stack_size:int)->bytes:
    if stack_size < 0 or stack_size % 16: raise FrameEncodingError("stack size must be non-negative and 16-byte aligned")
    if stack_size:
        return b"\x48\x81\xc4" + int(stack_size).to_bytes(4,"little",signed=True) + b"\xc3"
    return b"\xc3"
