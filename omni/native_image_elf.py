"""Convert a NativeImage into an ELF64 payload with code as entry region."""
from __future__ import annotations
from .elf64 import build_elf64
from .native_image import NativeImage

def image_to_elf(image:NativeImage, entry_symbol:str="main") -> bytes:
    if entry_symbol not in image.code_symbols:
        raise ValueError(f"unknown entry symbol: {entry_symbol}")
    payload=image.code+image.data
    return build_elf64(payload,image.code_symbols[entry_symbol])
