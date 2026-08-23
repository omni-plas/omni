from omni.native_image_symbols import resolve_symbols


def test_code_and_data_share_image_address_space():
    symbols=resolve_symbols({'main':0},{'message':4},100)
    assert symbols['main'].offset==0
    assert symbols['main'].section=='code'
    assert symbols['message'].offset==104
    assert symbols['message'].section=='data'
