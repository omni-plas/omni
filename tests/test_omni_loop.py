from omni.omni_expr import Variable
from omni.omni_loop import While

def test_while_statement():
    loop=While(Variable('running'),())
    assert loop.condition.name=='running'
