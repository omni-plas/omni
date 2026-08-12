from omni.ir import BasicBlock, FunctionIR, ModuleIR, Operation
from omni.optimize import optimize_module
from omni.types import TypeKind, TypeRef


def test_optimizer_removes_unreachable_blocks_and_identity_ops():
    i32 = TypeRef(TypeKind.INTEGER, bits=32)
    module = ModuleIR(
        name="m",
        types={},
        functions=(
            FunctionIR(
                name="main",
                parameters={},
                result=i32,
                blocks=(
                    BasicBlock(
                        name="entry",
                        operations=(
                            Operation("identity", inputs=("x",), outputs=("y",)),
                            Operation("return", inputs=("y",)),
                        ),
                        successors=(),
                    ),
                    BasicBlock(
                        name="dead",
                        operations=(Operation("return", inputs=("x",)),),
                        successors=(),
                    ),
                ),
            ),
        ),
    )
    optimized = optimize_module(module)
    blocks = optimized.functions[0].blocks
    assert [block.name for block in blocks] == ["entry"]
    assert blocks[0].operations[0].opcode == "return"
    assert blocks[0].operations[0].inputs == ("x",)
