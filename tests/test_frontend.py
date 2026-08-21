import pytest

from omni.frontend import FrontendRegistry


class FutureFrontend:
    language = "future-lang"

    def supports(self, language):
        return language == self.language

    def parse(self, source, *, filename="<source>"):
        return {"source": source, "filename": filename}


class AnotherFrontend:
    language = "another-lang"

    def supports(self, language):
        return language == self.language

    def parse(self, source, *, filename="<source>"):
        return {"source": source, "filename": filename}


def test_frontend_registry_resolves_open_world_language():
    registry = FrontendRegistry((FutureFrontend(),))
    assert registry.resolve("future-lang").language == "future-lang"
    assert registry.languages() == ("future-lang",)
    assert len(registry) == 1


def test_frontend_registry_register_and_unregister():
    registry = FrontendRegistry()
    registry.register(AnotherFrontend())
    assert registry.resolve("another-lang").parse("x", filename="x.src")["filename"] == "x.src"
    registry.unregister("another-lang")
    assert len(registry) == 0


def test_frontend_registry_rejects_duplicate_language():
    registry = FrontendRegistry((FutureFrontend(),))
    with pytest.raises(ValueError, match="already registered"):
        registry.register(FutureFrontend())


def test_frontend_registry_rejects_invalid_frontend():
    class Invalid:
        language = "invalid"

    with pytest.raises(TypeError, match="supports"):
        FrontendRegistry((Invalid(),))


def test_frontend_registry_rejects_blank_language():
    class Blank:
        language = " "
        supports = lambda self, language: True
        parse = lambda self, source, filename="<source>": None

    with pytest.raises(ValueError, match="non-empty"):
        FrontendRegistry((Blank(),))


def test_frontend_registry_reports_missing_language():
    registry = FrontendRegistry()
    with pytest.raises(LookupError):
        registry.resolve("language-that-does-not-exist-yet")


def test_frontend_registry_rejects_blank_resolution_language():
    registry = FrontendRegistry((FutureFrontend(),))
    with pytest.raises(ValueError, match="non-empty"):
        registry.resolve(" ")
