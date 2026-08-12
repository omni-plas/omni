import pytest

from omni.targeting import TargetResolutionError, resolve_target
from omni.targets import TargetDescriptor


class Backend:
    def __init__(self, platform):
        self.platform = platform

    def supports_target(self, target):
        return target.platform == self.platform


def test_target_resolution_is_capability_driven():
    target = TargetDescriptor(platform="future-os", architecture="future-cpu")
    backend = Backend("future-os")
    match = resolve_target(target, [Backend("other-os"), backend])
    assert match.backend is backend
    assert match.target == target


def test_target_resolution_rejects_unsupported_target():
    target = TargetDescriptor(platform="unknown-os")
    with pytest.raises(TargetResolutionError):
        resolve_target(target, [Backend("known-os")])
