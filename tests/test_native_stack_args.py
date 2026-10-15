from omni.native_stack_args import place_stack_arguments


def test_stack_args_are_reversed_for_call_order():
    args=place_stack_arguments((10,11))
    assert args.arguments[0].source_register == 11
    assert args.arguments[1].source_register == 10
    assert args.arguments[1].stack_offset == 8
