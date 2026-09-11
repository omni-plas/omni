"""First-class handling of Omni source files.

The ``.oi`` suffix is part of the Omni language identity.  This module keeps
that rule at the file boundary so callers cannot accidentally treat another
file type as native Omni source.
"""
from __future__ import annotations

from pathlib import Path

from .oi_file_icon import OI_EXTENSION
from .omni_source import Program, parse


class OmniSourceFileError(ValueError):
    """Raised when a path is not a valid native Omni source-file input."""


def is_omni_source_path(path: str | Path) -> bool:
    """Return whether *path* uses the official ``.oi`` source extension."""
    return Path(path).suffix.lower() == OI_EXTENSION


def require_omni_source_path(path: str | Path) -> Path:
    """Validate and return a path as a ``Path`` object."""
    source_path = Path(path)
    if not is_omni_source_path(source_path):
        raise OmniSourceFileError(
            f"Omni source files must use the {OI_EXTENSION} extension: {source_path}"
        )
    return source_path


def load_oi_source(path: str | Path) -> Program:
    """Read and parse a native Omni ``.oi`` source file."""
    source_path = require_omni_source_path(path)
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OmniSourceFileError(f"cannot read Omni source file {source_path}: {exc}") from exc
    return parse(source)
