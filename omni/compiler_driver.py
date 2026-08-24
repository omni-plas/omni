"""Unified compiler driver for the current Omni front-to-IR pipeline."""
from __future__ import annotations
from dataclasses import dataclass
from .omni_compiler_pipeline import compile_source_to_ir
from .optimization_pipeline import optimize

@dataclass(frozen=True)
class CompilationUnit:
    source: str
    ir: object
    optimized_ir: object

def compile_source(source: str) -> CompilationUnit:
    ir=compile_source_to_ir(source)
    optimized=tuple(optimize(block.operations) for fn in ir.functions for block in getattr(fn,'blocks',()))
    return CompilationUnit(source,ir,optimized)
