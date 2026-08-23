"""Read and write Omni portable artifacts as validated binary files."""

from __future__ import annotations

from pathlib import Path

from .native_backend import read_artifact


def write_artifact(path: str | Path, payload: bytes) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    return destination


def read_artifact_file(path: str | Path) -> dict:
    return read_artifact(Path(path).read_bytes())
