import pytest

from omni.serialization import dumps_uir, loads_uir


def test_uir_serialization_is_deterministic_and_round_trips():
    document = {"version": "0.1", "entity": {"kind": "application"}, "extension": {"x": 1}}
    encoded = dumps_uir(document)
    assert encoded == '{"entity":{"kind":"application"},"extension":{"x":1},"version":"0.1"}'
    assert loads_uir(encoded) == document


def test_uir_json_requires_object_root():
    with pytest.raises(ValueError, match="root must be an object"):
        loads_uir("[]")
