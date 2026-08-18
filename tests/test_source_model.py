import pytest

from omni.source_model import SourceNode, SourceSpan, SourceUnit


def test_source_model_is_language_neutral():
    root = SourceNode(
        "program",
        children=(SourceNode("literal", value="42", span=SourceSpan(0, 2)),),
    )
    unit = SourceUnit("future-language", root, "future.omni")
    assert unit.to_dict()["language"] == "future-language"
    assert unit.to_dict()["root"]["children"][0]["value"] == "42"


def test_source_span_rejects_invalid_range():
    with pytest.raises(ValueError):
        SourceSpan(5, 2)
