from omni.ir import Operation
from omni.ssa import rename_ssa

def test_ssa_versions_outputs():
    ops=rename_ssa((Operation('const',outputs=('x',),attributes={'value':1}),Operation('const',outputs=('x',),attributes={'value':2})))
    assert ops[0].outputs==('x.1',)
    assert ops[1].outputs==('x.2',)
