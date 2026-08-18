# Omni

Omni is an open-ended digital creation and semantic compilation engine. It is designed around two goals: **create any digital thing**—including kinds that do not yet exist—and **compile source programs across languages and targets**, including future language and platform identifiers, through explicit extensible capabilities.

The repository implements the architecture defined by [`SPEC.md`](./SPEC.md): formal UIR, semantic analysis, lowering to executable IR, extensible source/target contracts, deterministic artifacts, a reference runtime, and a concrete C99 emitter for the currently supported portable IR subset.

## Vision

Omni treats digital creation and compilation as open-world problems. Applications, services, games, APIs, simulations, data products, and future artifact kinds can share the same extensible construction model. Languages, platforms, architectures, ABIs, and execution models are identifiers and contracts rather than a closed enum.

An unknown future concept can therefore be modeled, validated, and carried through the semantic pipeline. Actual materialization remains capability-driven: if no installed implementation can realize a requested semantics, Omni reports that capability gap instead of fabricating a successful artifact.

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

## Implemented foundation

- Strict, extensible UIR validation.
- Open-world digital artifact specifications and construction planning.
- Semantic requirements for types, control/data flow, memory, ownership/lifetime, concurrency, errors, I/O, dependencies, security, performance, and execution.
- Semantic IR with validation and lowering from UIR.
- Structural type checking and diagnostics.
- Deterministic canonical serialization and build manifests.
- Reference execution runtime for the portable arithmetic IR subset.
- Source frontend and target backend protocols plus an open-world plugin registry.
- Formal digital-entity model and materialization contract.
- Content-addressed artifact manifests using SHA-256.
- Concrete C99 emission for the supported portable IR subset; unsupported operations fail explicitly.
- CLI execution of UIR programs.
- Automated tests and GitHub Actions CI.

## Development

Requires Python 3.11+.

```bash
python -m pip install -e .
python -m pytest -q
```

Omni does not pretend that a closed implementation can magically execute on a future machine or compile an arbitrary future language without an implementation boundary. The architecture instead makes future languages, targets, and digital artifact kinds representable while requiring concrete frontends/backends/runtime capabilities for actual realization.
