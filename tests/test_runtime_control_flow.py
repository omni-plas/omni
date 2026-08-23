from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.omni_runtime import execute_function
from omni.types import TypeKind, TypeRef


def test_runtime_branch_selects_true_path():
    fn = FunctionIR(
        "main", {"x": TypeRef(TypeKind.INTEGER)}, TypeRef(TypeKind.INTEGER),
        (
            BasicBlock("entry", (Operation("const", outputs=("one",), attributes={"value": 1}), Operation("compare", inputs=("x", "one"), outputs=("c",), attributes={"operator": "gt"}), Operation("branch", inputs=("c",), attributes={"true": "yes", "false": "no"})), ("yes", "no")),
            BasicBlock("yes", (Operation("const", outputs=("r",), attributes={"value": 42}), Operation("return", inputs=("r",))), ()),
            BasicBlock("no", (Operation("const", outputs=("r",), attributes={"value": 7}), Operation("return", inputs=("r",))), ()),
        ),
    )
    assert execute_function(ModuleIR("m", {}, (fn,)), "main", (3,)) == 42
    assert execute_function(ModuleIR("m", {}, (fn,)), "main", (0,)) == 7
