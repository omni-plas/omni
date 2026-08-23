from omni.backend import BackendRegistry, GenericArtifactBackend
from omni.frontend import FrontendRegistry
from omni.target_model import TargetModel
from omni.targets import TargetDescriptor
from omni.universal_pipeline import UniversalPipelineError, compile_universal
from omni.uir import UIR


class FutureFrontend:
    language = "future-language"

    def supports(self, language: str) -> bool:
        return language == self.language

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        target = TargetDescriptor("future-os", "future-cpu", "future-abi", {"semantic-artifact": True})
        return UIR("future.entity", target, {"source": source, "filename": filename})


def test_universal_pipeline_accepts_future_language_and_target():
    frontend = FrontendRegistry((FutureFrontend(),))
    backend = BackendRegistry((GenericArtifactBackend(),))
    target = TargetDescriptor("future-os", "future-cpu", "future-abi", {"semantic-artifact": True})
    result = compile_universal("future source", "future-language", target, frontends=frontend, backends=backend)
    assert result.frontend_name == "future-language"
    assert result.backend_name == GenericArtifactBackend.name
    assert result.artifact.payload


def test_universal_pipeline_rejects_target_mismatch():
    frontend = FrontendRegistry((FutureFrontend(),))
    backend = BackendRegistry((GenericArtifactBackend(),))
    requested = TargetDescriptor("other-os", "other-cpu", "other-abi", {"semantic-artifact": True})
    try:
        compile_universal("future source", "future-language", requested, frontends=frontend, backends=backend)
    except UniversalPipelineError:
        return
    raise AssertionError("target mismatch must fail")
