from omni.native_runtime_builder import build_exit_program


def test_build_exit_program():
    blob=build_exit_program(0)
    assert blob[:4]==b'\x7fELF'
    assert blob.endswith(b'\x0f\x05')
