# Omni SPEC Implementation Addendum

This addendum records implementation-level requirements derived from the current native compiler work. It complements `SPEC.md` without replacing its open-world principles.

## 1. Native Build Pipeline

The native compiler must expose one composable pipeline:

```text
FunctionIR / ModuleIR
    ↓
Reachability Analysis
    ↓
Target Validation
    ↓
Register Allocation / Spill Planning
    ↓
Stack Frame Layout
    ↓
Native Lowering
    ↓
Call ABI Lowering
    ↓
Symbol / Relocation Construction
    ↓
Multi-function Linking
    ↓
Code + Global Data Image
    ↓
Target Artifact Emission
    ↓
Artifact Verification
    ↓
Artifact Identity
    ↓
Build Report
```

Each stage must expose typed inputs and outputs and must be independently testable.

## 2. Target-Driven Compilation

Target information is part of compilation state, not merely metadata. At minimum, a native target identifies:

- operating system;
- architecture;
- ABI;
- calling convention;
- executable/object format;
- alignment rules;
- relocation rules;
- runtime assumptions.

Unsupported combinations must fail during preflight rather than producing an ambiguous artifact.

The target model remains open-world: validation rules may be extended by target definitions and must not become a permanent closed list.

## 3. Calls and Stack Frames

Native calls must be lowered according to the selected ABI. The implementation must model:

- register arguments;
- outgoing stack arguments;
- stack alignment;
- caller cleanup;
- callee prologue/epilogue;
- return-value locations;
- symbol references and relocations.

A call is not considered implemented merely because a textual or symbolic `call` exists. The emitted bytes, relocation semantics, frame state, and cleanup must agree.

## 4. Linking and Global Data

The linker must combine multiple native functions and global data into one deterministic image. Symbol resolution must distinguish:

- local code symbols;
- global data symbols;
- external symbols;
- unresolved symbols;
- duplicate definitions;
- relocation records.

Code/data placement and symbol offsets must be deterministic for identical inputs and target definitions.

## 5. Artifact Verification

A successful build must produce an artifact that can be independently verified. Verification must cover, as applicable:

- executable format validity;
- architecture/endianness;
- entry validity;
- entry-symbol consistency;
- symbol bounds;
- relocation consistency;
- section/layout consistency;
- content identity.

The artifact must have a stable cryptographic identity, currently SHA-256 in the bootstrap implementation.

## 6. Reproducible Build Identity

A build identity consists of the target identity, canonicalized build-manifest identity, and artifact content identity.

```text
BuildIdentity = Target + ManifestDigest + ArtifactDigest
```

The implementation must make it possible to determine whether two builds correspond to the same declared inputs and produce identical output content.

## 7. Build Driver

The build driver is responsible for orchestration, not for embedding the semantics of every compiler stage. It must coordinate:

1. preflight;
2. manifest construction;
3. compilation;
4. linking;
5. emission;
6. verification;
7. identity generation;
8. reporting.

This keeps the compiler modular while providing one end-to-end build entry point.

## 8. Self-Hosting

The bootstrap self-hosting path must progressively replace bootstrap-only infrastructure with Omni-owned infrastructure.

A self-hosting milestone is only complete when Omni can compile the relevant Omni source into a functioning artifact and independently verify that artifact. Merely copying source files, invoking an external compiler as the final implementation, or printing a success marker does not satisfy self-hosting.

## 9. Implementation Status Rule

This document distinguishes architecture from capability maturity. A subsystem may be represented and tested before it supports the complete universal behavior promised by the top-level specification. Implementations must not silently treat a partial backend, limited target set, or bootstrap mechanism as proof that universal compilation or universal target support is already complete.

The engineering objective remains to expand the typed, modular pipeline until additional languages, targets, operations, entities, and future definitions can be introduced without redesigning the entire system.
