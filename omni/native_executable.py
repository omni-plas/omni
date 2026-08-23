"""IR-to-native executable API for targets with a self-contained backend."""

from __future__ import annotations

from .ir import ModuleIR
from .native_codegen import NativeExecutable, emit_x86_64_elf
from .targets import TargetDescriptor


def compile_native_executable(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    """Lower an already validated Omni IR module to a native executable artifact."""
    return emit_x86_64_elf(module, target)
