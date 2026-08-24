from omni.native_codegen_multi import place_functions, rel32

def test_functions_are_contiguous():
    p=place_functions((('a',b'123'),('b',b'45')))
    assert p[0].offset==0 and p[0].size==3
    assert p[1].offset==3 and p[1].size==2

def test_rel32_is_relative_to_next_instruction():
    assert rel32(100,200)==95
