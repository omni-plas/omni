"""End-to-end textual Omni compiler bridge.

This is a real source -> AST -> semantic IR pipeline. Native emission is kept
behind the existing IR/backend boundary until the textual language gains all
semantics required by the native backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .omni_lowering import lower_source
from .ir import ModuleIR


@dataclass(frozen=True)
class OmniCompilation:
    source: str
    module: ModuleIR
    target: str


def compile_omni_source(source: str, *, target: str = "linux-x86_64", module_name: str = "omni_module") -> OmniCompilation:
    module = lower_source(source, module_name=module_name)
    return OmniCompilation(source, module, target)
