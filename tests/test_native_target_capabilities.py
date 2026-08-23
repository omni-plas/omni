import pytest
from omni.native_target_capabilities import TargetCapabilities


def test_required_capabilities_are_checked():
    caps=TargetCapabilities()
    assert caps.require(call_rel32=True,stack_arguments=True,relocations=True)


def test_missing_capability_fails():
    caps=TargetCapabilities(relocations=False)
    with pytest.raises(ValueError):
        caps.require(relocations=True)
