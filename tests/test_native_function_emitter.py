from omni.native_function_emitter import emit_function
from omni.native_binary_lowering import lower_binary


def test_emit_function_has_frame_and_body():
    emitted=emit_function("f",16,(lower_binary("add",3,4,3),))
    assert emitted.code
    assert emitted.code.endswith(b"\xc3")
