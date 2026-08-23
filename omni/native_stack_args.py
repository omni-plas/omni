"""Model outgoing stack arguments for System V calls."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StackArgument:
    source_register:int
    stack_offset:int

@dataclass(frozen=True)
class OutgoingCallFrame:
    arguments: tuple[StackArgument,...]
    size:int
    alignment:int

def place_stack_arguments(registers, shadow_space:int=0, word_size:int=8, alignment:int=16):
    if shadow_space < 0 or shadow_space % word_size:
        raise ValueError("shadow space must be word aligned")
    if alignment <= 0 or alignment % word_size:
        raise ValueError("alignment must be a positive word multiple")
    args=tuple(StackArgument(reg, shadow_space+i*word_size)
               for i,reg in enumerate(reversed(tuple(registers))))
    raw=shadow_space+len(args)*word_size
    size=(raw+alignment-1)//alignment*alignment
    return OutgoingCallFrame(args,size,alignment)
