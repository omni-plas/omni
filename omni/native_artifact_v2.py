"""Represent a native executable together with verified metadata."""
from __future__ import annotations
from dataclasses import dataclass
from .native_executable_verify import verify_elf64

@dataclass(frozen=True)
class NativeArtifact:
    data: bytes
    entry_offset: int
    symbols: dict[str,int]

    @classmethod
    def from_elf(cls, data: bytes, entry_offset: int = 0, symbols=None):
        verify_elf64(data, entry_offset)
        return cls(bytes(data), entry_offset, dict(symbols or {}))

    def verify(self):
        return verify_elf64(self.data, self.entry_offset)
