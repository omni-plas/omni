""""Type-aware validation at the native lowering boundary."""

from __future__ import annotations

from .type_system import Type

SUPPORTED_INTEGER_BITS = {1, 8, 16, 32, 64}


def validate_native_type(typ: Type) -> bool:
    """Return whether a type occupies a native value location.

    Primitive types are identified by canonical names such as i64 and void,
    not by a kind attribute.
    """
    name = getattr(typ, "name", None)
    if name == "void":
        return False

    bits = getattr(typ, "bits", None)
    if isinstance(name, str) and name.startswith("i") and name[1:].isdigit():
        width = int(name[1:])
        if bits is not None and bits != width:
            raise ValueError(f"inconsistent integer type width: {name} has bits={bits}")
        bits = width

    if bits is not None and bits in SUPPORTED_INTEGER_BITS and getattr(typ, "signed", None) in (True, False, None):
        return True

    raise ValueError(f"unsupported native type: {typ}")
