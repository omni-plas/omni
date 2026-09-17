# Omni source compilation boundary

Omni resolves source code through three explicit layers:

```text
source text + origin
        ↓
LanguageDefinition
        ↓
registered Frontend
        ↓
validated UIR
        ↓
semantic compilation pipeline
        ↓
IR / target backend
```

`omni.source_compiler` is the public entry point for this boundary.

## Automatic resolution

When the caller provides a source origin, Omni can resolve the language from a
registered source extension. The registry has no fixed language whitelist.
Language packs register versioned definitions and frontends register executable
implementations separately.

```python
from omni.source_compiler import compile_source

result = compile_source(
    "fn main() { let answer = 40 + 2; return answer; }",
    origin="hello.oi",
)
```

The `.oi` definition and native frontend are built in. A new language can use
the same pipeline by registering a `LanguageDefinition` and a frontend that
implements `lower(SourceUnit) -> UIR`.

## Important boundary

A declarative language pack is **not** treated as an executable compiler. Its
syntax, semantic, type, execution, memory, ABI, and dependency fields describe
the authoritative language contract. An executable frontend must still exist
for source text to be lowered into UIR.

This separation prevents a language definition from silently becoming a fake
compiler and keeps the architecture open for future language implementations.
