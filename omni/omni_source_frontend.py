"""Small, deterministic frontend for the core Omni bootstrap language subset."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class OmniFunction:
    name: str
    params: tuple[str, ...]
    body: tuple[str, ...]

_FUNC = re.compile(r"^fn\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*\{$")

def parse_source(source: str) -> tuple[OmniFunction, ...]:
    # Accept compact one-line function declarations as well as the canonical
    # multiline form. Split simple inline statements at semicolons, preserving
    # the existing line-oriented parser and its deterministic diagnostics.
    expanded = []
    for raw in source.splitlines():
        line = raw.strip()
        inline = _INLINE_EMPTY_OR_SIMPLE.match(line)
        if inline:
            expanded.append(inline.group(1) + " {")
            body = inline.group(2).strip()
            if body:
                expanded.extend(part.strip() for part in body.split(";") if part.strip())
            expanded.append("}")
        else:
            expanded.append(raw)
    lines = [x.strip() for x in expanded if x.strip() and not x.strip().startswith("#")]
    functions = []
    current = None
    for line in lines:
        m = _FUNC.match(line)
        if m:
            if current is not None:
                raise SyntaxError("nested function")
            params = tuple(x.strip() for x in m.group(2).split(",") if x.strip())
            current = [m.group(1), params, []]
        elif line == "}":
            if current is None:
                raise SyntaxError("unexpected }")
            functions.append(OmniFunction(current[0], current[1], tuple(current[2])))
            current = None
        elif current is not None:
            current[2].append(line)
        else:
            raise SyntaxError(f"unexpected source: {line}")
    if current is not None:
        raise SyntaxError("unterminated function")
    return tuple(functions)

parse = parse_source
