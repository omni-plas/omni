from omni.native_data import layout_data


def test_data_layout_assigns_offsets():
    section=layout_data((("x",b"abc"),("y",b"z")))
    assert section.symbols=={"x":0,"y":3}
    assert section.data==b"abcz"
