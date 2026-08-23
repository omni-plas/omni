"""Build a deterministic call graph and function layout for native modules."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CallEdge:
    caller: str
    callee: str

@dataclass(frozen=True)
class CallGraph:
    functions: tuple[str,...]
    edges: tuple[CallEdge,...]

def build_call_graph(functions, edges=()):
    names=tuple(functions)
    known=set(names)
    normalized=[]
    for caller,callee in edges:
        if caller not in known or callee not in known:
            raise KeyError((caller,callee))
        normalized.append(CallEdge(caller,callee))
    return CallGraph(names,tuple(normalized))

def reachable(graph:CallGraph, entry:str)->tuple[str,...]:
    if entry not in graph.functions: raise KeyError(entry)
    adj={name:[] for name in graph.functions}
    for edge in graph.edges: adj[edge.caller].append(edge.callee)
    seen=set(); order=[]; stack=[entry]
    while stack:
        name=stack.pop()
        if name in seen: continue
        seen.add(name); order.append(name)
        stack.extend(reversed(adj[name]))
    return tuple(order)
