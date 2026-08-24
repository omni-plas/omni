"""Compile parsed Omni functions with structured statement bodies."""
from __future__ import annotations
from .omni_stmt_ir import lower_statements

def compile_function(name, statements):
    return lower_statements(name,tuple(statements))
