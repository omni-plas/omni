import pytest

from omni.frontend_metadata import FrontendMetadata


def test_metadata_matches_alias_version_and_extension():
    metadata = FrontendMetadata(
        "C++", aliases=frozenset({"cpp", "cxx"}), versions=frozenset({"23"}), source_extensions=frozenset({".cpp"}), priority=10
    )
    assert metadata.matches_language("cpp")
    assert metadata.matches_version("23")
    assert metadata.matches_extension(".CPP")


def test_metadata_rejects_invalid_extensions():
    with pytest.raises(ValueError):
        FrontendMetadata("x", source_extensions=frozenset({"cpp"}))
