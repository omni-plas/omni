import pytest

from omni.targets import TargetDescriptor


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
    with pytest.raises(ValueError, match="lacks capability graphics"):
        target.require("graphics")


def test_target_can_be_extended_immutably():
    target = TargetDescriptor("future-os")
    extended = target.with_capability("runtime", "omni-v1")
    assert not target.supports("runtime")
    assert extended.supports("runtime", "omni-v1")


def test_target_rejects_blank_capability_values():
    with pytest.raises(ValueError, match="capability values"):
        TargetDescriptor("future-os", capabilities={"graphics": " "})


def test_target_rejects_blank_capability_names():
    with pytest.raises(ValueError, match="capability names"):
        TargetDescriptor("future-os", capabilities={" ": True})


def test_target_rejects_invalid_capability_queries():
    target = TargetDescriptor("future-os")
    with pytest.raises(ValueError, match="capability name"):
        target.capability(" ")
    with pytest.raises(ValueError, match="capability name"):
        target.supports("")
