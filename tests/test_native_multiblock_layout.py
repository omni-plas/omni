from omni.native_multiblock_layout import layout_blocks

def test_blocks_are_placed_contiguously():
    p,total=layout_blocks((('entry',b'abc'),('exit',b'de')))
    assert p[0].offset==0 and p[0].size==3
    assert p[1].offset==3 and p[1].size==2
    assert total==5
