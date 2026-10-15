"""End-to-end textual Omni compiler bridge."""

from __future__ import annotations

from dataclasses import dataclass

from .native_codegen import NativeExecutable, emit_x86_64_elf
from .native_multi_codegen import emit_multi_x86_64_elf
from .omni_lowering import lower_source
from .ir import ModuleIR
from .targets import TargetDescriptor


@dataclass(frozen=True)
class OmniCompilation:
    source: str
    module: ModuleIR
    target: str
    executable: NativeExecutable | None = None


def compile_omni_source(
    source: str,
    *,
    target: str = "linux-x86_64",
    module_name: str = "omni_module",
    emit_native: bool = False,
) -> OmniCompilation:
    module = lower_source(source, module_name=module_name, strict_calls=False)
    executable = None
    if emit_native:
        if target not in {"linux-x86_64", "linux-amd64"}:
            raise ValueError(f"native bootstrap currently supports linux-x86_64 only: {target}")
        descriptor = TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
        if len(module.functions) == 1:
            executable = emit_x86_64_elf(module, descriptor)
        else:
            executable = emit_multi_x86_64_elf(module, descriptor)
    return OmniCompilation(source, module, target, executable)
