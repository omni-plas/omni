from omni.elf64 import build_elf64


def test_build_elf64_has_valid_header_and_code():
    blob=build_elf64(b"\xc3")
    assert blob[:4] == b"\x7fELF"
    assert blob[18:20] == (62).to_bytes(2,"little")
    assert blob[-1:] == b"\xc3"
