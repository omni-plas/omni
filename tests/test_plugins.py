import pytest

from omni.plugins import PluginRegistry


def test_registry_supports_future_language_and_target_names():
    registry = PluginRegistry()
    frontend = object()
    backend = object()
    registry.register_frontend("future-language", frontend)
    registry.register_backend("future-os/future-cpu", backend)
    assert registry.frontend("future-language") is frontend
    assert registry.backend("future-os/future-cpu") is backend


def test_registry_rejects_duplicate_plugins():
    registry = PluginRegistry()
    registry.register_frontend("lang", object())
    with pytest.raises(ValueError, match="already registered"):
        registry.register_frontend("lang", object())
