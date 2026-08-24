from omni.native_call_sequence import lower_internal_call

def test_internal_call_sequence_emits_call():
    code=lower_internal_call(('a','b'), {'a':3,'b':4}, 0)
    assert b'\xe8' in code
