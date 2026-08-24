from omni.omni_source_frontend import parse_source


def test_parse_two_functions():
    source='''
    fn main() {
      return 0
    }
    fn helper(x, y) {
      return x
    }
    '''
    functions=parse_source(source)
    assert [f.name for f in functions]==['main','helper']
    assert functions[1].params==('x','y')
