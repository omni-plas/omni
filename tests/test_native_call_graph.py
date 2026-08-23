from omni.native_call_graph import build_call_graph, reachable

def test_reachable_functions():
    graph=build_call_graph(('main','foo','dead'),(('main','foo'),))
    assert reachable(graph,'main')==('main','foo')
