"""Encode caller stack cleanup after an outgoing call."""
from __future__ import annotations
import struct

def add_rsp(size:int)->bytes:
    if size<0 or size%8: raise ValueError('stack cleanup must be non-negative and word aligned')
    if size==0: return b''
    if size<=127:
        return b'\x48\x83\xc4'+bytes([size])
    if size>0xffffffff: raise OverflowError('cleanup too large')
    return b'\x48\x81\xc4'+struct.pack('<I',size)
