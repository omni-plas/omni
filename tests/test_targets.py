import json

import pytest

from omni.targets import TargetDescriptor, TargetError


def test_target_descriptor_supports_open_world_targets():
    target = TargetDescriptor(
        platform="future-os", architecture="future-cpu", abi="future-abi",
        capabilities={"graphics": "next-gen"},
    )
    assert target.identity() == "future-os-future-cpu-future-abi"
    assert target.capabilities["graphics"] == "next-gen"
    assert target.capability("graphics") == "next-gen"
    assert target.supports("graphics", "next-gen")
    assert not target.supports("graphics", "legacy")


def test_target_descriptor_supports_structured_capabilities():
    target = TargetDescriptor("future-os", capabilities={"memory": {"tagged": True, "width": 128}})
    assert target.capability("memory")["tagged"] is True
    assert target.supports("memory", {"tagged": True, "width": 128})


def test_target_require_reports_missing_capability():
    target = TargetDescriptor("future-os")
    with pytest.raises(TargetError, match="lacks capability graphics"):
        target.require("graphics")


def test_target_can_be_extended_immutably():
    target = TargetDescriptor("future-os")
    extended = target.with_capability("runtime", "omni-v1")
    assert not target.supports("runtime")
    assert extended.supports("runtime", "omni-v1")


def test_target_rejects_blank_capability_values():
    with pytest.raises(TargetError, match="capability values"):
        TargetDescriptor("future-os", capabilities={"graphics": " "})


def test_target_rejects_blank_capability_names():
    with pytest.raises(TargetError, match="capability names"):
        TargetDescriptor("future-os", capabilities={" ": True})


def test_target_rejects_invalid_capability_queries():
    target = TargetDescriptor("future-os")
    with pytest.raises(TargetError, match="capability name"):
        target.capability(" ")
    with pytest.raises(TargetError, match="capability name"):
        target.supports("")


def test_target_identity_and_fields_are_normalized():
    target = TargetDescriptor(" future-os ", " future-cpu ", " future-abi ")
    assert target.identity() == "future-os-future-cpu-future-abi"


def test_target_document_is_versioned_and_round_trips():
    target = TargetDescriptor(
        "historical-os", "legacy-cpu", capabilities={"era": "1990s", "boot": {"mode": "legacy"}}
    )
    document = target.document()
    assert document["schema"] == "omni.target.v1"
    assert TargetDescriptor.from_document(document) == target
    assert TargetDescriptor.deserialize(target.serialize()) == target


def test_target_serialization_is_deterministic():
    target = TargetDescriptor("os", capabilities={"z": 2, "a": 1})
    assert target.serialize() == target.serialize()
    assert json.loads(target.serialize())["capabilities"] == {"a": 1, "z": 2}


def test_target_rejects_unknown_schema():
    with pytest.raises(TargetError, match="unsupported"):
        TargetDescriptor.from_document({"schema": "other.v1", "platform": "os"})


def test_target_rejects_invalid_json():
    with pytest.raises(TargetError, match="invalid target JSON"):
        TargetDescriptor.deserialize("{")


def test_target_rejects_non_serializable_capabilities():
    target = TargetDescriptor("os", capabilities={"value": object()})
    with pytest.raises(TargetError, match="not JSON-serializable"):
        target.serialize()
