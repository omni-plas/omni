import math

import pytest

from omni.serialization import SerializationError, dumps_uir, loads_uir


def test_uir_serialization_is_deterministic_and_round_trips():
    document = {"version": "0.1", "entity": {"kind": "application"}, "extension": {"x": 1}}
    encoded = dumps_uir(document)
    assert encoded == '{"entity":{"kind":"application"},"extension":{"x":1},"version":"0.1"}'
    assert loads_uir(encoded) == document


def test_uir_json_requires_object_root():
    with pytest.raises(SerializationError, match="root must be an object"):
        loads_uir("[]")


def test_invalid_json_reports_location():
    with pytest.raises(SerializationError, match="line 1 column"):
        loads_uir('{"x":')


def test_non_standard_constants_are_rejected():
    with pytest.raises(SerializationError, match="NaN"):
        loads_uir('{"value": NaN}')


def test_nan_cannot_be_serialized():
    with pytest.raises(SerializationError, match="JSON-serializable"):
        dumps_uir({"value": math.nan})


def test_non_mapping_document_is_rejected():
    with pytest.raises(SerializationError, match="object"):
        dumps_uir([])
