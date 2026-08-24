"""Plan native placement and internal call relocations for multiple functions."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class FunctionPlacement:
    name:str
    offset:int
    size:int

def place_functions(functions):
    offset=0; result=[]
    for name,code in functions:
        result.append(FunctionPlacement(name,offset,len(code)))
        offset += len(code)
    return tuple(result)

def rel32(call_site, target):
    value=target-(call_site+5)
    if not -(1<<31) <= value < (1<<31): raise ValueError('call displacement out of range')
    return value
