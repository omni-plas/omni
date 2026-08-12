from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.manifest import manifest_for
from omni.targets import TargetDescriptor
from omni.types import TypeKind, TypeRef


def module():
    i64 = TypeRef(TypeKind.INTEGER, bits=64)
    return ModuleIR(
        name="demo",
        types={},
        functions=(FunctionIR(
            name="main",
            parameters={},
            result=i64,
            blocks=(BasicBlock(name="entry", operations=(
                Operation("const", outputs=("x",), output_types=(i64,), attributes={"value": 7}),
                Operation("return", inputs=("x",), input_types=(i64,)),
            )),),
        ),),
    )


def test_manifest_is_reproducible():
    target = TargetDescriptor("portable-c", "x86_64")
    first = manifest_for(module(), target)
    second = manifest_for(module(), target)
    assert first.ir_sha256 == second.ir_sha256
    assert len(first.ir_sha256) == 64
