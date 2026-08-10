"""Canonical UIR schema metadata used by validation and tooling."""

from __future__ import annotations

REQUIRED_ROOT_FIELDS = ("version", "entity", "source", "target", "semantics")
REQUIRED_SEMANTIC_FIELDS = (
    "types",
    "control_flow",
    "data_flow",
    "memory_model",
    "error_handling",
    "io",
    "dependencies",
    "security",
    "performance",
)


def schema_summary() -> dict[str, tuple[str, ...]]:
    return {
        "root": REQUIRED_ROOT_FIELDS,
        "semantics": REQUIRED_SEMANTIC_FIELDS,
    }
