"""Run build stages without losing structured failure information."""
from __future__ import annotations
from dataclasses import dataclass
from .native_build_diagnostics import Diagnostic, error

@dataclass(frozen=True)
class StageResult:
    value: object = None
    diagnostics: tuple[Diagnostic,...] = ()
    success: bool = True

def run_stage(name:str, fn)->StageResult:
    try:
        return StageResult(fn(),(),True)
    except Exception as exc:
        return StageResult(None,(error(name,'E_STAGE',str(exc)),),False)
