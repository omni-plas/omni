"""Build concrete spill frame allocation around Omni function bodies."""
from __future__ import annotations
from .spill_allocator import allocate_spill_slots
from .native_frame_emitter import allocate_stack, cleanup_stack

def build_spill_frame(values, slot_size=8):
    slots,size=allocate_spill_slots(values,slot_size)
    return {'slots':slots,'size':size,'prologue':allocate_stack(size),'epilogue':cleanup_stack(size)}
