import pytest

from omni.uir import UIRValidationError, validate_uir


def base():
    return {
        "version": "1",
        "entity": {"kind": "future.digital"},
        "source": {"language": "future-language"},
        "target": {"platform": "future-platform"},
        "semantics": {"program": {"operations": []}},
    }


def test_future_language_and_platform_remain_open_world():
    uir = validate_uir(base())
    assert uir.source["language"] == "future-language"
    assert uir.target["platform"] == "future-platform"


@pytest.mark.parametrize("field", ["source", "target"])
def test_descriptor_requires_string_identity(field):
    document = base()
    document[field] = {}
    with pytest.raises(UIRValidationError):
        validate_uir(document)
