"""Combine spill allocation with concrete native frame setup."""
from __future__ import annotations
from .spill_allocator import allocate_spill_slots
from .native_frame_emitter import emit_frame_allocate, emit_frame_cleanup

def build_spill_frame(values):
    slots,size=allocate_spill_slots(values)
    aligned=((size+15)//16)*16
    return {'slots':slots,'size':aligned,'prologue':emit_frame_allocate(aligned) if aligned else b'','epilogue':emit_frame_cleanup(aligned) if aligned else b''}
