"""Resolve x86-64 rel32 call displacements from native symbol offsets."""
from __future__ import annotations

def call_rel32_displacement(target_offset:int, call_offset:int, instruction_size:int=5)->int:
    if instruction_size != 5: raise ValueError('rel32 call instruction must be 5 bytes')
    delta=target_offset-(call_offset+instruction_size)
    if not -(1<<31) <= delta < (1<<31):
        raise OverflowError('rel32 call target out of range')
    return delta
