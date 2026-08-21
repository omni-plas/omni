# Omni

Omni is an independent, open-world digital creation and semantic compilation engine. Its long-term goal is to let Omni itself construct digital entities and compile source programs across languages, targets, and future-defined contracts without making another language compiler a fundamental dependency.

The repository implements the architecture defined by [`SPEC.md`](./SPEC.md): formal UIR, semantic analysis, lowering to executable IR, extensible source/target contracts, deterministic artifacts, a reference runtime, and concrete materializers for supported subsets.

## Core model

```text
Digital Entity / Source / Blueprint
                |
                v
          UIR + validation
                |
                v
       Semantic requirements
                |
                v
          Semantic IR
          /          \
         v            v
   Reference       Backends /
    runtime        materializers
         \            /
          +----------+
                |
                v
             Artifact
```

Omni deliberately uses an **open-world** model. Languages, operating systems, CPUs, ABIs, runtimes, libraries, plugins, formats, and artifact kinds are represented through extensible identifiers and contracts rather than a closed list. A future concept can therefore be modeled and validated today. Actual execution or materialization remains capability-driven: when a concrete implementation is unavailable, Omni reports the missing capability instead of fabricating success.

## Current foundation

- Strict UIR validation and canonical serialization.
- Open-world digital-entity specifications and construction planning.
- Semantic requirements for types, control/data flow, memory, ownership/lifetime, concurrency, errors, I/O, dependencies, security, performance, and execution.
- Semantic IR lowering, type checking, semantic validation, and deterministic optimization.
- Reference runtime for the portable arithmetic/control-flow IR subset.
- Extensible source frontend and target backend contracts.
- Digital-entity materialization contracts and content-addressed artifact manifests.
- Concrete C99 emission for the currently representable portable IR subset.
- Terminal commands for validation, execution, and C emission.
- Automated tests and GitHub Actions CI.

## CLI

```bash
python -m pip install -e .
omni validate program.json
omni run program.json --args '{"x": 41}'
omni emit-c program.json program.c
python -m pytest -q
```

Requires Python 3.11+.

## Long-term direction

The reference implementation is intentionally honest about capability boundaries. Omni can represent a future language or target without pretending that an absent frontend, backend, runtime, ABI, or specification is already implemented. The roadmap is to progressively replace reference implementations with native Omni implementations and ultimately reach genuine self-hosting.
