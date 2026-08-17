from omni.backends import Artifact
from omni.targeting import resolve_target
from omni.targets import TargetDescriptor


class Backend:
    def __init__(self, platform):
        self.platform = platform

    def supports_target(self, target):
        return target.platform == self.platform

    def emit(self, program, target):
        return Artifact(target=target, payload=b"artifact", format="test")


def test_backend_contract_supports_open_world_targets():
    target = TargetDescriptor(platform="future-os", architecture="future-cpu")
    backend = Backend("future-os")
    assert resolve_target(target, [backend]).backend is backend
