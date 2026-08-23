"""Compile only functions reachable from the selected entry point."""
from __future__ import annotations
from .native_call_graph import build_call_graph, reachable
from .native_function_module import compile_functions

def compile_reachable(functions, edges, entry):
    graph=build_call_graph(tuple(fn.name for fn in functions),edges)
    wanted=set(reachable(graph,entry))
    selected=tuple(fn for fn in functions if fn.name in wanted)
    return compile_functions(selected)
