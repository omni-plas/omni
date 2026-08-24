from omni.semantic import analyze
from omni.omni_ir import lower_semantic
from omni.omni_source_frontend import parse


def test_lower_semantic_module_to_ir():
    ir=lower_semantic(analyze(parse('fn main(a) {}')))
    assert ir.functions[0].name=='main'
    assert ir.functions[0].parameters==('a',)
