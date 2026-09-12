import pytest

from omni.language_definition import LanguageDefinition
from omni.registry import CompilerRegistry, RegistryError


class DummyFrontend:
    language = "x"


class DummyBackend:
    pass


def test_registry_supports_runtime_extensions():
    registry = CompilerRegistry()
    frontend = DummyFrontend()
    backend = DummyBackend()
    registry.register_frontend("x", frontend)
    registry.register_backend("future-os", backend)
    assert registry.frontend("x") is frontend
    assert registry.backend("future-os") is backend


def test_registry_rejects_duplicate_frontends():
    registry = CompilerRegistry()
    registry.register_frontend("x", DummyFrontend())
    with pytest.raises(RegistryError, match="already registered"):
        registry.register_frontend("x", DummyFrontend())


def test_registry_resolves_versioned_language_definitions_by_alias():
    registry = CompilerRegistry()
    definition = LanguageDefinition(
        name="FutureLang",
        version="1.0",
        aliases=("future",),
        source_extensions=("fl",),
    )
    registry.register_language_definition(definition)

    assert registry.language_definition("FutureLang") is definition
    assert registry.language_definition("future", "1.0") is definition
    assert registry.language_definition("future").identity == "FutureLang@1.0"


def test_registry_rejects_duplicate_language_identity():
    registry = CompilerRegistry()
    definition = LanguageDefinition(name="X", version="1")
    registry.register_language_definition(definition)
    with pytest.raises(RegistryError, match="already registered"):
        registry.register_language_definition(definition)
