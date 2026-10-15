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
    absolute_end=len(code)
    for item in globals_:
        absolute_start=align_up(absolute_end, item.alignment)
        # Keep the data section payload independent of its absolute image
        # placement: its first symbol may start after code-to-data alignment,
        # but that leading gap belongs to the linker layout, not data bytes.
        if data and absolute_start>absolute_end:
            data.extend(b'\0'*(absolute_start-absolute_end))
        data_symbols[item.name]=absolute_start
        data.extend(item.data)
        absolute_end=absolute_start+len(item.data)
    symbols=dict(module.symbols)
    for name,offset in data_symbols.items():
        if name in symbols: raise ValueError(f'duplicate symbol: {name}')
        symbols[name]=offset
    return LinkedImage(code,bytes(data),symbols)
