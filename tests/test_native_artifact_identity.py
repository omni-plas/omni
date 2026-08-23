from omni.native_artifact_identity import sha256, verify_digest


def test_digest_is_stable():
    digest=sha256(b'omni')
    assert len(digest)==64
    assert verify_digest(b'omni',digest)
    assert not verify_digest(b'other',digest)
