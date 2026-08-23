"""Build a deterministic native image model from code and global data."""
from __future__ import annotations
from dataclasses import dataclass
from .native_module_linker import link_fragments
from .native_global_data import place_data, GlobalData

@dataclass(frozen=True)
class NativeImage:
    code: bytes
    data: bytes
    code_symbols: dict[str,int]
    data_symbols: dict[str,int]

def build_image(fragments, globals_=()):
    module=link_fragments(tuple(fragments))
    data_start=len(module.code)
    data=place_data(tuple(globals_),data_start)
    return NativeImage(module.code,data.data,dict(module.symbols),dict(data.offsets))
