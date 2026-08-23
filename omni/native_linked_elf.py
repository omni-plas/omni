"""Emit a linked native code/data image as an ELF64 artifact."""
from __future__ import annotations
from .native_link_image import link_image
from .native_global_data import GlobalData
from .native_module_linker import NativeFragment
from .elf64 import build_elf64

def build_image_elf(fragments, globals_=(), entry='main', external_symbols=None):
    image=link_image(tuple(fragments),tuple(globals_),external_symbols)
    if entry not in image.symbols: raise KeyError(entry)
    # Current ELF emitter accepts a contiguous payload. Keep the image layout
    # deterministic: code first, then aligned data.
    return build_elf64(image.code+image.data, image.symbols[entry])
