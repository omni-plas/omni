from omni.native_stack_args_real import push_arguments


def test_arguments_are_pushed_right_to_left():
    code=push_arguments((1,2,3))
    assert code[0:1]==b'\x68'
    assert int.from_bytes(code[1:5],'little',signed=True)==3
    assert int.from_bytes(code[6:10],'little',signed=True)==2
    assert int.from_bytes(code[11:15],'little',signed=True)==1
