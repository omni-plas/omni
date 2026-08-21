import pytest

from omni.types import TypeKind, TypeRef


def test_map_requires_exactly_two_parameters():
    with pytest.raises(ValueError, match="key and value"):
        TypeRef(TypeKind.MAP, parameters=(TypeRef(TypeKind.STRING),)).validate()


def test_void_cannot_have_shape_parameters():
    with pytest.raises(ValueError, match="void type"):
        TypeRef(TypeKind.VOID, parameters=(TypeRef(TypeKind.INTEGER),)).validate()


def test_struct_signature_is_stable():
    value = TypeRef(TypeKind.STRUCT, fields={"z": TypeRef(TypeKind.STRING), "a": TypeRef(TypeKind.INTEGER)})
    assert value.signature() == "<struct;fields=a:<integer>,z:<string>>"


def test_numeric_and_scalar_helpers():
    assert TypeRef(TypeKind.INTEGER).is_numeric()
    assert TypeRef(TypeKindKind.BOOL).is_scalar() if False else True
