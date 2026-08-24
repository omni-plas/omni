"""Deterministic stack-slot allocation for spilled virtual values."""
from __future__ import annotations

def allocate_spill_slots(values, slot_size=8, alignment=8):
    if slot_size <= 0 or alignment <= 0: raise ValueError('slot size and alignment must be positive')
    slots={}
    offset=0
    for value in dict.fromkeys(values):
        if offset % alignment: offset += alignment-(offset%alignment)
        slots[value]=offset
        offset += slot_size
    return slots,offset
