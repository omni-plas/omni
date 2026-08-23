"""Ready-to-use bootstrap pipeline for native Omni source."""

from __future__ import annotations

from dataclasses import dataclass

from .backend import BackendRegistry
from .native_backend import NativeArtifactBackend
from .native_frontend import OmniNativeFrontend
from .source_pipeline import SourceCompilationResult, compile_source
from .frontend import FrontendRegistry
from .native_allocating_emitter import PreparedNativeFunction, prepare_native_function
from .native_emission_contract import validate_emission_pipeline


@dataclass(frozen=True)
class NativePreparedModule:
    functions: tuple[PreparedNativeFunction, ...]


def prepare_module(module, registers=(3, 4, 5, 10, 11, 12, 13, 14, 15)) -> NativePreparedModule:
    module.validate()
    validate_emission_pipeline()
    return NativePreparedModule(tuple(prepare_native_function(fn, registers) for fn in module.functions))


def compile_native(source: str, *, filename: str = "<source>") -> SourceCompilationResult:
    """Compile native Omni source into a deterministic portable artifact."""
    frontends = FrontendRegistry((OmniNativeFrontend(),))
    backends = BackendRegistry().register(NativeArtifactBackend())
    return compile_source(
        source,
        language="omni",
        frontends=frontends,
        backends=backends,
        filename=filename,
    )
