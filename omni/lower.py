"""Lower validated UIR semantic declarations into executable IR."""

from __future__ import annotations

from typing import Any, Mapping

from .ir import BasicBlock, FunctionIR, ModuleIR, Operation
from .types import TypeKind, TypeRef
from .uir import UIR, UIRValidationError, validate_uir


def _type_from_spec(spec: Any) -> TypeRef:
    if isinstance(spec, str):
        canonical = "integer" if spec == "int" else spec
        try:
            return TypeRef(TypeKind(canonical))
        except ValueError:
            return TypeRef(TypeKind.STRUCT, name=spec)
    if not isinstance(spec, Mapping):
        raise UIRValidationError("type specification must be a string or object")
    kind = spec.get("kind")
    if not isinstance(kind, str):
        raise UIRValidationError("type.kind must be a string")
    kind = "integer" if kind == "int" else kind
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
        bits=spec.get("bits"),
        signed=spec.get("signed"),
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
    raw_functions = semantics.get("functions", ())
    if isinstance(raw_functions, Mapping):
        normalized_functions = []
        for function_name, function_doc in raw_functions.items():
            if not isinstance(function_doc, Mapping):
                raise UIRValidationError("semantics.functions entries must be objects")
            normalized_functions.append({"name": function_name, **dict(function_doc)})
        raw_functions = normalized_functions
    if not isinstance(raw_functions, (list, tuple)):
        raise UIRValidationError("semantics.functions must be an object or array")
    for function in raw_functions:  # extensible: additional semantic nodes may coexist
        if not isinstance(function, Mapping):
            raise UIRValidationError("semantics.functions entries must be objects")
        name = function.get("name")
        if not isinstance(name, str) or not name.strip():
            raise UIRValidationError("function.name must be a non-empty string")
        raw_parameters = function.get("parameters", {})
        if isinstance(raw_parameters, Mapping):
            parameters = {str(key): _type_from_spec(value) for key, value in raw_parameters.items()}
        elif isinstance(raw_parameters, (list, tuple)):
            parameters = {
                str(parameter.get("name")) if isinstance(parameter, Mapping) else str(parameter):
                    _type_from_spec(parameter.get("type", "integer")) if isinstance(parameter, Mapping) else TypeRef(TypeKind.INTEGER)
                for parameter in raw_parameters
            }
        else:
            raise UIRValidationError(f"function {name} parameters must be an object or array")
        result = _type_from_spec(function.get("result", "void"))
        def lower_operation(op: Mapping[str, Any]) -> Operation:
            if not isinstance(op, Mapping):
                raise UIRValidationError(f"function {name} operations must be objects")
            return Operation(
                opcode=str(op.get("opcode")),
                inputs=tuple(str(x) for x in op.get("inputs", ())),
                outputs=tuple(str(x) for x in op.get("outputs", ())),
                attributes=dict(op.get("attributes", {})),
            )

        cfg = function.get("control_flow", {})
        raw_blocks = cfg.get("blocks", ()) if isinstance(cfg, Mapping) else ()
        if not raw_blocks:
            raw_blocks = function.get("blocks", ())
        if raw_blocks:
            blocks = []
            for raw_block in raw_blocks:
                if not isinstance(raw_block, Mapping):
                    raise UIRValidationError(f"function {name} control-flow blocks must be objects")
                block_name = raw_block.get("name")
                if not isinstance(block_name, str) or not block_name.strip():
                    raise UIRValidationError(f"function {name} block name must be non-empty")
                blocks.append(BasicBlock(
                    name=block_name,
                    operations=tuple(lower_operation(op) for op in raw_block.get("operations", ())),
                    successors=tuple(str(x) for x in raw_block.get("successors", ())),
                ))
        else:
            blocks = [BasicBlock(
                name="entry",
                operations=tuple(lower_operation(op) for op in function.get("operations", ())),
                successors=(),
            )]
        functions.append(FunctionIR(name=name, parameters=parameters, result=result, blocks=tuple(blocks)))

    module = ModuleIR(name=module_name, types=declared_types, functions=tuple(functions))
    module.validate()
    return module
