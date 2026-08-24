"""Concrete outgoing call-frame lowering for System V AMD64."""
from __future__ import annotations
from .native_calling_convention import ARG_REGISTERS
from .native_stack_args import place_stack_arguments
from .native_stack_store import sub_rsp8, add_rsp8, store_rsp8

def lower_outgoing_frame(values, register_map):
    overflow=tuple(values[len(ARG_REGISTERS):])
    frame=place_stack_arguments(tuple(register_map[v] for v in overflow))
    code=bytearray(sub_rsp8(frame.size) if frame.size else b'')
    for arg in frame.arguments:
        code += store_rsp8(arg.source_register,arg.stack_offset)
    return bytes(code), frame

def cleanup_outgoing_frame(frame):
    return add_rsp8(frame.size) if frame.size else b''
