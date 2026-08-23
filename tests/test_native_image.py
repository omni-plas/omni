from omni.native_image import build_image
from omni.native_module_linker import NativeFragment
from omni.native_global_data import GlobalData


def test_image_places_data_after_code():
    image=build_image((NativeFragment("main",b"\xc3"),),(GlobalData("msg",b"hi",4),))
    assert image.code==b"\xc3"
    assert image.data.endswith(b"hi")
    assert image.code_symbols["main"]==0
    assert image.data_symbols["msg"]==4
