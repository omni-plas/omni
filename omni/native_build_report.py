"""Compact machine-readable native build report."""
from __future__ import annotations

def build_report(result):
    return {
        'target': result.target.triple(),
        'entry': result.manifest['entry'],
        'artifact_size': len(result.artifact),
        'artifact_sha256': result.identity.artifact,
        'manifest_sha256': result.identity.manifest,
    }
