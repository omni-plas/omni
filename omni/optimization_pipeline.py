"""Deterministic optimization pipeline for Omni IR."""
from .constant_folding import fold_constants
from .ssa import rename_ssa

def optimize(operations):
    return rename_ssa(fold_constants(tuple(operations)))
