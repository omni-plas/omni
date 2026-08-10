# Omni

Omni is an open-ended digital creation and semantic compilation engine. The repository implements the architecture defined by [`SPEC.md`](./SPEC.md): formal UIR, semantic analysis, lowering to executable IR, extensible source/target contracts, deterministic artifacts, a reference runtime, and a concrete C99 emitter for the currently supported portable IR subset.

## Vision

Omni treats **digital creation as an open-world problem**. A digital artifact is not limited to today's categories: applications, services, games, APIs, tools, simulations, data products, or a future kind of artifact can be represented through the same extensible construction model. Likewise, languages, platforms, architectures, ABIs, and execution models are identifiers and contracts rather than a closed enum.

The important boundary is capability, not naming: an unknown future concept can be modeled, validated, and carried through the semantic pipeline, while compilation/materialization fails explicitly when no installed implementation can actually realize its semantics. This prevents fake "universal" support while keeping the architecture extensible toward it.

## Architecture

```text
Concept / Blueprint / Source
          |
          v
       UIR + validation
          |
          v
   Digital specification
          |
          v
   Semantic model + checks
          |
          v
      Semantic IR
       /       \
      v         v
 Reference    Frontend/Backend plugins
 runtime      + concrete emitters
      |         |
      +----+----+
           v
        Artifact
```

## What is implemented

- Strict, extensible UIR validation.
- Open-world digital artifact specifications and construction planning.
- Semantic requirements for types, control/data flow, memory, ownership/lifetime, concurrency, errors, I/O, dependencies, security, performance, and execution.
- Semantic IR with validation and lowering from UIR.
- Structural type checking and diagnostics.
- Deterministic JSON serialization.
- Reference execution runtime for the portable arithmetic IR subset.
- Source frontend and target backend protocols plus an open-world plugin registry.
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

The project does not claim that a closed implementation can magically compile an arbitrary future language or execute on a future machine. Instead, Omni provides an extensible semantic contract: future languages, targets, and digital artifact kinds can be represented without changing the core schema, while installed frontends/backends are required to provide the actual implementation needed to realize them.
