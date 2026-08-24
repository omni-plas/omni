from omni.omni_source_native import compile_source_to_native


def test_source_to_native_module():
    module=compile_source_to_native('fn main() {}\nfn run(x) {}')
    assert module.symbols=={'main':0,'run':1}
    assert module.code==b'\xc3\xc3'
