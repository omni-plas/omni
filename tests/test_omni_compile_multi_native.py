from omni.omni_compile import compile_omni_source


def test_compile_multi_function_native_program():
    result = compile_omni_source(
        "fn double(x) { return x + x; } fn main() { let x = 21; let y = double(x); return y; }",
        emit_native=True,
    )
    assert result.executable is not None
    assert result.executable.payload[:4] == b'\x7fELF'
    assert result.module.functions[0].name == "double"
    assert result.module.functions[1].name == "main"
