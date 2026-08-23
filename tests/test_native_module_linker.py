from omni.native_module_linker import NativeFragment, link_fragments


def test_link_fragments_assigns_symbols_and_concatenates_code():
    linked=link_fragments((NativeFragment("a",b"\x90"),NativeFragment("b",b"\xc3")))
    assert linked.symbols=={"a":0,"b":1}
    assert linked.code==b"\x90\xc3"
