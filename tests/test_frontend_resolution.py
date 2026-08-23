from omni.frontend import FrontendRegistry
from omni.frontend_metadata import FrontendMetadata


class FrontendImpl:
    def __init__(self, language, metadata):
        self.language = language
        self.metadata = metadata

    def supports(self, language):
        return self.metadata.matches_language(language)

    def parse(self, source, *, filename="<source>"):
        raise NotImplementedError


def test_resolution_prefers_priority_and_is_case_insensitive():
    old = FrontendImpl("C++-old", FrontendMetadata("C++", aliases=frozenset({"cpp"}), versions=frozenset({"17"}), priority=1))
    new = FrontendImpl("C++-new", FrontendMetadata("C++", aliases=frozenset({"cpp"}), versions=frozenset({"23"}), priority=5))
    registry = FrontendRegistry((old, new))
    assert registry.resolve("CPP", version="23") is new
    assert registry.discover("cpp", version="17").frontend is old


def test_discovery_explains_match():
    frontend = FrontendImpl("Go", FrontendMetadata("Go", aliases=frozenset({"golang"}), priority=2))
    candidate = FrontendRegistry((frontend,)).discover("golang")
    assert candidate.reason == "metadata match"
