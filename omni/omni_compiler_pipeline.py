"""Front-to-IR pipeline for Omni source."""
from __future__ import annotations
from .omni_source_frontend import parse
from .semantic import analyze
from .omni_ir import lower_semantic

def compile_source_to_ir(source: str):
    return lower_semantic(analyze(parse(source)))
