import pytest

from omni.os_model import OSModelError, OperatingSystemSpec
from omni.targets import TargetDescriptor


def test_existing_os_can_be_modeled():
    spec = OperatingSystemSpec(
        "example-os",
        TargetDescriptor("existing-os", "x86_64", capabilities={"boot": "uefi"}),
        kernel="kernel.omni",
        bootloader="boot.omni",
        runtime="runtime.omni",
        filesystem="fs",
    )
    assert spec.requires_bootloader()
    assert spec.requires_filesystem()
    assert spec.target.capability("boot") == "uefi"


def test_historical_and_future_os_are_not_special_cases():
    historical = OperatingSystemSpec("old-os", TargetDescriptor("historical-os"), kernel="kernel")
    future = OperatingSystemSpec("new-os", TargetDescriptor("future-os"), kernel="kernel")
    assert historical.target.platform == "historical-os"
    assert future.target.platform == "future-os"


def test_os_requires_kernel_and_name():
    with pytest.raises(OSModelError, match="name"):
        OperatingSystemSpec("", TargetDescriptor("os"), kernel="kernel")
    with pytest.raises(OSModelError, match="kernel"):
        OperatingSystemSpec("os", TargetDescriptor("os"), kernel="")


def test_os_validates_optional_components():
    with pytest.raises(OSModelError, match="bootloader"):
        OperatingSystemSpec("os", TargetDescriptor("os"), kernel="k", bootloader=" ")
    with pytest.raises(OSModelError, match="drivers"):
        OperatingSystemSpec("os", TargetDescriptor("os"), kernel="k", drivers=("",))


def test_installation_capabilities_are_open_world():
    spec = OperatingSystemSpec(
        "future-os",
        TargetDescriptor("future-os"),
        kernel="k",
        installation_capabilities={"custom-installer": True},
    )
    assert spec.capability("custom-installer") is True
