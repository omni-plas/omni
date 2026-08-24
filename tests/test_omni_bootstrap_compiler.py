from omni.omni_bootstrap_compiler import compile_source


def test_compile_source_links_functions():
    source='fn main() { return 0 }\nfn helper() { return 0 }'
    module=compile_source(source,lambda fn:b'\xc3')
    assert module.symbols=={'main':0,'helper':1}
