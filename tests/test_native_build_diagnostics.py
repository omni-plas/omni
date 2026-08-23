from omni.native_build_diagnostics import Diagnostic, error, warning


def test_diagnostics_are_structured():
    assert error('link','E_SYMBOL','missing').severity=='error'
    assert warning('opt','W_UNUSED','unused').severity=='warning'
    assert Diagnostic('parse','E_PARSE','bad').code=='E_PARSE'
