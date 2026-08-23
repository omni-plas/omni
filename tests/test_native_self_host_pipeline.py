from omni.native_self_build import self_build_target
from omni.native_self_host_pipeline import build_steps


def test_self_host_pipeline_is_repeatable():
    steps=build_steps(self_build_target())
    assert [s.name for s in steps]==['bootstrap','compile-self','verify-self','promote']
