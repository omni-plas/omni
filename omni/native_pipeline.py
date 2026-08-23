"""Ready-to-use bootstrap pipeline for native Omni source."""

from __future__ import annotations

from .backend import BackendRegistry
from .native_backend import NativeArtifactBackend
from .native_frontend import OmniNativeFrontend
from .source_pipeline import SourceCompilationResult, compile_source
from .frontend import FrontendRegistry


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
