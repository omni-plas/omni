from omni.native_elf_layout import layout


def test_data_is_aligned_after_code():
    result=layout(13,5,3,16)
    assert result.code_offset==0
    assert result.data_offset==16
    assert result.entry_offset==3
    assert result.total_size==21
