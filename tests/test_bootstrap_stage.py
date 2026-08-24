from omni.bootstrap_stage import next_stage


def test_next_bootstrap_stage_is_native_lowering():
    assert next_stage()=='ir-to-native'
