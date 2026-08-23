from omni.native_backend_plan import build_plan, encode_reload, encode_spill
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def test_native_backend_plan_maps_allocated_values():
    integer = TypeRef(TypeKind.INTEGER)
    fn = FunctionIR("f", {}, integer, (BasicBlock("entry", (Operation("const", outputs=("x",), attributes={"value": 1}), Operation("return", ("x",)))),))
    plan = build_plan(fn, (3,))
    assert plan.locations["x"].register == 3


def test_spill_encoders_are_noops_for_register_values():
    from omni.native_backend_plan import NativeValueLocation
    loc = NativeValueLocation(register=3)
    assert encode_reload(loc, 3) == b""
    assert encode_spill(loc, 3) == b""
