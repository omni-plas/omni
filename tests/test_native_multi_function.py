from omni.native_multi_function import FunctionFragment, build_function_module


def test_two_functions_get_distinct_symbols():
    module=build_function_module((FunctionFragment('a',b'\xc3'),FunctionFragment('b',b'\xc3')))
    assert module.symbols=={'a':0,'b':1}
    assert module.code==b'\xc3\xc3'
