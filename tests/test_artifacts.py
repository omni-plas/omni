import pytest

from omni.artifacts import ArtifactError, ArtifactManifest, manifest
from omni.targets import TargetDescriptor


def test_manifest_is_content_addressed_and_deterministic():
    target = TargetDescriptor("future-os", "future-cpu")
    first = manifest(b"hello", target, "binary", name="system", kind="os-image")
    second = manifest(b"hello", target, "binary", name="system", kind="os-image")
    assert first == second
    assert first.size == 5
    assert first.key().startswith("sha256:")
    assert first.identity().startswith("os-image:system:future-os-future-cpu:")


def test_manifest_normalizes_format():
    result = manifest(b"x", TargetDescriptor("future-os"), " binary ")
    assert result.format == "binary"


def test_manifest_rejects_invalid_payload_and_format():
    with pytest.raises(TypeError):
        manifest("x", TargetDescriptor("future-os"), "binary")
    with pytest.raises(ValueError):
        manifest(b"x", TargetDescriptor("future-os"), " ")


def test_manifest_validates_digest_shape():
    with pytest.raises(ArtifactError, match="SHA-256"):
        ArtifactManifest(TargetDescriptor("future-os"), "binary", "bad", 1)


def test_manifest_rejects_negative_or_boolean_size():
    with pytest.raises(ArtifactError, match="negative"):
        ArtifactManifest(TargetDescriptor("future-os"), "binary", "0" * 64, -1)
    with pytest.raises(ArtifactError, match="negative"):
        ArtifactManifest(TargetDescriptor("future-os"), "binary", "0" * 64, True)


def test_manifest_rejects_invalid_optional_identity_fields():
    with pytest.raises(ArtifactError, match="name"):
        manifest(b"x", TargetDescriptor("future-os"), "binary", name=" ")
    with pytest.raises(ArtifactError, match="kind"):
        manifest(b"x", TargetDescriptor("future-os"), "binary", kind=" ")
