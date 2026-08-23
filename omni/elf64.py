"""Minimal ET_EXEC ELF64 writer for position-fixed machine code."""
from __future__ import annotations
import struct

ELF_HEADER_SIZE = 64
PROGRAM_HEADER_SIZE = 56
PAGE = 0x1000
PT_LOAD = 1
PF_X = 1
PF_W = 2
PF_R = 4
ET_EXEC = 2
EM_X86_64 = 62
EV_CURRENT = 1

class ELFError(ValueError):
    pass

def build_elf64(code: bytes, entry_offset: int = 0, writable: bool = False) -> bytes:
    if not code:
        raise ELFError("ELF executable cannot contain empty code")
    if entry_offset < 0 or entry_offset >= len(code):
        raise ELFError("entry offset outside code")
    phoff = ELF_HEADER_SIZE
    code_off = PAGE
    base = 0x400000
    entry = base + code_off + entry_offset
    flags = PF_R | PF_X | (PF_W if writable else 0)
    ph = struct.pack(
        "<IIQQQQQQ", PT_LOAD, flags, code_off, base + code_off,
        base + code_off, len(code), len(code), PAGE
    )
    ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + bytes(8)
    eh = struct.pack(
        "<16sHHIQQQIHHHHHH", ident, ET_EXEC, EM_X86_64, EV_CURRENT,
        entry, phoff, 0, 0, ELF_HEADER_SIZE, PROGRAM_HEADER_SIZE, 1, 0, 0, 0
    )
    padding = code_off - len(eh) - len(ph)
    if padding < 0:
        raise ELFError("ELF headers exceed page size")
    return eh + ph + b"\x00" * padding + code
