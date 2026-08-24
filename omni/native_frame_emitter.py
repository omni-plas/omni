"""Concrete stack-frame instruction emission for x86-64."""
from __future__ import annotations
import struct


def _imm32(value):
    if not 0 <= value <= 0x7fffffff:
        raise ValueError('frame size must fit positive signed imm32')
    return struct.pack('<I', value)


def allocate_stack(bytes_count):
    if bytes_count < 0 or bytes_count % 8:
        raise ValueError('stack size must be a non-negative multiple of 8')
    if not bytes_count:
        return b''
    return b'\x48\x81\xec' + _imm32(bytes_count)


def cleanup_stack(bytes_count):
    if bytes_count < 0 or bytes_count % 8:
        raise ValueError('stack size must be a non-negative multiple of 8')
    if not bytes_count:
        return b''
    return b'\x48\x81\xc4' + _imm32(bytes_count)
