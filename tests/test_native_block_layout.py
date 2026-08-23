from omni.native_block_layout import layout_blocks
from omni.ir import BasicBlock


def test_layout_assigns_offsets_and_labels():
    blocks=(BasicBlock("entry"),BasicBlock("exit"))
    layout=layout_blocks(blocks,(b"\x90\x90",b"\xc3"))
    assert layout.labels=={"entry":0,"exit":2}
    assert layout.spans[0].end==2
    assert layout.code==b"\x90\x90\xc3"
