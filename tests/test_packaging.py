import pytest

from omni.packaging import PackageManifest
from omni.targets import TargetDescriptor


def test_package_manifest_supports_future_targets():
    manifest = PackageManifest(
        "my-os", "0.1.0", TargetDescriptor("future-os", "future-cpu"),
        artifacts=("system.img",), dependencies=("runtime",),
        metadata={"installer": "required"},
    )
    updated = manifest.with_artifact("installer.img")
    assert manifest.artifacts == ("system.img",)
    assert updated.artifacts == ("system.img", "installer.img")


def test_package_manifest_validates_identity():
    with pytest.raises(ValueError, match="name"):
        PackageManifest("", "1", TargetDescriptor("os"))
    with pytest.raises(ValueError, match="version"):
        PackageManifest("os", "", TargetDescriptor("os"))


def test_package_manifest_validates_artifacts():
    with pytest.raises(ValueError, match="artifacts"):
        PackageManifest("os", "1", TargetDescriptor("os"), artifacts=("",))
