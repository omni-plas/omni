from omni.bootstrap_plan import BOOTSTRAP_STAGES, validate_bootstrap_stages


def test_bootstrap_has_seed_self_compile_and_recompile():
    validate_bootstrap_stages(BOOTSTRAP_STAGES)
    assert [s.name for s in BOOTSTRAP_STAGES] == ["seed", "self_compile", "recompile"]
