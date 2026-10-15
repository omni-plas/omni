"""Semantic validation for the bootstrap Omni AST."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SemanticFunction:
    name: str
    parameters: tuple[str,...]

@dataclass(frozen=True)
class SemanticModule:
    functions: tuple[SemanticFunction,...]

def analyze(module):
    seen=set(); functions=[]
    source_functions = getattr(module, "functions", module)
    for fn in source_functions:
        if fn.name in seen: raise ValueError(f"duplicate function: {fn.name}")
        seen.add(fn.name)
        params=tuple(fn.parameters)
        if len(params)!=len(set(params)): raise ValueError(f"duplicate parameter in {fn.name}")
        functions.append(SemanticFunction(fn.name,params))
    return SemanticModule(tuple(functions))
