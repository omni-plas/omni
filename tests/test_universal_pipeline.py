from omni.backend import BackendRegistry, GenericArtifactBackend
from omni.frontend import FrontendRegistry
from omni.targets import TargetDescriptor
from omni.universal_pipeline import compile_universal
from omni.uir import UIR


class FutureFrontend:
    language = "future-language"

    def supports(self, language: str) -> bool:
        return language == self.language

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        target = TargetDescriptor("frontend-default", "default-cpu", "default-abi", {"semantic-artifact": True})
        return UIR(
            "1",
            {"kind": "future.entity"},
            {"language": self.language, "filename": filename},
            target.document(),
            {"program": source, "behavior": {"source": source}},
        )


def test_universal_pipeline_binds_requested_future_target():
    frontends = FrontendRegistry((FutureFrontend(),))
    backends = BackendRegistry((GenericArtifactBackend(),))
    target = TargetDescriptor("future-os", "future-cpu", "future-abi", {"semantic-artifact": True})
    result = compile_universal("future source", "future-language", target, frontends=frontends, backends=backends)
    assert result.frontend_name == "future-language"
    assert result.backend_name == GenericArtifactBackend.name
    assert result.plan.target == target


def test_universal_pipeline_accepts_open_world_target_identity():
    frontends = FrontendRegistry((FutureFrontend(),))
    backends = BackendRegistry((GenericArtifactBackend(),))
    target = TargetDescriptor("another-future-os", "another-future-cpu", "another-future-abi", {"semantic-artifact": True})
    result = compile_universal("source", "future-language", target, frontends=frontends, backends=backends)
    assert result.plan.target.platform == "another-future-os"
