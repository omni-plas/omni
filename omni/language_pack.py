"""Load declarative language definitions without installing another compiler.

A language pack describes the source-language contract. Executable frontend
code can be registered separately, but the definition itself is portable data
and can be shipped with Omni or discovered at runtime.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .language_definition import LanguageDefinition, LanguageDefinitionError
from .registry import CompilerRegistry, RegistryError


class LanguagePackError(ValueError):
    """Raised when a language-pack document cannot be loaded."""


def definition_from_mapping(document: Mapping[str, Any]) -> LanguageDefinition:
    if not isinstance(document, Mapping):
        raise LanguagePackError("language pack root must be an object")
    try:
        return LanguageDefinition(
            name=document["name"],
            version=document["version"],
            source_extensions=tuple(document.get("source_extensions", ())),
            aliases=tuple(document.get("aliases", ())),
            syntax=document.get("syntax", {}),
            semantics=document.get("semantics", {}),
            type_rules=document.get("type_rules", {}),
            execution_model=document.get("execution_model", {}),
            memory_model=document.get("memory_model", {}),
            abi_expectations=document.get("abi_expectations", {}),
            dependency_rules=document.get("dependency_rules", {}),
        )
    except (KeyError, TypeError, LanguageDefinitionError) as exc:
        raise LanguagePackError(f"invalid language pack: {exc}") from exc


def load_language_pack(path: str | Path) -> LanguageDefinition:
    pack_path = Path(path)
    try:
        document = json.loads(pack_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LanguagePackError(f"cannot read language pack {pack_path}: {exc}") from exc
    return definition_from_mapping(document)


def register_language_pack(registry: CompilerRegistry, path: str | Path) -> LanguageDefinition:
    definition = load_language_pack(path)
    try:
        registry.register_language_definition(definition)
    except RegistryError as exc:
        raise LanguagePackError(str(exc)) from exc
    return definition

def dump_language_pack(definition: LanguageDefinition, path: str | Path) -> None:
    """Write a canonical deterministic language-pack document."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(definition.manifest(), ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
