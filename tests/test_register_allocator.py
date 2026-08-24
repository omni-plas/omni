from omni.register_allocator import allocate

def test_allocator_assigns_registers_then_spills():
    a=allocate(('a','b','c'),(1,2))
    assert a.registers=={'a':1,'b':2}
    assert a.spills=={'c':0}
