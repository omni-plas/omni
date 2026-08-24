"""Integrated spill/reload lowering for allocated Omni values."""
from __future__ import annotations
from .native_spill_emitter import emit_spill, emit_reload
from .spill_allocator import allocate_spill_slots

def emit_spill_sequence(spilled_values, register_map):
    slots,size=allocate_spill_slots(spilled_values)
    code=bytearray()
    for value in spilled_values:
        if value not in register_map: raise ValueError(f'missing register for {value}')
        code += emit_spill(register_map[value], -(slots[value]+8))
    return bytes(code), slots, size

def emit_reload_sequence(values, register_map, slots):
    code=bytearray()
    for value in values:
        if value not in slots or value not in register_map: raise ValueError(f'missing spill mapping for {value}')
        code += emit_reload(register_map[value], -(slots[value]+8))
    return bytes(code)
