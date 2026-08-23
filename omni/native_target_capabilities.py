"""Declare capabilities required by native compilation stages."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TargetCapabilities:
    call_rel32: bool = True
    stack_arguments: bool = True
    global_data: bool = True
    relocations: bool = True
    elf64: bool = True

    def require(self, **requirements):
        for name, needed in requirements.items():
            if needed and not getattr(self, name, False):
                raise ValueError(f'target capability required: {name}')
        return True
