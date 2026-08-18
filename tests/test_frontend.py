import pytest

from omni.frontend import FrontendRegistry


class FutureFrontend:
    language = "future-lang"

    def supports(self, language):
        return language == self.language

    def parse(self, source, *, filename="<source>"):
        raise NotImplementedError


def test_frontend_registry_resolves_open_world_language():
    registry = FrontendRegistry((FutureFrontend(),))
    assert registry.resolve("future-lang").language == "future-lang"
    assert registry.languages() == ("future-lang",)


def test_frontend_registry_reports_missing_language():
    registry = FrontendRegistry()
    with pytest.raises(LookupError):
        registry.resolve("language-that-does-not-exist-yet")
