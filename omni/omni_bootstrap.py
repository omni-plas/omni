"""Bootstrap builder for compiling a textual Omni program to native ELF."""

from __future__ import annotations

from dataclasses import dataclass

from .native_codegen import NativeExecutable, emit_x86_64_elf
from .native_multi_codegen import emit_multi_x86_64_elf
from .omni_compile import compile_omni_source
from .targets import TargetDescriptor


@dataclass(frozen=True)
class OmniBootstrapArtifact:
    target: TargetDescriptor
    executable: NativeExecutable


def build_bootstrap(source: str, *, target: TargetDescriptor | None = None) -> OmniBootstrapArtifact:
    requested = target or TargetDescriptor("linux", "x86_64", "sysv", {"native-executable": True})
    compilation = compile_omni_source(source, target=requested.identity())
    if len(compilation.module.functions) == 1:
        executable = emit_x86_64_elf(compilation.module, requested)
    else:
        executable = emit_multi_x86_64_elf(compilation.module, requested)
    return OmniBootstrapArtifact(requested, executable)
