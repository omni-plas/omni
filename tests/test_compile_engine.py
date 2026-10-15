from omni.backend import BackendRegistry, GenericArtifactBackend
from omni.compile_engine import compile_uir


def document():
    return {
        "version": "1",
        "entity": {"kind": "application", "name": "demo"},
        "source": {"language": "omni", "version": "1"},
        "target": {"platform": "future-os", "capabilities": {"semantic-artifact": True}},
        "semantics": {
            "program": {"entry": "main"}, "types": {}, "control_flow": {}, "data_flow": {},
            "memory_model": {}, "error_handling": {}, "io": {}, "dependencies": [],
            "security": {}, "performance": {},
        },
    }


def test_compile_engine_selects_backend_and_generates_artifact():
    result = compile_uir(document(), BackendRegistry().register(GenericArtifactBackend()))
    assert result.backend_name == "generic-semantic-artifact"
    assert result.artifact.kind == "application"
    assert result.artifact.target.platform == "future-os"
    assert result.artifact.manifest.digest
