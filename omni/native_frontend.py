"""Native, dependency-free bootstrap frontend for the Omni language.

The frontend accepts both the original declarative bootstrap form and the
canonical ``.oi`` programming syntax. Both forms produce the same validated
UIR, so source-file identity does not force callers onto a second frontend.
"""

from __future__ import annotations

import re
from typing import Any

from .frontends import SourceUnit
from .frontends import SourceUnit
from .omni_lowering import lower_source
from .uir import UIR, validate_uir


class OmniNativeFrontend:
    language = "omni"
    _line = re.compile(r"^\s*(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*=\s*(?P<value>.+?)\s*$")

    def supports(self, language: str) -> bool:
        return isinstance(language, str) and language.strip().lower() == self.language

    def lower(self, source: SourceUnit) -> UIR:
        """Lower a registry SourceUnit into validated semantic UIR."""
        if not isinstance(source, SourceUnit):
            raise TypeError("source must be a SourceUnit")
        if not self.supports(source.language):
            raise ValueError(f"frontend {self.language} cannot lower language {source.language!r}")
        return self.parse(source.text, filename=source.origin or "<source>")

    @staticmethod
    def _operation_document(operation) -> dict[str, Any]:
        return {
            "opcode": operation.opcode,
            "inputs": list(operation.inputs),
            "outputs": list(operation.outputs),
            "attributes": dict(operation.attributes),
        }

    def _parse_program(self, source: str, *, filename: str) -> UIR:
        module = lower_source(source, module_name=filename, strict_calls=False)
        functions: list[dict[str, Any]] = []
        for function in module.functions:
            blocks = [
                {
                    "name": block.name,
                    "operations": [self._operation_document(op) for op in block.operations],
                    "successors": list(block.successors),
                }
                for block in function.blocks
            ]
            functions.append(
                {
                    "name": function.name,
                    "parameters": {name: value.signature() for name, value in function.parameters.items()},
                    "result": function.result.signature(),
                    "operations": [self._operation_document(op) for block in function.blocks for op in block.operations],
                    "control_flow": {"blocks": blocks},
                }
            )
        document: dict[str, Any] = {
            "version": "0.1",
            "entity": {"kind": "program", "name": filename},
            "source": {"language": "omni", "version": "1", "extension": ".oi"},
            "target": {
                "platform": "semantic-artifact",
                "architecture": None,
                "abi": None,
                "capabilities": {"omni-native-source": True},
            },
            "semantics": {
                "program": {"entry": "main"},
                "types": {},
                "functions": functions,
                "control_flow": {},
                "data_flow": {},
                "memory_model": {},
                "error_handling": {},
                "io": {},
                "dependencies": [],
                "security": {},
                "performance": {},
            },
        }
        return validate_uir(document)

    def lower(self, source: SourceUnit) -> UIR:
        """Lower a registered Omni source unit through the canonical parser."""
        if not isinstance(source, SourceUnit):
            raise TypeError("source must be a SourceUnit")
        if source.language.strip().casefold() != self.language:
            raise ValueError(f"unsupported source language: {source.language}")
        return self.parse(source.text, filename=source.origin or "<source>")

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        if not isinstance(source, str) or not source.strip():
            raise ValueError("Omni source cannot be empty")
        # Canonical .oi programming syntax starts with a function declaration.
        # Keep the key=value bootstrap syntax for compatibility with existing
        # manifests and tests.
        if re.search(r"(?:^|\n)\s*fn\s+[A-Za-z_]", source):
            return self._parse_program(source, filename=filename)

        values: dict[str, str] = {}
        for number, raw in enumerate(source.splitlines(), 1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            match = self._line.match(line)
            if not match:
                raise ValueError(f"{filename}:{number}: expected key = value")
            key, value = match.group("key"), match.group("value")
            if key in values:
                raise ValueError(f"{filename}:{number}: duplicate field {key!r}")
            values[key] = value.strip().strip('"').strip("'")

        required = ("entity", "name", "platform", "architecture", "abi")
        missing = [key for key in required if key not in values]
        if missing:
            raise ValueError(f"{filename}: missing required fields: {', '.join(missing)}")

        document: dict[str, Any] = {
            "version": values.get("version", "1"),
            "entity": {"kind": values["entity"], "name": values["name"]},
            "source": {"language": "omni", "version": values.get("language_version", "1")},
            "target": {
                "platform": values["platform"],
                "architecture": values["architecture"],
                "abi": values["abi"],
                "capabilities": {},
            },
            "semantics": {
                "program": {"entry": values.get("entry", "main")},
                "types": {},
                "control_flow": {},
                "data_flow": {},
                "memory_model": {},
                "error_handling": {},
                "io": {},
                "dependencies": [],
                "security": {},
                "performance": {},
            },
        }
        return validate_uir(document)
