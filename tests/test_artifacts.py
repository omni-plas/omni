import pytest

from omni.artifacts import ArtifactManifest, manifest
from omni.targets import TargetDescriptor


def test_manifest_is_content_addressed_and_deterministic():
    target = TargetDescriptor("future-os", "future-cpu")
    first = manifest(b"hello", target, "binary")
    second = manifest(b"hello", target, "binary")
    assert first == second
    assert first.size == 5
    assert first.key().startswith("sha256:")


def test_manifest_normalizes_format():
    result = manifest(b"x", TargetDescriptor("future-os"), " binary ")
    assert result.format == "binary"


def test_manifest_rejects_invalid_payload_and_format():
    with pytest.raises(TypeError):
        manifest("x", TargetDescriptor("future-os"), "binary")
    with pytest.raises(ValueError):
        manifest(b"x", TargetDescriptor("future-os"), " ")


def test_manifest_validates_digest_shape():
    with pytest.raises(ValueError, match="SHA-256"):
        ArtifactManifest(TargetDescriptor("future-os"), "binary", "bad", 1)


def test_manifest_rejects_negative_size():
    with pytest.raises(ValueError, match="negative"):
        ArtifactManifest(TargetDescriptor("future-os"), "binary", "0" * 64, -1)
