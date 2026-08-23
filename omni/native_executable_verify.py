"""Validate basic invariants of generated ELF/native artifacts."""
from __future__ import annotations

def verify_elf64(blob:bytes,entry_offset:int=0):
    if len(blob)<64: raise ValueError('ELF image too small')
    if blob[:4]!=b'\x7fELF': raise ValueError('invalid ELF magic')
    if blob[4]!=2: raise ValueError('ELF image is not 64-bit')
    if blob[5]!=1: raise ValueError('ELF image is not little-endian')
    if entry_offset<0: raise ValueError('negative entry offset')
    return True
