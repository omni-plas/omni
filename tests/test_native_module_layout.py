from omni.native_module_layout import layout_functions

def test_function_layout_is_contiguous():
    p,total=layout_functions((('main',b'ab'),('helper',b'cde')))
    assert p[0].offset==0 and p[1].offset==2
    assert total==5
