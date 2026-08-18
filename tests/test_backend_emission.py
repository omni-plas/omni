import pytest

from omni.backends import Artifact, emit_with_backend
from omni.targets import TargetDescriptor


class Backend:
    def __init__(self, supported):
        self.supported = supported

    def supports_target(self, target):
        return target.platform == self.supported

    def emit(self, program, target):
        return Artifact(target, b"payload", "test")


def test_backend_emission_enforces_target_capability():
    target = TargetDescriptor(platform="future-os", architecture="future-cpu")
    with pytest.raises(LookupError):
        emit_with_backend(Backend("other-os"), object(), target)


def test_backend_emission_requires_artifact_result():
    class BadBackend(Backend):
        def emit(self, program, target):
            return b"not-an-artifact"

    target = TargetDescriptor(platform="future-os", architecture="future-cpu")
    with pytest.raises(TypeError):
        emit_with_backend(BadBackend("future-os"), object(), target)
