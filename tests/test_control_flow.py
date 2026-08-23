import pytest

from omni.control_flow import ControlFlowError, analyze_control_flow
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def fn(*blocks):
    return FunctionIR("main", {}, TypeRef(TypeKind.INTEGER), tuple(blocks))


def test_control_flow_builds_predecessors():
    graph = analyze_control_flow(
        fn(
            BasicBlock("entry", (Operation("branch"),), ("body",)),
            BasicBlock("body", (Operation("return", inputs=("x",)),), ()),
        )
    )
    assert graph.entry == "entry"
    assert graph.predecessors["body"] == ("entry",)
    assert graph.reachable == ("entry", "body")


def test_return_block_cannot_have_successors():
    with pytest.raises(ControlFlowError, match="return block"):
        analyze_control_flow(fn(BasicBlock("entry", (Operation("return", inputs=("x",)),), ("exit",))))


def test_unreachable_block_is_rejected():
    with pytest.raises(ControlFlowError, match="unreachable blocks"):
        analyze_control_flow(
            fn(
                BasicBlock("entry", (Operation("return", inputs=("x",)),), ()),
                BasicBlock("dead", (Operation("return", inputs=("x",)),), ()),
            )
        )
