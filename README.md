# Omni

Omni is an open-ended digital creation and semantic compilation engine. The repository implements the architecture defined by [`SPEC.md`](./SPEC.md): formal UIR, semantic analysis, lowering to executable IR, extensible source/target contracts, deterministic artifacts, a reference runtime, and a concrete C99 emitter for the currently supported portable IR subset.

## Architecture

```text
Concept / Blueprint / Source
          |
          v
       UIR + validation
          |
          v
   Semantic model + checks
          |
          v
      Semantic IR
       /       \
      v         v
 Reference    Emitters
 runtime      (C99 + plugins)
      |         |
      +----+----+
           v
        Artifact
```

The architecture intentionally uses open-world identifiers for languages, platforms, architectures, execution models, and digital entity kinds. New definitions can be represented without modifying the UIR schema.

## What is implemented

- Strict, extensible UIR validation.
- Semantic requirements for types, control/data flow, memory, ownership/lifetime, concurrency, errors, I/O, dependencies, security, performance, and execution.
- Semantic IR with validation and lowering from UIR.
- Deterministic JSON serialization.
- Reference execution runtime for the portable arithmetic IR subset.
- Source frontend and target backend protocols plus registries.
- Formal digital-entity model and materialization contract.
- Content-addressed artifact manifests using SHA-256.
- Concrete C99 emission for the supported portable IR subset; unsupported operations fail explicitly rather than producing fake output.
- CLI execution of UIR programs.
- Automated tests and GitHub Actions.

## Development

Requires Python 3.11+.

```bash
python -m pip install -e .
python -m pytest -q
```

The project treats unsupported language/target semantics as an explicit capability boundary. It does not claim that a closed implementation can magically compile an arbitrary future language or execute on a future machine; instead, it provides an extensible semantic contract and rejects requests that an installed frontend/backend cannot represent.
