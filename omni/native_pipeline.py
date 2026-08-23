"""Ready-to-use bootstrap pipeline for native Omni source."""

from __future__ import annotations

from .backend import BackendRegistry, GenericArtifactBackend
from .native_frontend import OmniNativeFrontend
from .source_pipeline import SourceCompilationResult, compile_source
from .frontend import FrontendRegistry


def compile_native(source: str, *, filename: str = "<source>") -> SourceCompilationResult:
    """Compile native Omni source through the standard frontend/backend pipeline.

    The bootstrap backend emits a deterministic semantic artifact. Real target
    backends can be substituted without changing the source frontend contract.
    """
    frontends = FrontendRegistry((OmniNativeFrontend(),))
    backends = BackendRegistry().register(GenericArtifactBackend())
    return compile_source(
        source,
        language="omni",
        frontends=frontends,
        backends=backends,
        filename=filename,
    )
