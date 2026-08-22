import json

import pytest

from omni.packaging import PackageError, PackageManifest
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


def test_package_manifest_rejects_duplicates():
    with pytest.raises(PackageError, match="unique"):
        PackageManifest("os", "1", TargetDescriptor("os"), artifacts=("a", "a"))
    manifest = PackageManifest("os", "1", TargetDescriptor("os"), dependencies=("runtime",))
    with pytest.raises(PackageError, match="unique"):
        manifest.with_dependency("runtime")


def test_package_manifest_supports_immutable_dependency_extension():
    manifest = PackageManifest("os", "1", TargetDescriptor("os"))
    updated = manifest.with_dependency("runtime")
    assert manifest.dependencies == ()
    assert updated.dependencies == ("runtime",)


def test_package_manifest_is_deterministic():
    manifest = PackageManifest(
        "os", "1", TargetDescriptor("future-os", "cpu", "abi", {"boot": "next"}),
        artifacts=("kernel",), dependencies=("runtime",), metadata={"channel": "future"},
    )
    document = json.loads(manifest.manifest())
    assert document["schema"] == "omni.package.v1"
    assert document["target"]["schema"] == "omni.target.v1"
    assert manifest.manifest() == manifest.manifest()
