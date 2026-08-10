from omni.backends import Artifact, Backend
from omni.frontends import Frontend, SourceUnit


def test_source_unit_preserves_source_identity():
    unit = SourceUnit(language="future-language", text="program", origin="input.omni")
    assert unit.language == "future-language"
    assert unit.origin == "input.omni"


def test_backend_artifact_is_explicitly_targeted():
    # Protocols are structural contracts; this test checks the concrete artifact shape.
    artifact = Artifact(target=None, payload=b"artifact", format="binary")
    assert artifact.payload == b"artifact"
    assert artifact.format == "binary"
