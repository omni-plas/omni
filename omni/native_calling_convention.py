"""System V AMD64 argument and return register model."""
from __future__ import annotations
ARG_REGISTERS=(7,6,2,1,8,9)
RETURN_REGISTER=0
STACK_ALIGNMENT=16

def assign_arguments(count:int):
    if count<0: raise ValueError('argument count cannot be negative')
    registers=tuple(ARG_REGISTERS[:min(count,len(ARG_REGISTERS))])
    stack=max(0,count-len(ARG_REGISTERS))
    return registers,stack
