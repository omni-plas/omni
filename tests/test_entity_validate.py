import pytest

from omni.entity_validate import entity_from_mapping
from omni.uir import UIRValidationError


def test_unknown_entity_kind_is_valid_when_formally_defined():
    entity = entity_from_mapping({
        "kind": "future-digital-organism",
        "name": "x",
        "structure": {"nodes": []},
        "behavior": {"steps": []},
        "inputs": [{"name": "in"}],
        "outputs": [{"name": "out"}],
        "execution": {"model": "future-runtime"},
    })
    assert entity.kind == "future-digital-organism"


def test_entity_requires_named_ports():
    with pytest.raises(UIRValidationError, match="ports"):
        entity_from_mapping({"kind": "thing", "name": "x", "inputs": [{"name": ""}]})
