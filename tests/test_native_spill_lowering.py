from omni.native_spill_lowering import encode_spill_action, lower_reload, lower_spill


def test_spill_and_reload_actions_encode():
    assert encode_spill_action(lower_spill(-8, 3))
    assert encode_spill_action(lower_reload(-8, 3))
