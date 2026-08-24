"""Native spill frame planning without pretending to emit unsupported instructions."""
from __future__ import annotations
from .spill_allocator import allocate_spill_slots

def plan_spill_frame(values, slot_size=8):
    slots,size=allocate_spill_slots(values,slot_size)
    return slots,size
