from omni.native_binary_lowering import encode_binary, lower_binary


def test_add_lowering():
    code=encode_binary(lower_binary("add",3,4,3))
    assert code


def test_mul_lowering_moves_left_operand_when_needed():
    code=encode_binary(lower_binary("mul",3,4,5))
    assert code
