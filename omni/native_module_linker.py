"""Link native function fragments and resolve local branch/call relocations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_relocations import Relocation, apply_rel8
from .native_call_relocations import CallRelocation, apply_call_rel32

@dataclass(frozen=True)
class NativeFragment:
    name: str
    code: bytes
    branch_relocations: tuple[Relocation,...] = ()
    call_relocations: tuple[CallRelocation,...] = ()

@dataclass(frozen=True)
class LinkedModule:
    code: bytes
    symbols: dict[str,int]

def link_fragments(fragments):
    offsets={}
    cursor=0
    for fragment in fragments:
        if fragment.name in offsets: raise ValueError(f"duplicate symbol: {fragment.name}")
        offsets[fragment.name]=cursor
        cursor += len(fragment.code)
    output=bytearray(cursor)
    cursor=0
    for fragment in fragments:
        output[cursor:cursor+len(fragment.code)] = fragment.code
        cursor += len(fragment.code)
    # Relocation targets are fragment-local absolute offsets in this compact linker.
    for fragment in fragments:
        base=offsets[fragment.name]
        local=bytearray(fragment.code)
        branch=tuple(Relocation(r.offset+base,r.target+base,r.size) for r in fragment.branch_relocations)
        calls=tuple(CallRelocation(r.immediate_offset+base,r.target_offset+base,r.instruction_end+base) for r in fragment.call_relocations)
        apply_rel8(output,branch)
        apply_call_rel32(output,calls)
    return LinkedModule(bytes(output),offsets)
