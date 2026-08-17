import omni


def test_public_api_exposes_core_pipeline():
    assert callable(omni.compile_semantics)
    assert callable(omni.validate_uir)
    assert callable(omni.lower_to_ir)
    assert callable(omni.optimize_module)
    assert callable(omni.resolve_target)
    assert omni.ValidationError.__mro__[1] is omni.OmniError
