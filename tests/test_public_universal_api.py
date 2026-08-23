from omni import (
    BackendRegistry,
    FrontendRegistry,
    GenericArtifactBackend,
    TargetDescriptor,
    UIR,
    compile_universal,
)


class PublicFutureFrontend:
    language = "public-future"

    def supports(self, language: str) -> bool:
        return language == self.language

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        target = TargetDescriptor("frontend-default", "cpu", "abi")
        return UIR("future.entity", target, {"source": source, "filename": filename})


def test_universal_pipeline_is_public_api():
    frontends = FrontendRegistry((PublicFutureFrontend(),))
    backends = BackendRegistry((GenericArtifactBackend(),))
    target = TargetDescriptor("requested-os", "requested-cpu", "requested-abi")
    result = compile_universal("x", "public-future", target, frontends=frontends, backends=backends)
    assert result.plan.target == target
    assert result.artifact.payload
