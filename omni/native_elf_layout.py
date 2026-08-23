"""Deterministic layout metadata for native ELF payloads."""
from __future__ import annotations
from dataclasses import dataclass
from .native_global_data import align_up

@dataclass(frozen=True)
class ElfLayout:
    code_offset:int
    data_offset:int
    entry_offset:int
    total_size:int

def layout(code_size:int,data_size:int,entry_offset:int=0,data_alignment:int=16)->ElfLayout:
    if code_size<0 or data_size<0: raise ValueError('negative section size')
    if entry_offset<0 or entry_offset>=max(code_size,1): raise ValueError('entry outside code')
    data_offset=align_up(code_size,data_alignment)
    return ElfLayout(0,data_offset,entry_offset,data_offset+data_size)
