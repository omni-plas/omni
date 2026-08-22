import pytest

from omni.backend import BackendError, BackendRegistry, GenericArtifactBackend
from omni.compiler import CompilationPlan
from omni.targets import TargetDescriptor


class Backend:
    name = "future"

    def supports(self, target):
        return target.platform == "future-os"

    def compile(self, uir, plan):
        raise AssertionError("compile not needed for registry tests")


def test_registry_is_open_world():
    registry = BackendRegistry().register(Backend()).register(GenericArtifactBackend())
    assert registry.names() == ("future", "generic-semantic-artifact")
    assert registry.select(TargetDescriptor("future-os")).backend.name == "future"


def test_registry_rejects_duplicate_backend():
    registry = BackendRegistry().register(Backend())
    with pytest.raises(BackendError, match="already registered"):
        registry.register(Backend())


def test_registry_rejects_unsupported_target():
    with pytest.raises(BackendError, match="no backend"):
        BackendRegistry().select(TargetDescriptor("unknown-os"))
