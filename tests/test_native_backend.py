import json

from omni.backend import BackendRegistry
from omni.native_backend import NativeArtifactBackend, read_artifact
from omni.native_frontend import OmniNativeFrontend
from omni.compiler import plan_compilation


def _uir():
    return OmniNativeFrontend().parse(
        "entity = application\nname = hello\nplatform = semantic-artifact\narchitecture = universal\nabi = universal\n"
    )


def test_native_backend_round_trip():
    uir = _uir()
    plan = plan_compilation(uir)
    artifact = NativeArtifactBackend().compile(uir, plan)
    assert artifact.format == "omni-artifact"
    document = read_artifact(artifact.payload)
    assert document["entity"]["name"] == "hello"


def test_native_backend_payload_is_deterministic():
    uir = _uir()
    plan = plan_compilation(uir)
    backend = NativeArtifactBackend()
    assert backend.compile(uir, plan).payload == backend.compile(uir, plan).payload


def test_corrupt_artifact_is_rejected():
    uir = _uir()
    plan = plan_compilation(uir)
    payload = bytearray(NativeArtifactBackend().compile(uir, plan).payload)
    payload[-1] ^= 1
    try:
        read_artifact(bytes(payload))
    except ValueError as exc:
        assert "corrupt" in str(exc)
    else:
        raise AssertionError("corrupt artifact was accepted")
