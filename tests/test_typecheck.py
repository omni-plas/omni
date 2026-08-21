from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.typecheck import check_module, is_valid
from omni.types import TypeKind, TypeRef


I32 = TypeRef(TypeKind.INTEGER, name="i32")
I64 = TypeRef(TypeKind.INTEGER, name="i64")


def test_typecheck_rejects_undefined_values():
    module = ModuleIR("demo", {}, (FunctionIR("main", {}, I32, (BasicBlock("entry", (Operation("add", inputs=("missing",), outputs=("x",)),)),)),))
    diagnostics = check_module(module)
    assert any(d.code == "IR002" for d in diagnostics)
    assert not is_valid(module)


def test_typecheck_accepts_defined_value_flow():
    module = ModuleIR("demo", {}, (FunctionIR("main", {"input": I32}, I32, (BasicBlock("entry", (Operation("copy", inputs=("input",), outputs=("x",)),)),)),))
    assert check_module(module) == ()


def test_typecheck_rejects_redefinition():
    module = ModuleIR("demo", {}, (FunctionIR("main", {"input": I32}, I32, (BasicBlock("entry", (
        Operation("copy", inputs=("input",), outputs=("x",))), Operation("copy", inputs=("input",), outputs=("x",))),)),))
    assert any(d.code == "IR007" for d in check_module(module))


def test_typecheck_rejects_input_type_mismatch():
    module = ModuleIR("demo", {}, (FunctionIR("main", {"input": I32}, I32, (BasicBlock("entry", (
        Operation("copy", inputs=("input",), outputs=("x",), attributes={"input_types": (I64,), "output_type": I64}),
    )),),)))
    diagnostics = check_module(module)
    assert any(d.code == "IR005" and d.value == "input" for d in diagnostics)


def test_typecheck_rejects_bad_output_type_attribute():
    module = ModuleIR("demo", {}, (FunctionIR("main", {"input": I32}, I32, (BasicBlock("entry", (
        Operation("copy", inputs=("input",), outputs=("x",), attributes={"output_type": "i32"}),
    )),),)))
    assert any(d.code == "IR006" for d in check_module(module))


def test_typecheck_rejects_operation_after_return():
    module = ModuleIR("demo", {}, (FunctionIR("main", {"input": I32}, I32, (BasicBlock("entry", (
        Operation("return", inputs=("input",)), Operation("copy", inputs=("input",), outputs=("x",))),),),)))
    assert any(d.code == "IR008" for d in check_module(module))


def test_typecheck_compares_struct_fields():
    left = TypeRef(TypeKind.STRUCT, fields={"a": I32})
    right = TypeRef(TypeKind.STRUCT, fields={"a": I64})
    module = ModuleIR("demo", {}, (FunctionIR("main", {"x": left}, left, (BasicBlock("entry", (
        Operation("copy", inputs=("x",), outputs=("y",), attributes={"input_types": (right,)}),
    )),),)))
    assert any(d.code == "IR005" for d in check_module(module))
