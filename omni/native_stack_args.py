"""Model outgoing stack arguments for System V calls."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StackArgument:
    source_register:int
    stack_offset:int

def place_stack_arguments(registers, shadow_space:int=0, word_size:int=8):
    if shadow_space < 0 or shadow_space % word_size:
        raise ValueError("shadow space must be word aligned")
    # SysV stack arguments are placed from right to left; offset 0 is the
    # first outgoing argument slot above the return-address boundary model.
    return tuple(StackArgument(reg, shadow_space+i*word_size)
                  for i,reg in enumerate(reversed(tuple(registers))))
