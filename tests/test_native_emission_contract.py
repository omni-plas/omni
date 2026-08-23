from omni.native_emission_contract import NATIVE_EMISSION_STAGES, validate_emission_pipeline


def test_native_pipeline_order():
    validate_emission_pipeline(NATIVE_EMISSION_STAGES)
    assert [s.name for s in NATIVE_EMISSION_STAGES] == ["allocation", "frame", "lowering", "encoding", "relocations", "executable"]
