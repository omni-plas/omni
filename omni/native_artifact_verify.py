"""Validate native artifact metadata beyond the ELF header."""
from __future__ import annotations
from .native_executable_verify import verify_elf64

def verify_artifact(data: bytes, entry_offset: int, symbols: dict[str,int], entry: str):
    verify_elf64(data, entry_offset)
    if entry not in symbols:
        raise ValueError(f'missing entry symbol: {entry}')
    if symbols[entry] != entry_offset:
        raise ValueError('entry symbol does not match entry offset')
    for name, offset in symbols.items():
        if offset < 0:
            raise ValueError(f'negative symbol offset: {name}')
        if offset >= len(data):
            raise ValueError(f'symbol outside artifact: {name}')
    return True
