from omni.omni_compile import compile_omni_source


def test_compile_omni_source_builds_valid_ir():
    result = compile_omni_source('fn main(a, b) { let x = a + b * 2; return x; }')
    result.module.validate()
    assert result.target == 'linux-x86_64'
    assert result.module.functions[0].name == 'main'
