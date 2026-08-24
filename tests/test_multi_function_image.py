from omni.multi_function_image import assemble_functions

def test_functions_are_contiguous_and_indexed():
    image=assemble_functions((('main',b'abc'),('helper',b'de')))
    assert image.payload==b'abcde'
    assert image.functions[0].offset==0 and image.functions[1].offset==3
    assert image.functions[1].size==2
