from omni.omni_compiler_pipeline import compile_source_to_ir


def test_source_to_ir_pipeline():
    ir=compile_source_to_ir('fn main(a,b) {}\nfn run(x) {}')
    assert [f.name for f in ir.functions]==['main','run']
