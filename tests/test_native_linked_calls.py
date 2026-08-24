from omni.native_linked_calls import build_linked_call

def test_internal_call_symbol_is_resolved():
    linked=build_linked_call('caller',b'', 'callee', (), {})
    assert linked.symbols['caller']==0
    assert linked.symbols['callee']>0
    assert linked.code[0]==0xE8
    assert linked.code[1:5] == (linked.symbols['callee']-5).to_bytes(4,'little',signed=True)
