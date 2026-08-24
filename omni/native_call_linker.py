"""Link native functions with explicit internal call relocations."""
from __future__ import annotations
from dataclasses import dataclass
from .native_call_relocations import CallRelocation
from .native_module_linker import NativeFragment, link_fragments

@dataclass(frozen=True)
class NativeCallSite:
    immediate_offset: int
    instruction_end: int
    target: str

def link_functions(functions):
    """functions: iterable of (name, code, call_sites)."""
    fragments=[]
    for name,code,sites in functions:
        symbols=tuple()
        relocs=[]
        for site in sites:
            relocs.append(CallRelocation(site.immediate_offset,0,site.instruction_end))
        fragments.append(NativeFragment(name,code,call_relocations=tuple(relocs),symbol_relocations=tuple()))
    # Convert symbolic call sites to symbol relocations, because the linker already
    # owns the authoritative symbol table and can validate unresolved names.
    fragments=[]
    from .native_symbol_reloc import call_rel32
    for name,code,sites in functions:
        fragments.append(NativeFragment(name,code,symbol_relocations=tuple(call_rel32(s.immediate_offset,s.instruction_end,s.target) for s in sites)))
    return link_fragments(tuple(fragments))
