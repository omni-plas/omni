from omni.reproducible_build import fingerprint

def test_fingerprint_is_deterministic():
    assert fingerprint('omni','x',1)==fingerprint('omni','x',1)
    assert fingerprint('omni','x')!=fingerprint('omni','y')
