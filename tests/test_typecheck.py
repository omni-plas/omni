from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.typecheck import check_module, is_valid
from omni.types import TypeKind, TypeRef


I32 = TypeRef(TypeKind.INTEGER, name="i32")
I64 = TypeRef(TypeKind.INTEGER, name="i64")


def _module(operations, *, parameters=None, result=I32):
    """Build a well-formed module around the operations under test."""
    function = FunctionIR(
        "main",
        parameters if parameters is not None else {"input": I32},
        result,
        (BasicBlock("entry", tuple(operations)),),
    )
    return ModuleIR("demo", {}, (function,))


def test_typecheck_rejects_undefined_values():
    diagnostics = check_module(_module((Operation("add", inputs=("missing",), outputs=("x",)),)))
    assert any(d.code == "IR002" for d in diagnostics)
    assert not is_valid(_module((Operation("add", inputs=("missing",), outputs=("x",)),)))


def test_typecheck_accepts_defined_value_flow():
    module = _module((Operation("copy", inputs=("input",), outputs=("x",), attributes={"output_type": I32}),))
    assert check_module(module) == ()


def test_typecheck_rejects_redefinition():
    module = _module((
        Operation("copy", inputs=("input",), outputs=("x",), attributes={"output_type": I32}),
        Operation("copy", inputs=("input",), outputs=("x",), attributes={"output_type": I32}),
    ))
    assert any(d.code == "IR007" for d in check_module(module))


def test_typecheck_rejects_input_type_mismatch():
    module = _module((Operation(
        "copy", inputs=("input",), outputs=("x",),
        attributes={"input_types": (I64,), "output_type": I64},
    ),))
    diagnostics = check_module(module)
    assert any(d.code == "IR005" and d.value == "input" for d in diagnostics)


def test_typecheck_rejects_bad_output_type_attribute():
    module = _module((Operation(
        "copy", inputs=("input",), outputs=("x",), attributes={"output_type": "i32"},
    ),))
    assert any(d.code == "IR006" for d in check_module(module))


def test_typecheck_rejects_operation_after_return():
    module = _module((
        Operation("return", inputs=("input",)),
        Operation("copy", inputs=("input",), outputs=("x",), attributes={"output_type": I32}),
    ))
    assert any(d.code == "IR008" for d in check_module(module))


def test_typecheck_compares_struct_fields():
    left = TypeRef(TypeKind.STRUCT, fields={"a": I32})
    right = TypeRef(TypeKind.STRUCT, fields={"a": I64})
    module = _module(
        (Operation("copy", inputs=("x",), outputs=("y",), attributes={"input_types": (right,)}),),
        parameters={"x": left}, result=left,
    )
    assert any(d.code == "IR005" for d in check_module(module))
