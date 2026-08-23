from omni.native_global_data import GlobalData, place_data


def test_global_data_alignment_and_offsets():
    image=place_data((GlobalData("a",b"abc",1),GlobalData("b",b"xy",4)),10)
    assert image.offsets["a"]==10
    assert image.offsets["b"]==16
