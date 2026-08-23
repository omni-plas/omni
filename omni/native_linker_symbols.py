"""Link native fragments with symbol-named call/data relocations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_module_linker import NativeFragment
from .native_symbol_relocations import SymbolCallRelocation, SymbolDataRelocation, apply_symbol_relocations

@dataclass(frozen=True)
class SymbolicFragment:
    name: str
    code: bytes
    calls: tuple[SymbolCallRelocation,...] = ()
    data_refs: tuple[SymbolDataRelocation,...] = ()

def link_symbolic_fragments(fragments, data_symbols=None):
    data_symbols = {} if data_symbols is None else dict(data_symbols)
    offsets={}
    cursor=0
    for f in fragments:
        if f.name in offsets: raise ValueError(f'duplicate symbol: {f.name}')
        offsets[f.name]=cursor; cursor += len(f.code)
    out=bytearray(cursor)
    for f in fragments:
        base=offsets[f.name]
        out[base:base+len(f.code)]=f.code
    symbols=dict(offsets); symbols.update(data_symbols)
    for f in fragments:
        base=offsets[f.name]
        calls=tuple(SymbolCallRelocation(r.immediate_offset+base,r.instruction_end+base,r.symbol) for r in f.calls)
        refs=tuple(SymbolDataRelocation(r.immediate_offset+base,r.symbol,r.width) for r in f.data_refs)
        apply_symbol_relocations(out,calls,refs,symbols)
    return bytes(out), symbols
