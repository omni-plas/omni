"""Preflight checks shared by native build entry points."""
from __future__ import annotations
from .native_build_target import validate_target

def preflight(target, manifest:dict):
    validate_target(target)
    if not manifest.get('entry'):
        raise ValueError('build manifest requires an entry')
    sources=manifest.get('sources',manifest.get('source_units',()))
    if not sources:
        raise ValueError('build manifest requires source units')
    return True
