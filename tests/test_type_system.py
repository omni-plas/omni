from omni.type_system import I32, I64, require_same_type

def test_matching_types():
    assert require_same_type(I32,I32)==I32

def test_mismatched_types_rejected():
    try: require_same_type(I32,I64)
    except TypeError: pass
    else: raise AssertionError('expected type mismatch')
