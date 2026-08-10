import pytest

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
