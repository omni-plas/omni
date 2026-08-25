# Omni

Omni is an independent, open-world digital creation, transformation, compilation, packaging, installation, execution, and maintenance engine. Its long-term goal is to let Omni itself construct digital entities and transform sufficiently defined digital inputs across languages, targets, eras, and environments without making another language compiler a fundamental dependency.

The repository implements the architecture defined by [`SPEC.md`](./SPEC.md): formal UIR, semantic analysis, lowering to executable IR, extensible source/target contracts, deterministic artifacts, a reference runtime, installation planning, and concrete materializers for supported subsets.

## Official identity

Omni's official visual identity is the three-dimensional **winged lightning-and-infinity emblem**. The lightning represents power, speed, execution, and transformation; the infinity symbol represents Omni's open-world and extensible nature; and the wings represent freedom and reach across languages, targets, environments, and eras.

The official Omni source-file extension is **`.oi`**. A `.oi` file is source code written in Omni, analogous to `.py` for Python. Omni editors, IDEs, file managers, installers, and operating-system integrations should associate `.oi` files with the Omni emblem.

Canonical branding documentation: [`docs/OMNI_BRAND_IDENTITY.md`](./docs/OMNI_BRAND_IDENTITY.md)
Canonical logo asset: [`assets/branding/omni-logo.jpg`](./assets/branding/omni-logo.jpg)

## Core model

```text
Digital Idea / Specification / Source / Partial Project / Existing Entity
                              |
                              v
                    Understand + Validate
                              |
                              v
                       UIR + Semantics
                              |
                              v
                 Complete / Transform / Compile
                              |
                              v
                         Test + Validate
                              |
                              v
                   Package / Image / Artifact
                              |
                              v
                    Installer / Deployment
                              |
                              v
                         Usable Product
```

Omni deliberately uses an **open-world** model. Languages, operating systems, CPUs, ABIs, runtimes, libraries, plugins, formats, installation mechanisms, and artifact kinds are represented through extensible identifiers and contracts rather than a closed list. Historical, existing, and future concepts can therefore be modeled and validated. Actual execution or materialization remains capability-driven: when a concrete implementation is unavailable, Omni reports the missing capability instead of fabricating success.

## Universal lifecycle

Omni is designed around one overarching capability: take a sufficiently defined digital input at any meaningful stage and perform the remaining required work to reach a usable, executable, deployable, or installable product.

```text
Idea
  -> Specification
  -> Design / Architecture
  -> Source / Components
  -> Semantic Analysis
  -> Compilation / Transformation
  -> Link / Assemble
  -> Test / Validate
  -> Package
  -> Image / Installer
  -> Install / Deploy
  -> Run / Use
  -> Update / Repair / Maintain
```

A project can enter this lifecycle at any stage. For example, existing source code can go directly into analysis and compilation, while an operating-system specification can enter before source generation.

## Current foundation

- Strict UIR validation and canonical serialization.
- Open-world digital-entity specifications and construction planning.
- Semantic requirements for types, control/data flow, memory, ownership/lifetime, concurrency, errors, I/O, dependencies, security, performance, and execution.
- Semantic IR lowering, type checking, semantic validation, and deterministic optimization.
- Reference runtime for the portable arithmetic/control-flow IR subset.
- Extensible source frontend and target backend contracts.
- Digital-entity materialization contracts and content-addressed artifact manifests.
- Target-neutral operating-system and installer planning.
- Concrete C99 emission for the currently representable portable IR subset.
- Terminal commands for validation, execution, C emission, and installation-plan generation.
- Structured source-location diagnostics for compiler/tooling consumers.
- Explicit target capability requirements for open-world targets.
- Automated tests and GitHub Actions CI.

## Hardware requirements

The fundamental Omni engine is **not an AI model and must not require a powerful GPU** for its core operation. Compilation, semantic analysis, validation, packaging, installation planning, and other core toolchain operations are intended to run primarily on ordinary CPU/RAM resources.

A GPU may be used when the **product being built** requires GPU computation, such as large AI training or heavy 3D rendering. That is a requirement of the resulting workload, not a fundamental dependency of the Omni language or core toolchain.

## CLI

```bash
python -m pip install -e .
omni validate program.json
omni run program.json --args '{"x": 41}'
omni emit-c program.json program.c
omni install-plan --target future-os --architecture future-cpu --abi future-abi --kind bootable --format future-image --bootable --filesystem future-fs
python -m pytest -q
```

Requires Python 3.11+ for the current reference implementation.

## Capability model

Target descriptions are not restricted to known operating systems or CPUs. A target may carry arbitrary capability contracts and can be extended without mutating the original descriptor. Backends can require a capability and fail deterministically when it is unavailable.

## Long-term direction

The reference implementation is intentionally honest about capability boundaries. Omni can represent a future language, operating system, installer, or target without pretending that an absent frontend, backend, runtime, ABI, or specification is already implemented. The roadmap is to progressively replace reference implementations with native Omni implementations and ultimately reach genuine self-hosting.
