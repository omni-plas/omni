"""Patch x86-64 CALL rel32 operands after function placement."""
from __future__ import annotations

def patch_call_rel32(code:bytearray, call_offset:int, target_offset:int):
    if call_offset < 0 or call_offset+5 > len(code): raise ValueError('invalid call offset')
    displacement=target_offset-(call_offset+5)
    if not -(1<<31) <= displacement < (1<<31): raise OverflowError('call target out of rel32 range')
    code[call_offset+1:call_offset+5]=int(displacement).to_bytes(4,'little',signed=True)
    return code
