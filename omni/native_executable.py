"""IR-to-native executable API and filesystem materialization."""

from __future__ import annotations

import os
from pathlib import Path

from .ir import ModuleIR
from .native_codegen import NativeExecutable, emit_x86_64_elf
from .native_multi_codegen import emit_multi_x86_64_elf
from .targets import TargetDescriptor


def compile_native_executable(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    """Lower validated Omni IR to a self-contained native executable.

    The compact single-block emitter is retained for the smallest bootstrap
    modules. Modules containing multiple functions or control-flow blocks use
    the multi-function emitter so normal .oi control flow can reach native
    code generation without an intermediate external compiler.
    """
    module.validate()
    complex_module = len(module.functions) > 1 or any(len(function.blocks) > 1 for function in module.functions)
    if complex_module:
        return emit_multi_x86_64_elf(module, target)
    return emit_x86_64_elf(module, target)


def write_native_executable(path: str | Path, executable: NativeExecutable) -> Path:
    """Write a native executable and mark it executable on POSIX filesystems."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(executable.payload)
    if os.name != "nt":
        destination.chmod(destination.stat().st_mode | 0o111)
    return destination
