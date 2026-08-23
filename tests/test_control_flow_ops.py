from omni.control_flow_ops import branch, compare, jump


def test_compare_operation():
    op = compare("lt", "a", "b", "%c")
    assert op.opcode == "compare"
    assert op.inputs == ("a", "b")
    assert op.outputs == ("%c",)


def test_branch_and_jump_operations():
    br = branch("%c", "then", "else")
    jmp = jump("exit")
    assert br.attributes["true"] == "then"
    assert br.attributes["false"] == "else"
    assert jmp.attributes["target"] == "exit"
