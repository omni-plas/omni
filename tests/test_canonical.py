from omni.canonical import canonical_ir_bytes
from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.types import TypeKind, TypeRef


def make_module():
    i32 = TypeRef(TypeKind.INTEGER, bits=32)
    return ModuleIR(
        name="canonical",
        types={},
        functions=(FunctionIR(
            name="main",
            parameters={},
            result=i32,
            blocks=(BasicBlock(name="entry", operations=(
                Operation("const", outputs=("x",), output_types=(i32,), attributes={"value": 1}),
                Operation("return", inputs=("x",), input_types=(i32,)),
            )),),
        ),),
    )


def test_canonical_ir_is_stable():
    assert canonical_ir_bytes(make_module()) == canonical_ir_bytes(make_module())
