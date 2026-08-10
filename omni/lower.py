"""Lower validated UIR semantic declarations into executable IR."""

from __future__ import annotations

from typing import Any, Mapping

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir


def _type_from_spec(spec: Any) -> TypeRef:
    if isinstance(spec, str):
        try:
            return TypeRef(TypeKind(spec))
        except ValueError:
            return TypeRef(TypeKind.STRUCT, name=spec)
    if not isinstance(spec, Mapping):
        raise UIRValidationError("type specification must be a string or object")
    kind = spec.get("kind")
    if not isinstance(kind, str):
        raise UIRValidationError("type.kind must be a string")
    try:
        type_kind = TypeKind(kind)
    except ValueError as exc:
        raise UIRValidationError(f"unknown built-in type kind: {kind}") from exc
    parameters = tuple(_type_from_spec(item) for item in spec.get("parameters", ()))
    fields = {
        str(name): _type_from_spec(value)
        for name, value in dict(spec.get("fields", {})).items()
    }
    result = TypeRef(
        kind=type_kind,
        name=spec.get("name"),
        parameters=parameters,
        fields=fields,
        nullable=bool(spec.get("nullable", False)),
        metadata=dict(spec.get("metadata", {})),
    )
    result.validate()
    return result


def lower_to_ir(document: Mapping[str, Any] | UIR) -> ModuleIR:
    """Lower the supported semantic subset into validated ModuleIR."""
    uir = document if isinstance(document, UIR) else validate_uir(document)
    semantics = uir.semantics
    module_name = str(uir.entity.get("name") or uir.entity["kind"])

    declared_types = {
        str(name): _type_from_spec(spec)
        for name, spec in dict(semantics.get("types", {})).items()
    }
    functions: list[FunctionIR] = []
    for function in semantics.get("functions", ()):  # extensible: additional semantic nodes may coexist
        if not isinstance(function, Mapping):
            raise UIRValidationError("semantics.functions entries must be objects")
        name = function.get("name")
        if not isinstance(name, str) or not name.strip():
            raise UIRValidationError("function.name must be a non-empty string")
        parameters = {
            str(key): _type_from_spec(value)
            for key, value in dict(function.get("parameters", {})).items()
        }
        result = _type_from_spec(function.get("result", "void"))
        operations = tuple(
            Operation(
                opcode=str(op.get("opcode")),
                inputs=tuple(str(x) for x in op.get("inputs", ())),
                outputs=tuple(str(x) for x in op.get("outputs", ())),
                attributes=dict(op.get("attributes", {})),
            )
            for op in function.get("operations", ())
        )
        block = BasicBlock(
            name="entry",
            operations=operations,
            successors=(),
        )
        functions.append(FunctionIR(name=name, parameters=parameters, result=result, blocks=(block,)))

    module = ModuleIR(name=module_name, types=declared_types, functions=tuple(functions))
    module.validate()
    return module
