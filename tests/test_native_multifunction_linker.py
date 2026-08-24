from omni.native_multifunction_linker import link

def test_local_call_is_patched():
    payload,offsets=link((('main',b'\xe8\x00\x00\x00\x00\xc3',((0,'helper'),)),('helper',b'\xc3',())))
    assert offsets['helper']==6
    assert int.from_bytes(payload[1:5],'little',signed=True)==1
