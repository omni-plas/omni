from omni.omni_source_executable import compile_source_to_elf


def test_omni_source_builds_elf_image():
    blob=compile_source_to_elf('fn main() {}')
    assert blob[:4]==b'\x7fELF'


def test_missing_entry_is_rejected():
    try: compile_source_to_elf('fn run() {}')
    except ValueError as exc: assert 'entry symbol' in str(exc)
    else: raise AssertionError('missing entry must fail')
