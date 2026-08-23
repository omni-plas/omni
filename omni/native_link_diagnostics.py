"""Structured diagnostics for native symbol linking."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LinkDiagnostic:
    severity: str
    message: str
    symbol: str | None = None

def unresolved_symbol(symbol:str)->LinkDiagnostic:
    return LinkDiagnostic('error',f'unresolved symbol: {symbol}',symbol)

def duplicate_symbol(symbol:str)->LinkDiagnostic:
    return LinkDiagnostic('error',f'duplicate symbol: {symbol}',symbol)
