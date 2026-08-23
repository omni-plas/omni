from omni.native_function_module import compile_functions
from omni.ir import FunctionIR


def test_function_module_compiles_functions():
    a=FunctionIR('a')
    b=FunctionIR('b')
    linked=compile_functions((a,b))
    assert set(linked.symbols)=={'a','b'}
