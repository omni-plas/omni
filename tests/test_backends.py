import pytest

from omni.backends import Artifact, emit_with_backend
from omni.targets import TargetDescriptor


class BackendImpl:
    def __init__(self, supported=True, wrong_target=False):
        self.supported = supported
        self.wrong_target = wrong_target

    def supports_target(self, target):
        return self.supported

    def emit(self, program, target):
        output_target = TargetDescriptor("other") if self.wrong_target else target
        return Artifact(output_target, b"artifact", "binary")


def test_backend_emits_artifact_when_target_supported():
    target = TargetDescriptor("future-os")
    artifact = emit_with_backend(BackendImpl(), object(), target)
    assert artifact.target == target
    assert artifact.payload == b"artifact"


def test_backend_rejects_unsupported_target():
    with pytest.raises(LookupError, match="does not support"):
        emit_with_backend(BackendImpl(False), object(), TargetDescriptor("future-os"))


def test_backend_rejects_wrong_target_artifact():
    with pytest.raises(ValueError, match="different target"):
        emit_with_backend(BackendImpl(wrong_target=True), object(), TargetDescriptor("future-os"))


def test_artifact_rejects_non_bytes_payload():
    with pytest.raises(TypeError, match="bytes"):
        Artifact(TargetDescriptor("future-os"), "text", "binary")


def test_artifact_rejects_blank_format():
    with pytest.raises(ValueError, match="format"):
        Artifact(TargetDescriptor("future-os"), b"x", " ")


def test_backend_contract_requires_methods():
    with pytest.raises(TypeError, match="supports_target"):
        emit_with_backend(object(), object(), TargetDescriptor("future-os"))
