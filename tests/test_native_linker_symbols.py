from omni.native_linker_symbols import SymbolicFragment, link_symbolic_fragments
from omni.native_symbol_relocations import SymbolCallRelocation


def test_function_call_resolves_by_symbol():
    # call at offset 0 in first function; second function starts at 5.
    code=b'\xe8\x00\x00\x00\x00'
    out,symbols=link_symbolic_fragments((
        SymbolicFragment('main',code,(SymbolCallRelocation(1,5,'helper'),)),
        SymbolicFragment('helper',b'\xc3'),
    ))
    assert symbols['helper']==5
    assert int.from_bytes(out[1:5],'little',signed=True)==0
