from omni.native_global_refs import GlobalRef, apply_global_refs


def test_patch_absolute_image_offset():
    code=bytearray(b'\x00'*8)
    apply_global_refs(code,(GlobalRef(0,0x1234,4),))
    assert int.from_bytes(code[:4],'little')==0x1234


def test_patch_64bit_offset():
    code=bytearray(b'\x00'*8)
    apply_global_refs(code,(GlobalRef(0,0x123456789,8),))
    assert int.from_bytes(code,'little')==0x123456789
