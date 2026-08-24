from dataclasses import dataclass
from omni.native_symbol_table import build_symbol_table

@dataclass
class F:
    name:str
    code:bytes

def test_symbol_offsets_are_deterministic():
    table=build_symbol_table((F('a',b'123'),F('b',b'45')))
    assert table['a'].offset==0
    assert table['b'].offset==3
