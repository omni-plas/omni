"""Link native fragments and resolve local/global relocations."""
from __future__ import annotations
from dataclasses import dataclass
import struct
from .native_relocations import Relocation, apply_rel8
from .native_call_relocations import CallRelocation, apply_call_rel32

@dataclass(frozen=True)
class NativeFragment:
    name: str
    code: bytes
    branch_relocations: tuple[Relocation,...] = ()
    call_relocations: tuple[CallRelocation,...] = ()
    symbol_relocations: tuple = ()

@dataclass(frozen=True)
class LinkedModule:
    code: bytes
    symbols: dict[str,int]

def _resolve_symbol_relocations(output, relocs, symbols):
    for r in relocs:
        if r.symbol not in symbols:
            raise KeyError(f"unresolved symbol: {r.symbol}")
        target=symbols[r.symbol]+r.addend
        if r.kind == "call_rel32":
            if r.instruction_end is None: raise ValueError("call relocation needs instruction_end")
            delta=target-r.instruction_end
            output[r.immediate_offset:r.immediate_offset+4]=struct.pack('<i',delta)
        elif r.kind == "abs32":
            output[r.immediate_offset:r.immediate_offset+4]=struct.pack('<I',target & 0xffffffff)
        elif r.kind == "abs64":
            output[r.immediate_offset:r.immediate_offset+8]=struct.pack('<Q',target & 0xffffffffffffffff)
        else: raise ValueError(f"unknown relocation kind: {r.kind}")

def link_fragments(fragments):
    offsets={}; cursor=0
    for fragment in fragments:
        if fragment.name in offsets: raise ValueError(f"duplicate symbol: {fragment.name}")
        offsets[fragment.name]=cursor; cursor += len(fragment.code)
    output=bytearray(cursor); cursor=0
    for fragment in fragments:
        output[cursor:cursor+len(fragment.code)] = fragment.code; cursor += len(fragment.code)
    for fragment in fragments:
        base=offsets[fragment.name]
        branch=[Relocation(r.offset+base,r.target+base,r.size) for r in fragment.branch_relocations]
        calls=[CallRelocation(r.immediate_offset+base,r.target_offset+base,r.instruction_end+base) for r in fragment.call_relocations]
        apply_rel8(output,branch); apply_call_rel32(output,calls)
    symbols=dict(offsets)
    all_symbol_relocs=[]
    for fragment in fragments:
        base=offsets[fragment.name]
        for r in fragment.symbol_relocations:
            end=None if r.instruction_end is None else r.instruction_end+base
            all_symbol_relocs.append(type(r)(r.kind,r.immediate_offset+base,r.symbol,r.addend,end))
    _resolve_symbol_relocations(output,all_symbol_relocs,symbols)
    return LinkedModule(bytes(output),symbols)

def link_with_external_targets(fragments, external_symbols):
    module=link_fragments(fragments); symbols=dict(module.symbols); symbols.update(external_symbols)
    return LinkedModule(module.code,symbols)
