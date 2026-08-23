import pytest

from omni.native_artifact import compile_native_artifact
from omni.target_artifact import validate_artifact_for_target
from omni.targets import TargetDescriptor


def test_artifact_target_validation_accepts_matching_target():
    artifact = compile_native_artifact(
        "entity = application\nname = hello\nplatform = semantic-artifact\narchitecture = universal\nabi = universal\n"
    )
    assert validate_artifact_for_target(artifact.payload, artifact.target)["entity"]["name"] == "hello"


def test_artifact_target_validation_rejects_mismatch():
    artifact = compile_native_artifact(
        "entity = application\nname = hello\nplatform = semantic-artifact\narchitecture = universal\nabi = universal\n"
    )
    with pytest.raises(ValueError, match="does not match"):
        validate_artifact_for_target(artifact.payload, TargetDescriptor("other-target"))
