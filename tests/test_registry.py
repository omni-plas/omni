import pytest

from omni.language_definition import LanguageDefinition
from omni.registry import CompilerRegistry, RegistryError


class DummyFrontend:
    language = "x"

    def lower(self, source):
        return source


class DummyBackend:
    def supports_target(self, target):
        return True

    def emit(self, program, target):
        return None


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
    assert registry.language_definition_for_extension(".fl") is definition


def test_registry_resolves_frontend_from_extension():
    registry = CompilerRegistry()
    definition = LanguageDefinition(name="FutureLang", version="1", source_extensions=("fl",))
    frontend = DummyFrontend()
    registry.register_language_definition(definition)
    registry.register_frontend("FutureLang", frontend)
    assert registry.frontend_for_extension("fl") is frontend


def test_registry_rejects_duplicate_language_identity():
    registry = CompilerRegistry()
    definition = LanguageDefinition(name="X", version="1")
    registry.register_language_definition(definition)
    with pytest.raises(RegistryError, match="already registered"):
        registry.register_language_definition(definition)


def test_registry_rejects_unusable_frontend_and_backend():
    registry = CompilerRegistry()
    with pytest.raises(RegistryError, match="lower"):
        registry.register_frontend("broken", object())
    with pytest.raises(RegistryError, match="supports_target"):
        registry.register_backend("broken", object())


def test_registry_resolves_frontend_from_language_alias_and_version():
    registry = CompilerRegistry()
    definition = LanguageDefinition(
        name="FutureLang",
        version="2.0",
        aliases=("future",),
        source_extensions=("fl",),
    )
    frontend = DummyFrontend()
    registry.register_language_definition(definition)
    registry.register_frontend("FutureLang", frontend)

    assert registry.frontend_for_language("future") is frontend
    assert registry.frontend_for_language("FUTURE", "2.0") is frontend


def test_registry_reports_definition_without_executable_frontend():
    registry = CompilerRegistry()
    registry.register_language_definition(
        LanguageDefinition(name="FutureLang", version="1", source_extensions=("fl",))
    )
    with pytest.raises(RegistryError, match="definition but no executable frontend"):
        registry.frontend_for_extension("fl")
