from omni.type_aware_lowering import validate_native_type
from omni.type_system import I64, Void

def test_i64_is_native_lowerable():
    assert validate_native_type(I64) is True

def test_void_has_no_native_value():
    assert validate_native_type(Void) is False
