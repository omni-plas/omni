"""Build small Linux executables using Omni's native runtime primitives."""
from __future__ import annotations
from .native_entrypoint import emit_exit_with_status
from .native_executable_pipeline import build_single_function_executable

def build_exit_program(status=0):
    return build_single_function_executable('_start', emit_exit_with_status(status))
