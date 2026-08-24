from omni.native_call_patch import patch_call_rel32

def test_call_rel32_patch():
    code=bytearray(b'\xe8\x00\x00\x00\x00')+bytearray(b'xx')
    patch_call_rel32(code,0,10)
    assert int.from_bytes(code[1:5],'little',signed=True)==5
