from omni.semantic import analyze
from omni.omni_source_frontend import parse


def test_semantic_analysis_rejects_duplicate_functions():
    module=parse('fn main() {}\nfn main() {}')
    try: analyze(module)
    except ValueError as exc: assert 'duplicate function' in str(exc)
    else: raise AssertionError('expected duplicate function error')


def test_semantic_analysis_accepts_unique_functions():
    module=analyze(parse('fn main(a,b) {}\nfn run(x) {}'))
    assert module.functions[0].parameters==('a','b')
