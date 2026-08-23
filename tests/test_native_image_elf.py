from omni.native_image import build_image
from omni.native_image_elf import image_to_elf
from omni.native_module_linker import NativeFragment
from omni.native_global_data import GlobalData


def test_image_to_elf():
    image=build_image((NativeFragment("main",b"\xc3"),),(GlobalData("x",b"x"),))
    blob=image_to_elf(image)
    assert blob[:4]==b"\x7fELF"
    assert blob[-2:]==b"\xc3x"
