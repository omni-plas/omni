from omni.native_pipeline import compile_native


def test_compile_native_uses_frontend_and_backend():
    result = compile_native(
        "entity = application\\nname = hello\\nplatform = semantic-artifact\\narchitecture = universal\\nabi = universal\\n"
    )
    assert result.frontend_language == "omni"
    assert result.compilation.backend_name == "omni-portable-artifact"
    assert result.compilation.artifact.payload.startswith(b"OMNIART1")
