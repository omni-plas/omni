import pytest

from omni.target_specs import TargetSpecification
from omni.targets import TargetDescriptor


def test_target_specification_models_future_platforms():
    spec = TargetSpecification(
        TargetDescriptor("future-os", "future-cpu", "future-abi"),
        semantics={"memory": "capability-based"},
        abi="future-abi",
        executable_format="future-exe",
        boot_protocol="future-boot",
        package_format="future-pkg",
        installation_protocol="future-install",
    )
    assert spec.can_boot()
    assert spec.can_install()
    assert spec.capability("memory") == "capability-based"


def test_target_spec_rejects_invalid_target():
    with pytest.raises(TypeError, match="TargetDescriptor"):
        TargetSpecification(None)


def test_target_spec_rejects_empty_protocol():
    with pytest.raises(ValueError, match="boot_protocol"):
        TargetSpecification(TargetDescriptor("os"), boot_protocol=" ")
