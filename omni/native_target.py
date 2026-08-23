"""Target description for architecture-independent native compilation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class NativeTarget:
    os:str
    arch:str
    abi:str

    def triple(self):
        return f'{self.arch}-{self.os}-{self.abi}'
