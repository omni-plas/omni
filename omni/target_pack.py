"""Declarative target packs for historical, current, and future environments."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .targets import TargetDescriptor, TargetError


class TargetPackError(ValueError):
    """Raised when a target-pack document cannot be loaded."""


def target_from_mapping(document: Mapping[str, Any]) -> TargetDescriptor:
    if not isinstance(document, Mapping):
        raise TargetPackError("target pack root must be an object")
    try:
        if document.get("schema") not in (None, "omni.target.v1"):
            raise TargetPackError("unsupported target pack schema")
        return TargetDescriptor(
            document["platform"],
            document.get("architecture"),
            document.get("abi"),
            document.get("capabilities", {}),
        )
    except (KeyError, TypeError, TargetError) as exc:
        raise TargetPackError(f"invalid target pack: {exc}") from exc


def load_target_pack(path: str | Path) -> TargetDescriptor:
    target_path = Path(path)
    try:
        document = json.loads(target_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TargetPackError(f"cannot read target pack {target_path}: {exc}") from exc
    return target_from_mapping(document)


def dump_target_pack(target: TargetDescriptor, path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(target.document(), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
