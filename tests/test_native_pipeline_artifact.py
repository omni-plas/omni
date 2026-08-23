from omni.native_backend import read_artifact
from omni.native_pipeline import compile_native


def test_native_pipeline_emits_portable_artifact():
    result = compile_native(
        "entity = application\nname = hello\nplatform = semantic-artifact\narchitecture = universal\nabi = universal\n"
    )
    assert result.ok
    artifact = result.compilation.artifact
    document = read_artifact(artifact.payload)
    assert document["entity"]["name"] == "hello"
