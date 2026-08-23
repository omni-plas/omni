"""Small typed contracts shared by native build orchestration."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StageResult:
    stage: str
    output: object
    diagnostics: tuple[str,...] = ()

    def ok(self):
        return not self.diagnostics


def success(stage:str, output:object)->StageResult:
    return StageResult(stage,output,())


def failure(stage:str, message:str)->StageResult:
    return StageResult(stage,None,(message,))
