from omni.native_frame_encoding import epilogue, prologue


def test_frame_encoding_alignment():
    assert prologue(0)
    assert epilogue(0)
    assert len(prologue(16)) > len(prologue(0))
    assert len(epilogue(16)) > len(epilogue(0))
