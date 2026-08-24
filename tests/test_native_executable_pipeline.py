from omni.native_executable_pipeline import build_single_function_executable, build_linked_executable
from omni.native_module_linker import NativeFragment


def test_single_native_function_becomes_elf():
    blob=build_single_function_executable("main",b"\xc3")
    assert blob[:4]==b"\x7fELF"
    assert blob[-1:]==b"\xc3"


def test_multi_function_executable_uses_named_entry():
    image=build_linked_executable((NativeFragment('helper',b'\xc3'),NativeFragment('main',b'\xc3')),'main')
    assert image.data[:4]==b"\x7fELF"
    assert image.entry_offset==1
