"""Deterministic identity for native build inputs and outputs."""
from __future__ import annotations
import hashlib

def manifest_digest(manifest:dict)->str:
    payload=repr(sorted((str(k),repr(v)) for k,v in manifest.items())).encode()
    return hashlib.sha256(payload).hexdigest()

def verify_reproducible(expected:str, actual:str)->bool:
    return expected==actual
