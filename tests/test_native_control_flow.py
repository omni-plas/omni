from omni.native_control_flow import encode_branch, lower_branch


def test_eq_branch_lowering():
    code=encode_branch(lower_branch("eq",3,4,2,-2))
    assert code


def test_ne_branch_lowering():
    code=encode_branch(lower_branch("ne",3,4,2))
    assert code
