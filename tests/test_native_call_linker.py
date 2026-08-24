from omni.native_call_linker import NativeCallSite, link_functions

def test_internal_call_symbol_is_linked():
    caller=b'\x90\xe8\x00\x00\x00\x00\xc3'
    callee=b'\xc3'
    linked=link_functions((('caller',caller,(NativeCallSite(2,6,'callee'),)),('callee',callee,())))
    assert linked.symbols['caller']==0
    assert linked.symbols['callee']==len(caller)
    assert linked.code[1]==0xe8
    assert linked.code[2:6]==(len(caller)-6).to_bytes(4,'little',signed=True)
