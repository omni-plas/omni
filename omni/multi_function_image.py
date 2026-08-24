"""Assemble function byte fragments into one deterministic native image."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FunctionImage:
    name:str
    offset:int
    size:int

@dataclass(frozen=True)
class NativeImage:
    payload:bytes
    functions:tuple[FunctionImage,...]

def assemble_functions(functions):
    payload=bytearray(); meta=[]
    for name,code in functions:
        if not isinstance(name,str) or not name: raise ValueError('invalid function name')
        offset=len(payload); payload.extend(code)
        meta.append(FunctionImage(name,offset,len(code)))
    return NativeImage(bytes(payload),tuple(meta))
