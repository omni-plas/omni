from omni.omni_compile import compile_omni_source


def test_textual_omni_can_emit_native_elf():
    result = compile_omni_source('fn main() { return 42; }', emit_native=True)
    assert result.executable is not None
    assert result.executable.payload[:4] == b'\x7fELF'
    assert result.executable.format == 'elf-x86_64'
