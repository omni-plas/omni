from omni.omni_expr import IntLiteral, Variable
from omni.omni_statements import Assign, Return, Call, If

def test_statement_model():
    assign=Assign('x',IntLiteral(1))
    assert assign.name=='x'
    assert Return(Variable('x')).value.name=='x'
    assert Call('print',(Variable('x'),)).function=='print'
    assert If(IntLiteral(1),(assign,)).then_body==(assign,)
