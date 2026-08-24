from omni.ir import Operation
from omni.optimization_pipeline import optimize

def test_optimization_pipeline_folds_and_versions():
    ops=optimize((Operation('const',outputs=('a',),attributes={'value':2}),Operation('const',outputs=('b',),attributes={'value':3}),Operation('add',inputs=('a','b'),outputs=('c',))))
    assert ops[-1].opcode=='const'
    assert ops[-1].outputs==('c.1',)
