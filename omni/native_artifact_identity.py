"""Compute stable content identity for native build artifacts."""
from __future__ import annotations
import hashlib

def sha256(data:bytes)->str:
    return hashlib.sha256(bytes(data)).hexdigest()

def verify_digest(data:bytes, expected:str)->bool:
    return sha256(data)==expected
