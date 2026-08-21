import pytest

from omni.targeting import TargetResolutionError, resolve_target
from omni.targets import TargetDescriptor


class Backend:
    def __init__(self, platform, *, raises=False):
        self.platform = platform
        self.raises = raises

    def supports_target(self, target):
        if self.raises:
            raise RuntimeError("capability probe failed")
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


def test_target_resolution_skips_invalid_backend_contracts():
    target = TargetDescriptor("future-os")
    match = resolve_target(target, [object(), Backend("future-os")])
    assert match.backend.platform == "future-os"


def test_target_resolution_rejects_missing_backend_collection():
    with pytest.raises(TypeError, match="backends"):
        resolve_target(TargetDescriptor("future-os"), None)


def test_target_resolution_rejects_invalid_target():
    with pytest.raises(TypeError, match="TargetDescriptor"):
        resolve_target("future-os", [])


def test_target_resolution_reports_backend_probe_failure():
    with pytest.raises(TargetResolutionError, match="failed while checking"):
        resolve_target(TargetDescriptor("future-os"), [Backend("future-os", raises=True)])
