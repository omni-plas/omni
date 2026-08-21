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
    assert registry.languages() == ("future-language",)
    assert registry.targets() == ("future-os/future-cpu",)


def test_registry_rejects_duplicate_plugins():
    registry = PluginRegistry()
    registry.register_frontend("lang", object())
    with pytest.raises(ValueError, match="already registered"):
        registry.register_frontend("lang", object())


def test_registry_rejects_invalid_names_and_plugins():
    registry = PluginRegistry()
    with pytest.raises(ValueError, match="non-empty"):
        registry.register_frontend(" ", object())
    with pytest.raises(TypeError, match="string"):
        registry.register_backend(None, object())
    with pytest.raises(TypeError, match="None"):
        registry.register_frontend("lang", None)


def test_registry_supports_unregister():
    registry = PluginRegistry()
    frontend, backend = object(), object()
    registry.register_frontend("lang", frontend)
    registry.register_backend("target", backend)
    assert registry.unregister_frontend("lang") is frontend
    assert registry.unregister_backend("target") is backend
    with pytest.raises(LookupError):
        registry.frontend("lang")
    with pytest.raises(LookupError):
        registry.backend("target")
