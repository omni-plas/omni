from omni.artifact_io import read_artifact_file, write_artifact
from omni.native_artifact import compile_native_artifact


def test_artifact_file_round_trip(tmp_path):
    artifact = compile_native_artifact(
        "entity = application\nname = hello\nplatform = semantic-artifact\narchitecture = universal\nabi = universal\n"
    )
    path = write_artifact(tmp_path / "hello.omniart", artifact.payload)
    document = read_artifact_file(path)
    assert document["entity"]["name"] == "hello"
