"""Native function frame setup/teardown using existing encoders."""
from __future__ import annotations

def prologue():
    return b'\x55\x48\x89\xe5'

def epilogue():
    return b'\x5d\xc3'
