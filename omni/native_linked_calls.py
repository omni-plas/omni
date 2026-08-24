"""Build a linked native function containing an internal call."""
from __future__ import annotations
from dataclasses import dataclass
from .native_call_frame_lowering import lower_outgoing_frame, cleanup_outgoing_frame
from .native_call_lowering import move_call_arguments
from .native_machine_ops import call_rel32, ret
from .native_module_linker import NativeFragment, link_fragments
from .native_symbol_relocation import SymbolRelocation

@dataclass(frozen=True)
class LinkedCall:
    caller: str
    callee: str
    argument_values: tuple[str,...]
    register_map: dict[str,int]

def build_linked_call(caller, caller_code, callee, values, register_map):
    frame_code, frame=lower_outgoing_frame(values,register_map)
    args=tuple(values[:6])
    code=bytearray(caller_code)
    code += frame_code
    code += move_call_arguments(args,register_map)
    call_offset=len(code)
    code += call_rel32(0)
    code += cleanup_outgoing_frame(frame)
    code += ret()
    relocation=SymbolRelocation('call_rel32',call_offset+1,callee,0,call_offset+5)
    return link_fragments((NativeFragment(caller,bytes(code),symbol_relocations=(relocation,)), NativeFragment(callee,b'\xc3')))
