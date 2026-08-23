from omni.native_reproducibility import manifest_digest, verify_reproducible


def test_manifest_digest_is_deterministic():
    m={'target':'x86_64-linux-sysv','entry':'main','sources':['a','b']}
    assert manifest_digest(m)==manifest_digest(m)
    assert verify_reproducible('abc','abc')
    assert not verify_reproducible('abc','def')
