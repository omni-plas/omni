from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.typecheck import check_module, is_valid
from omni.types import TypeRef


def test_typecheck_rejects_undefined_values():
    module = ModuleIR(
        name="demo",
        types={},
        functions=(FunctionIR(
            name="main",
            parameters={},
            result=TypeRef("i32"),
            blocks=(BasicBlock("entry", (Operation("add", inputs=("missing",), outputs=("x",)),)),),
        ),),
    )
    diagnostics = check_module(module)
    assert any(d.code == "IR002" for d in diagnostics)
    assert not is_valid(module)


def test_typecheck_accepts_defined_value_flow():
    module = ModuleIR(
        name="demo",
        types={},
        functions=(FunctionIR(
            name="main",
            parameters={"input": TypeRef("i32")},
            result=TypeRef("i32"),
            blocks=(BasicBlock("entry", (Operation("copy", inputs=("input",), outputs=("x",)),)),),
        ),),
    )
    assert check_module(module) == ()
    assert is_valid(module)
