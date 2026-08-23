from omni.native_function_emitter import emit_elf64


def test_emit_elf64_contains_native_function():
    blob = emit_elf64("main", 0, ())
    assert blob[:4] == b"\x7fELF"
    assert blob.endswith(b"\xc3")
