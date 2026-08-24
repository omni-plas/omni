"""Concrete spill/reload emission using the existing RBP-relative encoders."""
from __future__ import annotations
from .native_machine_ops import load_rbp8, store_rbp8

def emit_spill(src_register, offset):
    if offset < -128 or offset > 127:
        raise ValueError('spill offset must fit signed 8-bit RBP displacement')
    return store_rbp8(offset, src_register)

def emit_reload(dst_register, offset):
    if offset < -128 or offset > 127:
        raise ValueError('reload offset must fit signed 8-bit RBP displacement')
    return load_rbp8(dst_register, offset)
