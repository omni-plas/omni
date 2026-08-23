from omni.native_codegen_v2 import prepare, encode_instruction, NativeInstruction
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_prepare_consumes_shared_allocation():
    integer=TypeRef(TypeKind.INTEGER)
    fn=FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value":1}), Operation("return", ("x",)))),))
    prepared=prepare(fn,(3,))
    assert prepared.name == "f"
    assert prepared.stack_size == 0


def test_machine_instruction_adapter():
    assert encode_instruction(NativeInstruction("imm", (3, 42)))
    assert encode_instruction(NativeInstruction("add", (3, 4)))
