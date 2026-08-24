from omni.omni_cfg import build_cfg
from omni.omni_expr import IntLiteral, Variable
from omni.omni_statements import If, Return
from omni.omni_loop import While


def test_if_creates_control_flow_blocks():
    blocks=build_cfg((If(IntLiteral(1),(Return(IntLiteral(1)),),(Return(IntLiteral(0)),)),))
    assert any(len(block.successors)==2 for block in blocks)
    assert any(block.name.startswith('then') for block in blocks)
    assert any(block.name.startswith('else') for block in blocks)


def test_while_creates_back_edge_and_exit():
    blocks=build_cfg((While(Variable('running'),(Return(IntLiteral(0)),)),))
    assert any(block.name.startswith('while_cond') and len(block.successors)==2 for block in blocks)
    assert any(block.name.startswith('while_exit') for block in blocks)
