from omni.native_call_sequence import lower_internal_call

def test_internal_call_sequence_emits_call():
    code,frame=lower_internal_call(('a','b'), {'a':3,'b':4}, 0)
    assert b'\xe8' in code
    assert frame is None

def test_internal_call_sequence_handles_stack_arguments():
    code,frame=lower_internal_call(tuple('abcdefgh'), {c:3+i for i,c in enumerate('abcdefgh')}, 0)
    assert b'\xe8' in code
    assert frame is not None
    assert frame.stack_argument_bytes==16
