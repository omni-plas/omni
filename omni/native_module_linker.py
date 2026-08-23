"""Link native fragments and resolve local/global relocations."""
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
        if fragment.name in offsets:
            raise ValueError(f"duplicate symbol: {fragment.name}")
        offsets[fragment.name]=cursor
        cursor += len(fragment.code)
    output=bytearray(cursor)
    cursor=0
    for fragment in fragments:
        output[cursor:cursor+len(fragment.code)] = fragment.code
        cursor += len(fragment.code)
    for fragment in fragments:
        base=offsets[fragment.name]
        branch=[]
        for r in fragment.branch_relocations:
            target = r.target + base
            branch.append(Relocation(r.offset + base, target, r.size))
        calls=[]
        for r in fragment.call_relocations:
            calls.append(CallRelocation(r.immediate_offset+base, r.target_offset+base, r.instruction_end+base))
        apply_rel8(output, branch)
        apply_call_rel32(output, calls)
    return LinkedModule(bytes(output), offsets)

def link_with_external_targets(fragments, external_symbols):
    """Link fragments whose relocation targets may name external symbols.

    External symbols are supplied as final code offsets in the linked image.
    """
    module=link_fragments(fragments)
    symbols=dict(module.symbols)
    symbols.update(external_symbols)
    return LinkedModule(module.code, symbols)
