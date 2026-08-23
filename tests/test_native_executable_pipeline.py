from omni.native_executable_pipeline import build_single_function_executable


def test_single_native_function_becomes_elf():
    blob=build_single_function_executable("main",b"\xc3")
    assert blob[:4]==b"\x7fELF"
    assert blob[-1:]==b"\xc3"
