from omni.native_reachable_module import compile_reachable
from omni.ir import BasicBlock, FunctionIR, Operation
from omni.types import TypeKind, TypeRef


def _function(name):
    return FunctionIR(name, {}, TypeRef(TypeKind.VOID), (BasicBlock("entry", (Operation("return"),)),))


def test_dead_function_is_excluded():
    main, foo, dead = _function("main"), _function("foo"), _function("dead")
    module = compile_reachable((main, foo, dead), (("main", "foo"),), "main")
    assert set(module.symbols) == {"main", "foo"}
