""""Type-aware validation at the native lowering boundary."""

from __future__ import annotations

from .type_system import Type

SUPPORTED_INTEGER_BITS = {1, 8, 16, 32, 64}


def validate_native_type(typ: Type) -> bool:
    """Return whether a supported integer type occupies a native value location."""
    name = getattr(typ, "name", None)
    if name == "void":
        return False

    bits = getattr(typ, "bits", None)
    if isinstance(name, str) and name.startswith("i") and name[1:].isdigit():
        width = int(name[1:])
        if bits is not None and bits != width:
            raise ValueError(f"inconsistent integer type width: {name} has bits={bits}")
        if width in SUPPORTED_INTEGER_BITS:
            return True
        raise ValueError(f"unsupported integer width: {width}")

    raise ValueError(f"unsupported native type: {typ}")
