"""Optional discovery of installed Omni language, frontend and backend plugins.

Omni keeps its core registry explicit, while this module provides a standard
extension seam for separately packaged implementations. Discovery is best
-effort by default so a broken optional plugin cannot silently replace the
core compiler.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata
from typing import Any, Callable

from .backend import BackendRegistry
from .language_definition import LanguageDefinition
from .registry import CompilerRegistry, RegistryError


LANGUAGE_GROUP = "omni.languages"
FRONTEND_GROUP = "omni.frontends"
BACKEND_GROUP = "omni.backends"


@dataclass(frozen=True)
class PluginDiscoveryReport:
    loaded: tuple[str, ...] = ()
    skipped: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


def _entry_points(group: str):
    points = metadata.entry_points()
    if hasattr(points, "select"):
        return tuple(points.select(group=group))
    return tuple(points.get(group, ()))


def _materialize(value: Any) -> Any:
    return value() if callable(value) and not isinstance(value, type) else value


def discover_plugins(
    registry: CompilerRegistry,
    *,
    strict: bool = False,
    groups: tuple[str, ...] = (LANGUAGE_GROUP, FRONTEND_GROUP, BACKEND_GROUP),
) -> PluginDiscoveryReport:
    """Load installed Omni plugins into a registry deterministically.

    Entry-point names are sorted before loading. In non-strict mode failures
    are reported and skipped; strict mode raises the first plugin error.
    """
    if not isinstance(registry, CompilerRegistry):
        raise TypeError("registry must be a CompilerRegistry")

    loaded: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    for group in groups:
        for point in sorted(_entry_points(group), key=lambda item: item.name.casefold()):
            label = f"{group}:{point.name}"
            try:
                value = _materialize(point.load())
                if group == LANGUAGE_GROUP:
                    if not isinstance(value, LanguageDefinition):
                        raise TypeError("language plugin must provide LanguageDefinition")
                    registry.register_language_definition(value)
                elif group == FRONTEND_GROUP:
                    registry.register_frontend(value.language, value)
                elif group == BACKEND_GROUP:
                    registry.register_backend(value.name, value)
                else:
                    raise RegistryError(f"unsupported plugin group: {group}")
                loaded.append(label)
            except Exception as exc:
                message = f"{label}: {exc}"
                if strict:
                    raise RegistryError(message) from exc
                errors.append(message)
                skipped.append(label)

    return PluginDiscoveryReport(tuple(loaded), tuple(skipped), tuple(errors))


def discover_default_plugins(*, strict: bool = False) -> tuple[CompilerRegistry, PluginDiscoveryReport]:
    """Create the native registry and extend it with installed plugins."""
    from .source_compiler import default_compiler_registry

    registry = default_compiler_registry()
    return registry, discover_plugins(registry, strict=strict)
