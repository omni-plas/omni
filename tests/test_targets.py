import pytest

from omni.targets import TargetDescriptor


def test_target_descriptor_supports_open_world_targets():
    target = TargetDescriptor(
        platform="future-os", architecture="future-cpu", abi="future-abi",
        capabilities={"graphics": "next-gen"},
    )
    assert target.identity() == "future-os-future-cpu-future-abi"
    assert target.capabilities["graphics"] == "next-gen"
    assert target.supports("graphics", "next-gen")
    assert not target.supports("graphics", "legacy")


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
