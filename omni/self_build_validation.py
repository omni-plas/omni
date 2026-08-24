"""Validation gates for moving from bootstrap to self-hosted Omni."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SelfBuildResult:
    bootstrap_ok: bool
    omni_rebuild_ok: bool
    reproducible: bool

    @property
    def self_hosted(self):
        return self.bootstrap_ok and self.omni_rebuild_ok and self.reproducible

def validate_self_build(result:SelfBuildResult):
    if not result.bootstrap_ok: raise RuntimeError('bootstrap compiler failed')
    if not result.omni_rebuild_ok: raise RuntimeError('Omni rebuild failed')
    if not result.reproducible: raise RuntimeError('self-build is not reproducible')
    return result
