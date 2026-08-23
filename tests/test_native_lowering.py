from omni.native_lowering import ValueLocation, lower_move


def test_register_to_register_lowering():
    code = lower_move(ValueLocation(register=3), ValueLocation(register=4))
    assert code[0].opcode == "mov_rr"


def test_spill_and_reload_lowering():
    reload_code = lower_move(ValueLocation(stack_offset=8), ValueLocation(register=4))
    spill_code = lower_move(ValueLocation(register=4), ValueLocation(stack_offset=8))
    assert reload_code[0].opcode == "reload"
    assert spill_code[0].opcode == "spill"
