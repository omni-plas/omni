from omni.native_module_linker import NativeFragment, link_fragments
from dataclasses import dataclass

@dataclass(frozen=True)
class R:
    kind:str
    immediate_offset:int
    symbol:str
    addend:int=0
    instruction_end:int|None=None


def test_link_fragments_assigns_symbols_and_concatenates_code():
    linked=link_fragments((NativeFragment("a",b"\x90"),NativeFragment("b",b"\xc3")))
    assert linked.symbols=={"a":0,"b":1}
    assert linked.code==b"\x90\xc3"


def test_symbol_call_relocation_resolves_against_function_symbol():
    linked=link_fragments((NativeFragment("caller",b"\xe8\x00\x00\x00\x00",symbol_relocations=(R("call_rel32",1,"callee",instruction_end=5),)),NativeFragment("callee",b"\xc3")))
    assert int.from_bytes(linked.code[1:5],'little',signed=True)==0


def test_symbol_abs64_relocation_resolves():
    linked=link_fragments((NativeFragment("main",b"\x00"*8,symbol_relocations=(R("abs64",0,"data"),)),NativeFragment("data",b"abc")))
    assert int.from_bytes(linked.code[:8],'little')==8
