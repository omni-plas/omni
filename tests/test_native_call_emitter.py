from omni.native_call_emitter import emit_call


def test_emit_call_has_rel32_relocation():
    code,reloc=emit_call('callee')
    assert code==b'\xe8\x00\x00\x00\x00'
    assert reloc.symbol=='callee'
    assert reloc.immediate_offset==1
    assert reloc.instruction_end==5
