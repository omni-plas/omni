"""Language-agnostic source resolution and semantic compilation entry point."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .frontends import SourceUnit
from .language_definition import LanguageDefinition
from .native_frontend import OmniNativeFrontend
from .pipeline import CompilationResult, compile_semantics
from .registry import CompilerRegistry, RegistryError


@dataclass(frozen=True)
class ResolvedSource:
    """The language contract and frontend selected for one source unit."""

    definition: LanguageDefinition
    frontend: object


def default_compiler_registry(*, include_plugins: bool = False) -> CompilerRegistry:
    """Build a minimal registry containing Omni's native frontend.

    Additional language definitions and frontends can be registered by callers;
    no permanent language whitelist is embedded in source resolution.
    """
    registry = CompilerRegistry()
    registry.register_language_definition(
        LanguageDefinition(
            name="Omni",
            version="1",
            aliases=("omni",),
            source_extensions=(".oi",),
            syntax={"grammar": "omni-native"},
            semantics={"model": "omni-uir"},
            type_rules={"model": "omni-native"},
            execution_model={"model": "target-defined"},
            memory_model={"model": "target-defined"},
            abi_expectations={"model": "target-defined"},
            dependency_rules={"resolution": "omni"},
        )
    )
    registry.register_frontend("Omni", OmniNativeFrontend())
    if include_plugins:
        from .plugin_discovery import discover_plugins
        discover_plugins(registry)
    return registry


def discover_compiler_registry(*, strict: bool = False) -> CompilerRegistry:
    """Create the native compiler registry and load installed plugins."""
    registry = default_compiler_registry()
    from .plugin_discovery import discover_plugins
    discover_plugins(registry, strict=strict)
    return registry


def resolve_source(
    source: str,
    *,
    language: str | None = None,
    version: str | None = None,
    origin: str | Path | None = None,
    registry: CompilerRegistry | None = None,
) -> ResolvedSource:
    """Resolve a source language by explicit identity or by its file extension."""
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source cannot be empty")
    active = registry or default_compiler_registry()
    if language:
        definition = active.language_definition(language, version)
        frontend = active.frontend(definition.name)
    else:
        if origin is None:
            raise RegistryError("language or source origin is required for automatic resolution")
        definition = active.language_definition_for_extension(Path(origin).suffix)
        if version is not None and definition.version != version.strip():
            raise RegistryError(f"source requires language version {version}, resolved {definition.version}")
        frontend = active.frontend(definition.name)
    return ResolvedSource(definition, frontend)


def compile_source(
    source: str,
    *,
    language: str | None = None,
    version: str | None = None,
    origin: str | Path | None = None,
    registry: CompilerRegistry | None = None,
) -> CompilationResult:
    """Resolve a frontend, lower its source to UIR, then run semantic compilation."""
    resolved = resolve_source(source, language=language, version=version, origin=origin, registry=registry)
    unit = SourceUnit(resolved.definition.name, source, str(origin) if origin is not None else None)
    uir = resolved.frontend.lower(unit)
    return compile_semantics(uir)
