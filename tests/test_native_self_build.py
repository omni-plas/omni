from omni.native_self_build import self_build_target


def test_self_build_target_defaults():
    target=self_build_target()
    assert target.compiler_source=='compiler.omni'
    assert target.target_arch=='x86_64'
    assert target.bootstrap
