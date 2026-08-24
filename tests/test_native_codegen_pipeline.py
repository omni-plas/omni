from omni.ir import Operation
from omni.native_codegen_pipeline import emit_function

def test_simple_function_codegen():
    ops=(Operation('const',outputs=('a',),attributes={'value':2}),Operation('const',outputs=('b',),attributes={'value':3}),Operation('add',inputs=('a','b'),outputs=('a',)),Operation('return',inputs=('a',)))
    code=emit_function(ops)
    assert code.startswith(b'\x55\x48\x89\xe5')
    assert code.endswith(b'\x5d\xc3')
