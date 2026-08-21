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
    value.validate()
    assert value.signature() == "<struct;fields=a:<integer>,z:<string>>"


def test_nested_array_and_map_validate():
    value = TypeRef(TypeKind.ARRAY, parameters=(TypeRef(TypeKind.MAP, parameters=(TypeRef(TypeKind.STRING), TypeRef(TypeKind.INTEGER))),))
    value.validate()
    assert value.parameters[0].kind is TypeKind.MAP


def test_function_type_requires_return_type():
    with pytest.raises(ValueError, match="return type"):
        TypeRef(TypeKind.FUNCTION).validate()


def test_pointer_requires_pointee_type():
    with pytest.raises(ValueError, match="parameter"):
        TypeRef(TypeKind.POINTER).validate()


def test_numeric_and_scalar_helpers():
    assert TypeRef(TypeKind.INTEGER).is_numeric()
    assert TypeRef(TypeKind.FLOAT).is_numeric()
    assert not TypeRef(TypeKind.STRING).is_numeric()
    assert TypeRef(TypeKind.BOOL).is_scalar()
    assert TypeRef(TypeKind.STRING).is_scalar()
    assert not TypeRef(TypeKind.ARRAY, parameters=(TypeRef(TypeKind.INTEGER),)).is_scalar()
