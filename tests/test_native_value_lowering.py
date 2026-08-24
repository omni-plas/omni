from omni.native_value_lowering import lower_value_ops
from omni.ir import Operation

def test_native_arithmetic_lowering():
    ops=(Operation('const',outputs=('a',),attributes={'value':2}),Operation('const',outputs=('b',),attributes={'value':3}),Operation('add',inputs=('a','b'),outputs=('a',)),Operation('return',inputs=('a',)))
    code=lower_value_ops(ops,{'a':3,'b':4})
    assert code.endswith(b'\xc3')
