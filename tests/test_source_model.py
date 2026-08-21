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


def test_source_span_rejects_invalid_range_and_exposes_length():
    with pytest.raises(ValueError):
        SourceSpan(5, 2)
    assert SourceSpan(2, 7).length == 5


def test_source_span_requires_integer_offsets():
    with pytest.raises(TypeError, match="integers"):
        SourceSpan("0", 1)


def test_source_node_rejects_invalid_shape():
    with pytest.raises(ValueError, match="kind"):
        SourceNode(" ")
    with pytest.raises(TypeError, match="attributes"):
        SourceNode("node", attributes=[])
    with pytest.raises(TypeError, match="children"):
        SourceNode("node", children=[])
    with pytest.raises(TypeError, match="SourceNode"):
        SourceNode("node", children=("bad",))


def test_source_unit_rejects_invalid_root_and_filename():
    with pytest.raises(TypeError, match="root"):
        SourceUnit("future", object())
    with pytest.raises(ValueError, match="filename"):
        SourceUnit("future", SourceNode("root"), " ")


def test_source_metadata_and_attributes_are_preserved():
    root = SourceNode("root", attributes={"future": {"enabled": True}})
    unit = SourceUnit("future-language", root, metadata={"vendor": "future"})
    result = unit.to_dict()
    assert result["root"]["attributes"]["future"]["enabled"] is True
    assert result["metadata"]["vendor"] == "future"
