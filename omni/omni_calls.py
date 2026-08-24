"""Lower call argument values according to the native calling convention."""
from __future__ import annotations
from .native_calling_convention import assign_arguments

def lower_call_arguments(values):
    registers,stack=assign_arguments(len(values))
    return tuple((value,registers[i] if i<len(registers) else None) for i,value in enumerate(values)),stack
