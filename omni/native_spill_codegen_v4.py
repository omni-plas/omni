"""Frame-aware spill code planning with explicit prologue/epilogue boundaries."""
from __future__ import annotations
from .spill_allocator import allocate_spill_slots

def plan_spill_frame(values):
    slots,size=allocate_spill_slots(values)
    aligned=((size+15)//16)*16
    return {'slots':slots,'raw_size':size,'frame_size':aligned}
