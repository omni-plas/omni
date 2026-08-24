"""Lower semantically validated Omni functions into a small function IR."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class IRFunction:
    name: str
    parameters: tuple[str,...]

@dataclass(frozen=True)
class IRModule:
    functions: tuple[IRFunction,...]

def lower_semantic(module):
    return IRModule(tuple(IRFunction(fn.name,fn.parameters) for fn in module.functions))
