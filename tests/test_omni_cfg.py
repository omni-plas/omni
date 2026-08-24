from omni.omni_cfg import build_cfg
from omni.omni_expr import IntLiteral
from omni.omni_statements import If, Return

def test_if_creates_control_flow_blocks():
    blocks=build_cfg((If(IntLiteral(1),(Return(IntLiteral(1)),),(Return(IntLiteral(0)),)),))
    assert len(blocks)==2
    assert blocks[0].successors
