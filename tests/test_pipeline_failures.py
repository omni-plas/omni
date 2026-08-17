import pytest

from omni.errors import ValidationError
from omni.pipeline import compile_semantics


def test_pipeline_converts_invalid_uir_to_public_validation_error():
    with pytest.raises(ValidationError):
        compile_semantics({})


def test_pipeline_rejects_invalid_target_descriptor():
    document = {
        "version": "1",
        "entity": {"kind": "program"},
        "source": {"language": "omni"},
        "target": {"platform": ""},
        "semantics": {"program": {}},
    }
    with pytest.raises(ValidationError):
        compile_semantics(document)
