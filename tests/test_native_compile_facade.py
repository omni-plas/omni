from omni.native_compile_facade import compile_module

def test_compile_facade_returns_elf(executable_module):
    result=compile_module(executable_module)
    assert result.format=='elf-x86_64'
    assert result.payload[:4]==b'\x7fELF'
