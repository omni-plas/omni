"""Aggregate value and diagnostics across native build stages."""
from __future__ import annotations
from dataclasses import dataclass
from .native_build_diagnostics import Diagnostic

@dataclass(frozen=True)
class PipelineResult:
    value: object = None
    diagnostics: tuple[Diagnostic,...] = ()
    success: bool = True

    @classmethod
    def failure(cls,*diagnostics:Diagnostic):
        return cls(None,tuple(diagnostics),False)

    @classmethod
    def ok(cls,value):
        return cls(value,(),True)
