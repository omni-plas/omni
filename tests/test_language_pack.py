import json

import pytest

from omni.language_definition import LanguageDefinition
from omni.language_pack import LanguagePackError, definition_from_mapping, dump_language_pack, load_language_pack, register_language_pack
from omni.registry import CompilerRegistry


def test_language_pack_round_trip_is_deterministic(tmp_path):
    definition = LanguageDefinition(
        name="ExampleLang",
        version="2026.1",
        aliases=("example",),
        source_extensions=("ex",),
        syntax={"grammar": "omni-pack-v1"},
        semantics={"evaluation": "specified"},
        type_rules={"typing": "gradual"},
        execution_model={"model": "stack"},
        memory_model={"model": "managed"},
        abi_expectations={"calling_convention": "target-defined"},
        dependency_rules={"resolution": "omni"},
    )
    path = tmp_path / "example.json"
    dump_language_pack(definition, path)
    assert load_language_pack(path) == definition
    assert json.loads(path.read_text(encoding="utf-8"))["identity"] == "ExampleLang@2026.1"


def test_language_pack_can_register_without_host_compiler(tmp_path):
    path = tmp_path / "future.json"
    path.write_text(
        '{"name":"FutureLang","version":"1","aliases":["future"],"source_extensions":["fl"]}',
        encoding="utf-8",
    )
    registry = CompilerRegistry()
    definition = register_language_pack(registry, path)
    assert registry.language_definition("future") is definition


def test_language_pack_rejects_missing_identity():
    with pytest.raises(LanguagePackError):
        definition_from_mapping({"name": "FutureLang"})
