from omni.native_reachable_module import compile_reachable
from omni.ir import FunctionIR

def test_dead_function_is_excluded():
    main=FunctionIR('main'); foo=FunctionIR('foo'); dead=FunctionIR('dead')
    module=compile_reachable((main,foo,dead),(('main','foo'),),'main')
    assert set(module.symbols)=={'main','foo'}
