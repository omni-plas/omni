"""Machine-checkable contract for native emission stages."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EmissionStage:
    name: str
    required: bool = True

NATIVE_EMISSION_STAGES = (
    EmissionStage("allocation"),
    EmissionStage("frame"),
    EmissionStage("lowering"),
    EmissionStage("encoding"),
    EmissionStage("relocations"),
    EmissionStage("executable"),
)

def validate_emission_pipeline(stages=NATIVE_EMISSION_STAGES) -> None:
    names = [s.name for s in stages]
    expected = [s.name for s in NATIVE_EMISSION_STAGES if s.required]
    if names != expected:
        raise ValueError(f"invalid native emission pipeline: {names}")
