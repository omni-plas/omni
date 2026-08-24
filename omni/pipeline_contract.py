"""Contracts for deterministic Omni compilation stages."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

I=TypeVar('I'); O=TypeVar('O')
@dataclass(frozen=True)
class StageResult(Generic[O]):
    value: O
    diagnostics: tuple[str,...]=()

class Stage(Generic[I,O]):
    name='stage'
    def run(self, value:I)->StageResult[O]:
        raise NotImplementedError
