from omni.native_linked_elf import build_image_elf
from omni.native_global_data import GlobalData
from omni.native_module_linker import NativeFragment


def test_linked_image_becomes_elf():
    blob=build_image_elf((NativeFragment('main',b'\xc3'),),(GlobalData('msg',b'hello',1),))
    assert blob[:4]==b'\x7fELF'
    assert blob.endswith(b'hello')
