"""Describe a native build artifact and its compilation inputs."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class NativeBuildManifest:
    target_os: str
    target_arch: str
    entry: str
    source_units: tuple[str,...]
    symbols: tuple[str,...]

    def as_dict(self):
        return {
            'target_os': self.target_os,
            'target_arch': self.target_arch,
            'entry': self.entry,
            'source_units': list(self.source_units),
            'symbols': list(self.symbols),
        }
