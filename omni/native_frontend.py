"""Native, dependency-free bootstrap frontend for the Omni language.

The grammar intentionally starts small but is real source syntax rather than a
JSON transport.  It produces the same canonical UIR used by the universal
pipeline, allowing the language frontend to evolve without changing targets.
"""

from __future__ import annotations

import re
from typing import Any

from .uir import UIR, validate_uir


class OmniNativeFrontend:
    language = "omni"
    _line = re.compile(r"^\\s*(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\\s*=\\s*(?P<value>.+?)\\s*$")

    def supports(self, language: str) -> bool:
        return isinstance(language, str) and language.strip().lower() == self.language

    def parse(self, source: str, *, filename: str = "<source>") -> UIR:
        if not isinstance(source, str) or not source.strip():
            raise ValueError("Omni source cannot be empty")
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
            "semantics": {"program": {"entry": values.get("entry", "main")}},
        }
        return validate_uir(document)
