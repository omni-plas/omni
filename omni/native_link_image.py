"""Link native code and data into one deterministic image."""
from __future__ import annotations
from dataclasses import dataclass
from .native_global_data import align_up, GlobalData
from .native_module_linker import link_fragments, NativeFragment

@dataclass(frozen=True)
class LinkedImage:
    code: bytes
    data: bytes
    symbols: dict[str,int]

def link_image(fragments, globals_=(), external_symbols=None):
    module=link_fragments(tuple(fragments), external_symbols)
    code=module.code
    data=bytearray()
    data_symbols={}
    for item in globals_:
        pos=align_up(len(code) + len(data), item.alignment) - len(code)
        if pos>len(data): data.extend(b'\0'*(pos-len(data)))
        data_symbols[item.name]=len(code)+pos
        data.extend(item.data)
    symbols=dict(module.symbols)
    for name,offset in data_symbols.items():
        if name in symbols: raise ValueError(f'duplicate symbol: {name}')
        symbols[name]=offset
    return LinkedImage(code,bytes(data),symbols)
