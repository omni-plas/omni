"""Encode SysV x86-64 outgoing stack arguments."""
from __future__ import annotations
import struct

# push imm32 is sign-extended by hardware; values outside signed 32-bit are
# represented with a mov/push sequence by higher lowering layers.
def push_imm32(value:int)->bytes:
    if not -(1<<31) <= value < (1<<31):
        raise OverflowError('value does not fit signed imm32')
    return b'\x68'+struct.pack('<i',value)

def push_arguments(values):
    out=bytearray()
    for value in reversed(tuple(values)):
        out += push_imm32(value)
    return bytes(out)
