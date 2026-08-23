from omni.native_multi_codegen import emit_multi_x86_64_elf
from omni.omni_lowering import lower_source


def test_multi_function_native_elf_with_call():
    module = lower_source('fn double(x) { return x + x; } fn main() { let x = 21; let y = double(x); return y; }')
    executable = emit_multi_x86_64_elf(module)
    assert executable.payload[:4] == b'\x7fELF'
    assert executable.format == 'elf-x86_64'
