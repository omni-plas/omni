"""Structured diagnostics for native build stages."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Diagnostic:
    stage: str
    code: str
    message: str
    severity: str = 'error'

def error(stage:str, code:str, message:str)->Diagnostic:
    return Diagnostic(stage,code,message,'error')

def warning(stage:str, code:str, message:str)->Diagnostic:
    return Diagnostic(stage,code,message,'warning')
