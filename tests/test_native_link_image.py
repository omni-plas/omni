from omni.native_link_image import link_image
from omni.native_global_data import GlobalData
from omni.native_module_linker import NativeFragment


def test_data_symbols_follow_code_image():
    image=link_image((NativeFragment('main',b'\xc3'),),(GlobalData('msg',b'hello',8),))
    assert image.symbols['main']==0
    assert image.symbols['msg']==8
    assert image.data==b'hello'
