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
        target = TargetDescriptor("frontend-default", "cpu", "abi", {"semantic-artifact": True})
        return UIR(
            "1",
            {"kind": "future.entity", "name": filename},
            {"language": self.language, "filename": filename},
            target.document(),
            {
                "program": {"source": source}, "types": {},
                "control_flow": {}, "data_flow": {}, "memory_model": {},
                "error_handling": {}, "io": {}, "dependencies": [],
                "security": {}, "performance": {},
            },
        )


def test_universal_pipeline_is_public_api():
    frontends = FrontendRegistry((PublicFutureFrontend(),))
    backends = BackendRegistry((GenericArtifactBackend(),))
    target = TargetDescriptor("requested-os", "requested-cpu", "requested-abi", {"semantic-artifact": True})
    result = compile_universal("x", "public-future", target, frontends=frontends, backends=backends)
    assert result.plan.target == target
    assert result.artifact.payload
