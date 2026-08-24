from omni.omni_calls import lower_call_arguments

def test_call_arguments_map_to_abi_registers():
    args,stack=lower_call_arguments(('a','b','c'))
    assert [x[1] for x in args]==[7,6,2]
    assert stack==0
