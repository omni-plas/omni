from omni.ir import Operation
from omni.constant_folding import fold_constants

def test_folds_addition():
    ops=fold_constants((Operation('const',outputs=('a',),attributes={'value':2}),Operation('const',outputs=('b',),attributes={'value':3}),Operation('add',inputs=('a','b'),outputs=('c',))))
    assert ops[-1].opcode=='const'
    assert ops[-1].attributes['value']==5
