"""IR-to-native executable API and filesystem materialization."""

from __future__ import annotations

import os
from pathlib import Path

from .ir import ModuleIR
from .native_codegen import NativeExecutable, emit_x86_64_elf
from .targets import TargetDescriptor


def compile_native_executable(module: ModuleIR, target: TargetDescriptor | None = None) -> NativeExecutable:
    """Lower an already validated Omni IR module to a native executable artifact."""
    return emit_x86_64_elf(module, target)


def write_native_executable(path: str | Path, executable: NativeExecutable) -> Path:
    """Write a native executable and mark it executable on POSIX filesystems."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(executable.payload)
    if os.name != "nt":
        destination.chmod(destination.stat().st_mode | 0o111)
    return destination
