import io
import zipfile

import pytest

from omni.package_writer import PackageWriteError, build_package
from omni.packaging import PackageManifest
from omni.targets import TargetDescriptor


def _manifest():
    target = TargetDescriptor("future-os", "future-cpu")
    return PackageManifest("future-product", "1", target, artifacts=("bin/app", "data/config"))


def test_build_package_contains_manifest_and_declared_entries():
    payload = build_package(_manifest(), {"bin/app": b"app", "data/config": b"config"})
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        assert archive.namelist() == ["manifest.json", "bin/app", "data/config"]
        assert archive.read("bin/app") == b"app"
        assert archive.read("data/config") == b"config"
        assert b"omni.package.v1" in archive.read("manifest.json")


def test_build_package_is_deterministic():
    entries = {"bin/app": b"app", "data/config": b"config"}
    assert build_package(_manifest(), entries) == build_package(_manifest(), entries)


def test_build_package_rejects_missing_or_extra_entries():
    with pytest.raises(PackageWriteError, match="do not match"):
        build_package(_manifest(), {"bin/app": b"app"})
    with pytest.raises(PackageWriteError, match="do not match"):
        build_package(_manifest(), {"bin/app": b"app", "data/config": b"config", "extra": b"x"})


def test_build_package_rejects_path_escape():
    manifest = PackageManifest("product", "1", TargetDescriptor("os"), artifacts=("../escape",))
    with pytest.raises(PackageWriteError, match="path"):
        build_package(manifest, {"../escape": b"x"})


def test_build_package_rejects_non_bytes_payload():
    manifest = PackageManifest("product", "1", TargetDescriptor("os"), artifacts=("app",))
    with pytest.raises(TypeError, match="bytes"):
        build_package(manifest, {"app": "not-bytes"})
