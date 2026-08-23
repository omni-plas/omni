from omni.native_link_diagnostics import duplicate_symbol, unresolved_symbol


def test_link_diagnostics():
    assert unresolved_symbol('x').severity=='error'
    assert duplicate_symbol('x').symbol=='x'
