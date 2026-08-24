"""Deterministic fingerprints for compiler outputs and build inputs."""
from __future__ import annotations
import hashlib

def fingerprint(*parts: object) -> str:
    h=hashlib.sha256()
    for part in parts:
        data=str(part).encode('utf-8')
        h.update(len(data).to_bytes(8,'big'))
        h.update(data)
    return h.hexdigest()
