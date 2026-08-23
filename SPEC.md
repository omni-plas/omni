# Omni — Universal Digital Creation, Transformation, Operations & Delivery System

## 1. Supreme Definition

Omni is an independent, self-contained, terminal-based programming language and open-world universal digital system for defining, understanding, creating, transforming, compiling, building, testing, repairing, optimizing, packaging, installing, executing, deploying, maintaining, migrating, and extending digital entities and digital capabilities.

Its fundamental capability is:

> **Given a sufficiently defined digital idea, requirement, specification, operation, artifact, source, partial project, existing digital entity, or intermediate state, Omni must be able to understand the required result, determine the applicable remaining work, perform that work, validate it, and continue until the requested usable digital capability or product is reached.**

This applies to digital entities and digital operations that existed in the past, exist today, or may exist in the future; at any time and in any place; across languages, platforms, operating systems, CPUs, architectures, runtimes, ABIs, executable formats, filesystems, environments, protocols, package systems, and targets, whenever the information required for correct realization is available or can be formally defined.

Omni is not limited by a permanent list of languages, compilers, operating systems, architectures, operations, entities, products, formats, or capabilities.

Programming is one part of the complete Omni lifecycle. Omni remains a genuine programming language while the complete system encompasses the broader transformation from digital intent or state to usable digital result.

---

## 2. One Fundamental Capability

All Omni subsystems are manifestations of one capability:

> **Turn sufficiently defined digital intent or digital state into the required digital result by performing whatever applicable digital operations and construction stages are necessary.**

This includes programming, source understanding, compilation, code generation, transformation, creation, build systems, testing, debugging, repair, optimization, linking, assembly, packaging, installer generation, deployment, installation, execution, updating, maintenance, migration, conversion, automation, digital-content processing, and creation of new digital capabilities.

---

## 3. Universal Digital Operation Principle

Omni must be capable of representing and performing digital operations that:

1. existed historically;
2. exist currently; and
3. can be defined in the future.

A Digital Operation is any digitally realizable transformation, computation, construction, processing action, orchestration, interaction, generation, conversion, execution, deployment, maintenance action, or other formally representable activity.

Examples include creating and transforming files, compiling source, translating languages, building executables, generating operating systems, creating installers, processing media, running programs, deploying services, updating software, repairing projects, migrating systems, generating tools, creating languages, creating compilers, creating formats, and creating entirely new classes of digital operations.

The architecture must not depend on a permanent hard-coded operation catalog. A new operation must be representable through sufficiently precise semantics, inputs, outputs, constraints, resources, effects, interfaces, dependencies, and execution requirements.

---

## 4. First-Capability Principle

Omni is intended not merely to reproduce existing capabilities.

> **Whenever a digital capability is technically and formally definable and its required specifications, semantics, resources, interfaces, constraints, and execution conditions can be satisfied, Omni should be capable of defining, constructing, validating, and operationalizing it even if no previous system was capable of doing so. Omni may therefore become the first system to provide a particular digital capability.**

This principle applies to every Omni capability, including new operations, entities, languages, compilers, runtimes, operating systems, architectures, targets, ABIs, formats, protocols, libraries, packages, plugins, installers, deployment mechanisms, multimedia formats, tools, and systems that create other systems.

This is an engineering requirement, not a claim of magic. Undefined requirements, unavailable information, impossible physical conditions, or unsatisfied execution constraints remain genuine limitations.

---

## 5. Any Time, Any Place, Any Stage

The principles of universality and first capability apply **for every time and every place**.

Unless a target explicitly imposes a limitation, every Omni subsystem must be designed to operate across historical, current, and future technologies and environments, including physical and virtual platforms, operating systems, CPUs, architectures, runtimes, ABIs, executable formats, filesystems, hardware interfaces, development environments, execution environments, and deployment environments.

A historical, future, or unknown target does not have to be hard-coded into Omni. It must be representable by a sufficiently precise target definition.

"Any" does not mean creation from zero information. Omni must require and model enough authoritative information to determine correct behavior.

---

## 6. Independent Programming Language

Omni is a genuine independent programming language.

It is not fundamentally based on Python, C, C++, Go, Rust, Java, JavaScript, or any other external language.

Omni must not merely wrap GCC, Clang, MSVC, another compiler, interpreter, runtime, or external build system.

External tools may be used as optional interoperability or bootstrap mechanisms, but they must never define Omni's fundamental architecture or remain a mandatory dependency for Omni's core operation once Omni's own infrastructure is capable of performing the required work.

The language used to implement an early Omni implementation does not by itself define a runtime dependency. For example, implementing early Omni components in Python does **not** mean the resulting Omni system is fundamentally Python-dependent.

---

## 7. Omni Must Be Able to Build Omni

**Self-build is a mandatory Omni capability.**

Omni source code must itself be understandable, compiled, built, tested, packaged, installed, executed, and updated by Omni.

The target architecture is:

```text
Omni Source
    ↓
Omni Frontend / Compiler
    ↓
Universal Semantic Representation
    ↓
Omni-Owned Compilation Infrastructure
    ↓
Omni Compiler / Runtime / Tools
    ↓
Executable / Library / Package / Installer
    ↓
New Omni
```

Omni must ultimately be able to build its own:

- compiler;
- frontend and parser infrastructure;
- semantic system;
- optimizer;
- backends and code generators;
- runtime;
- standard library;
- package and installer tools;
- command-line tools;
- plugins and extensions;
- core infrastructure;
- and other components required for a complete Omni distribution.

Self-build must not be a demonstration that only copies files or prints success. It must produce a functioning Omni implementation.

---

## 8. Self-Hosting and Bootstrap Independence

The project may use Python or other tools during bootstrap, development, testing, or interoperability. Such tools are implementation aids, not permanent architectural requirements.

The intended progression is:

```text
Bootstrap Implementation
        ↓
Working Omni Compiler
        ↓
Omni builds Omni Compiler
        ↓
Self-hosted Omni
        ↓
Omni builds future Omni versions
```

A mature Omni installation should be capable of rebuilding itself from Omni source without requiring the original bootstrap language/compiler as a fundamental prerequisite.

A self-hosting build must be reproducible and independently validated.

---

## 9. Universal Digital Entity Scope

A Digital Entity is anything that can be digitally defined, represented, generated, stored, transformed, processed, executed, distributed, installed, or used.

Omni must be architected to create or transform software, desktop and mobile applications, websites, games, engines, AI models and systems, operating systems, kernels, bootloaders, drivers, firmware, runtimes, virtual machines, compilers, interpreters, programming languages, IDEs, developer tools, databases, APIs, network services, CMS systems, libraries, packages, frameworks, plugins, protocols, data formats, images, audio, music, video, animation, 3D models, documents, books, installers, package managers, bootable images, recovery systems, deployment systems, historical entities, existing entities, future entities, and systems that create other systems.

A program that creates programs, a language that creates languages, and a system that creates digital systems are all within scope.

---

## 10. Universal Lifecycle

A project may enter Omni at any meaningful stage:

```text
Idea
Specification
Requirement
Design
Architecture
Source
Partial Source
Repository / Project
Components
Libraries
Packages
Build Artifacts
Binary / Executable
System Image
Installer
Existing Digital Product
```

Omni must inspect the current state, model requirements and semantics, identify missing information, generate or complete determinable parts, compile/build/transform, link/assemble where applicable, test, validate, debug, repair, optimize, package, create installers or images, install/deploy, configure, execute/use, and maintain the result as required.

Not every result needs every stage. Omni must select the stages appropriate to the requested product.

---

## 11. Universal Source-to-Product Capability

Omni must not stop at textual translation or an intermediate representation when the requested result is a usable product.

```text
Source
  ↓
Language Understanding
  ↓
Semantic Analysis
  ↓
Dependency Resolution
  ↓
Universal Semantic Representation
  ↓
Transformation / Compilation
  ↓
Link / Assemble
  ↓
Test / Validate
  ↓
Package
  ↓
Installer / Image / Deployment Artifact
  ↓
Usable Product
```

Incomplete source may enter the pipeline. Omni should complete whatever can be determined from specifications, project context, dependencies, semantics, constraints, and rules.

Program semantics must be preserved or explicitly modeled; simplistic textual substitution is insufficient for general compilation.

---

## 12. Universal Compilation

Omni must be capable of understanding and processing languages of the past, present, and future.

Examples include C, C++, Go, Python, Rust, Java, Kotlin, JavaScript, TypeScript, C#, Swift, Dart, PHP, Zig, Assembly, LLVM IR, Omni, historical languages, future languages, and user-defined languages.

This is not a permanent whitelist.

A language may be introduced through a sufficiently precise definition containing syntax, semantics, type rules, execution model, memory model, ABI/API expectations, standard-library interfaces, dependency rules, and other necessary rules.

The intended architecture is:

```text
Source
  ↓
Language Understanding
  ↓
Universal Semantic Representation
  ↓
Semantic Analysis
  ↓
Target Resolution
  ↓
Omni-Owned Backend / Emitter
  ↓
Target Artifact
```

Omni must ultimately perform fundamental compilation itself rather than requiring the original language compiler as a permanent dependency.

---

## 13. Frontend Extensibility

Language frontends are first-class, modular, and extensible.

A frontend may declare:

- canonical language identity;
- aliases;
- language versions;
- dialects;
- source extensions;
- syntax rules;
- semantic rules;
- type system rules;
- dependency model;
- execution model;
- priority and compatibility metadata.

Frontend resolution must be deterministic and must select an implementation capable of interpreting the requested language/version/variant.

Adding a new language must not require redesigning the entire compiler architecture.

---

## 14. Universal Target Model

Targets are first-class, descriptive, extensible objects.

A target may represent a historical, existing, future, or user-defined environment.

Target definitions may include operating system, version, architecture, CPU, ABI, runtime, executable format, object format, calling convention, memory model, device model, boot model, filesystem, security capabilities, package format, installation protocol, hardware capabilities, runtime capabilities, and arbitrary future capabilities.

No permanent closed target catalog is allowed.

---

## 15. Operating-System Creation

Operating systems are first-class Digital Entities.

Omni must be capable of creating operating-system source, kernels, boot components, drivers, runtimes, system components, filesystems, package layouts, system images, installers, and complete installable distributions.

This applies to historical, current, and future operating systems when their required specifications are available or formally defined.

---

## 16. Complete Operating-System Build

For a complete OS request, Omni must be able to continue through the applicable lifecycle:

```text
OS Specification / Source / Existing Project
                 ↓
         Language Understanding
                 ↓
       Universal Semantic Model
                 ↓
              OS Model
                 ↓
       Kernel / Runtime / Drivers
                 ↓
          System Components
                 ↓
          Root Filesystem
                 ↓
       Package / File Layout
                 ↓
       Boot & Startup Components
                 ↓
            System Image
                 ↓
       Installation Definition
                 ↓
      Installer / Bootable Media
                 ↓
        Complete Installable OS
```

Omni must not stop at a kernel or executable when the requested product is a complete operating system.

---

## 17. Universal Installer and Deployment Creation

Installers and deployment mechanisms are first-class Digital Entities.

Omni must support, as appropriate, graphical, terminal, command-line, bootable, network, package, system-image, recovery, firmware-assisted, custom, and future installation mechanisms.

Omni must generate the required installer software, installation logic, metadata, package layout, media image, and target-specific artifacts.

Distribution, installation, deployment, configuration, update, rollback, recovery, migration, and maintenance are all part of the lifecycle when required by the requested product.

---

## 18. Any Language + Any Target + Any Era

Universal compilation and product creation must compose independently:

```text
Any Language
+ Any Source Stage
+ Any Target
+ Any Era
+ Any Environment
        ↓
      OMNI
        ↓
Analyze / Transform / Build
        ↓
Test / Repair / Optimize
        ↓
Package
        ↓
Installer / Image / Artifact
        ↓
Usable Digital Product
```

The architecture must not assume that language, target, era, or environment are known in advance.

---

## 19. Future Languages and Open-World Semantics

Future or user-defined languages must be introducible through sufficiently precise definitions.

The same open-world mechanism applies to future file formats, protocols, package systems, runtimes, architectures, operating systems, and digital entities.

```text
Future Specification
        ↓
Omni Model
        ↓
Semantic Representation
        ↓
Implementation
        ↓
Validation
        ↓
Usable Capability
```

---

## 20. Ecosystem Compatibility

Omni must support interoperability with libraries, packages, frameworks, plugins, extensions, dependencies, runtime components, APIs, ABI-compatible components, and Omni-native components.

Compatibility must remain extensible and must not become a permanently hard-coded catalog.

An external dependency must not inherently prevent a project from being transformed into a usable product when the dependency can be correctly represented, resolved, built, packaged, replaced, or integrated under the target rules.

---

## 21. Multimedia and Non-Executable Entities

Omni includes non-executable digital content in its entity model and must be architected to create, transform, process, package, distribute, and operate on images, audio, music, video, animation, 3D models, documents, books, data files, and future media formats.

---

## 22. Future Digital Entities

Omni must be designed to create digital entities that do not yet exist, including future applications, operating systems, programming languages, libraries, plugins, formats, architectures, CPUs, runtimes, ABIs, package systems, installation systems, media types, and entire classes of digital systems.

A genuinely new entity requires sufficient formal specifications, semantics, constraints, interfaces, or other authoritative information.

---

## 23. Universal Operation and Capability Construction

Every Omni subsystem must permit a capability to become an input to Omni itself.

```text
Operation / Capability Definition
             ↓
       Semantic Model
             ↓
 Implementation / Construction
             ↓
        Compilation
             ↓
        Validation
             ↓
    First Working Capability
```

Capabilities must be composable so existing capabilities can create new capabilities.

---

## 24. First-Capability Principle Applies Everywhere

The First-Capability Principle is global.

For every subsystem:

```text
Existing Capability
       OR
Newly Defined Capability
       ↓
      Omni
       ↓
 Implementation
       ↓
First Working Result
```

No subsystem may be architecturally restricted merely because an equivalent capability did not previously exist.

---

## 25. Open-World Requirement

The following must not be permanent architectural limits:

- number of languages;
- number of language versions or dialects;
- number of operating systems;
- number of CPUs or architectures;
- number of runtimes or ABIs;
- number of formats or protocols;
- number of package systems or installers;
- number of digital entities;
- number of operations;
- number of capabilities;
- number of self-build generations.

New specifications, frontends, backends, target models, semantic models, adapters, plugins, and construction mechanisms must be introducible without redesigning the entire system.

---

## 26. Architecture

The intended high-level architecture is:

```text
                 Digital Idea / Requirement / Existing State
                                  │
                                  ▼
                       Omni Input & Language Layer
                                  │
                                  ▼
                         Understanding / Inspection
                                  │
                                  ▼
                    Universal Semantic Model / UIR
                                  │
                   ┌──────────────┴──────────────┐
                   ▼                             ▼
             Digital Entity Model          Operation Model
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                      Capability / Construction Layer
                                  │
                                  ▼
                       Universal Compilation Layer
                                  │
                                  ▼
                           Target Resolution
                                  │
                   ┌──────────────┼──────────────┐
                   ▼              ▼              ▼
               Historical      Existing        Future
                Targets        Targets         Targets
                   │              │              │
                   └──────────────┼──────────────┘
                                  ▼
                          Backend / Generator
                                  │
                                  ▼
                               Artifact
                                  │
                                  ▼
                            Materialization
                                  │
                                  ▼
                              Packaging
                                  │
                                  ▼
                          Installer / Image
                                  │
                                  ▼
                       Deployment / Installation
                                  │
                                  ▼
                            Usable Product
                                  │
                                  ▼
                       Execute / Update / Maintain
                                  │
                                  ▼
                         Self-Build / Self-Host
                                  │
                                  └──────→ Omni Source
```

Every layer must remain modular, testable, replaceable, and extensible.

---

## 27. Product Completion Principle

When a user asks Omni to create a product, Omni must not stop at an intermediate artifact merely because that artifact is technically valid.

The requested product definition determines the required completion level.

For example:

```text
Source → Executable
```

may be sufficient for one request, while another requires:

```text
Source → Executable → Package → Installer → Installable Product
```

For an operating system the requested completion may be:

```text
Source → Kernel → Components → RootFS → Image → Bootable Media → Installer → Installable OS
```

---

## 28. Partial-State Continuation Principle

Any sufficiently defined intermediate state may become an Omni input.

Omni must be able to continue from partial source, partial compiler, partial language, partial OS, partial application, partial game, partial AI system, partial library, partial package, partial installer, partial artifact, existing executable, existing system image, or existing repository.

The goal is to understand the current state and continue toward the requested result rather than unnecessarily restarting.

---

## 29. Self-Build Completion and Verification Requirements

Self-build is complete only when Omni can perform a genuine end-to-end rebuild of Omni from Omni source.

A valid self-build cycle must demonstrate, as applicable:

1. Omni source is accepted by Omni.
2. Omni compiles/builds its own compiler and required core components.
3. The generated implementation is executable and usable.
4. The generated implementation can build Omni again.
5. The resulting build is validated against the source and expected behavior.
6. Repeated self-builds are deterministic or have explicitly modeled, acceptable nondeterminism.
7. The bootstrap dependency is no longer required for the mature self-hosted path.

The system must test self-build rather than merely claim it.

---

## 30. Definition of a Complete Omni Result

A result is complete when it satisfies the requested entity or capability's target requirements and reaches the requested usable state.

Depending on the request this may be a source project, compiled artifact, runnable program, package, installer, bootable image, installable operating system, deployed service, digital document, processed media file, new operation, new capability, or any other appropriately defined digital result.

Omni must distinguish intermediate artifacts from final requested products.

---

## 31. Non-Magical but Open-Ended Constraint

Universal claims are bounded by what can be formally specified and technically realized.

Omni does not need to predict an undefined future system without information about it. Instead, Omni must provide mechanisms for introducing the required information.

For a requested result, Omni may require enough information to determine semantics, inputs, outputs, constraints, interfaces, dependencies, resources, target requirements, execution requirements, security requirements, compatibility requirements, installation requirements, and other rules necessary for correctness.

Once necessary information is available or formally defined, the architecture must not impose an arbitrary limitation merely because the entity, operation, language, target, or capability is new.

---

## 32. User-Facing Model

Omni remains a terminal-based programming language and tool.

Illustrative commands include:

```text
omni build project.omni
omni run project.omni
omni compile program.cpp --target windows
omni build os.spec --target future-os
omni install project.omni
omni transform input.digital --operation new-operation
omni self-build
```

The exact command set may evolve. The user-facing model must expose the same fundamental lifecycle: define or provide digital intent/state, specify the required result and target, and allow Omni to perform the applicable work.

---

## 33. Engineering Invariants

The following are permanent design invariants:

1. **Open World:** never assume the universe of languages, targets, entities, operations, or capabilities is closed.
2. **Semantic Correctness:** general compilation and transformation must model semantics rather than depend on textual substitution.
3. **Independence:** external languages and compilers are not fundamental architectural dependencies.
4. **Self-Build:** Omni must ultimately build Omni from Omni source.
5. **First Capability:** Omni may implement capabilities that did not previously exist whenever they are sufficiently specified and technically realizable.
6. **Any Time / Any Place:** the above principles apply across historical, current, and future environments and targets.
7. **Continuation:** Omni should continue from any sufficiently defined intermediate state toward the requested result.
8. **Product Completion:** do not stop at an intermediate artifact when the requested product requires further stages.
9. **Validation:** generated artifacts and capabilities must be validated against their target and semantic requirements.
10. **Modularity:** new languages, targets, operations, entities, backends, frontends, formats, and capabilities must be addable without fundamental redesign.
11. **No Fake Completion:** demo output, placeholders, success-only stubs, or claims without functional implementation do not satisfy a capability requirement.
12. **Reproducibility:** builds and transformations should be deterministic where the target permits it and must explicitly model unavoidable nondeterminism.

---

## 34. Development and Verification Rules

Implementation work on Omni must follow these rules:

- Do not create demo or placeholder code that only prints a success message.
- Model and validate UIR and other representations rather than treating them as arbitrary dictionaries or strings.
- Keep the project modular and extensible.
- Add automated tests for implemented capabilities.
- Maintain CI for supported development environments.
- Every implemented capability must have a path from specification to executable/testable behavior.
- Every change must be evaluated against this SPEC.md.
- Existing functionality must not be silently discarded merely to simplify implementation.
- If an operation fails, investigate the cause, fix it where possible, and continue.
- Prefer completing all work that can be performed with available tools instead of stopping for unnecessary confirmations.
- A capability is not considered complete merely because its API exists; the underlying behavior must work.

SPEC.md is the authoritative definition of the Omni project. Every operation, implementation stage, architectural decision, test, and extension must be evaluated against this document.

---

## 35. Final Definition

> **Omni is an independent, self-contained, terminal-based programming language and open-world universal digital creation, transformation, operation, compilation, build, testing, repair, optimization, packaging, installation, deployment, execution, maintenance, and self-building system. Its fundamental capability is to take a sufficiently defined digital idea, requirement, operation, source, artifact, partial project, existing digital entity, or intermediate state at any stage of its lifecycle and perform the remaining applicable work required to turn it into the requested usable digital capability or product. This applies to digital entities and digital operations of the past, present, and future, at any time and in any place, across relevant languages, operating systems, CPUs, architectures, runtimes, ABIs, platforms, formats, environments, and targets, provided the specifications, semantics, interfaces, dependencies, resources, constraints, and other information required for correct realization are available or can be formally defined. Omni is a real programming language and must ultimately be self-hosting: Omni must be able to compile and build Omni itself, including its compiler, runtime, tools, libraries, packages, and core infrastructure, and mature Omni must not fundamentally depend on the bootstrap language or external compiler used to create its earliest implementation. Omni's architecture is open-world and extensible rather than a permanent closed catalog. It is intended not merely to reproduce existing capabilities but, whenever a capability is sufficiently specified and technically realizable, to define, construct, validate, and operationalize capabilities that did not previously exist, potentially making Omni the first system capable of providing them. The First-Capability Principle, self-build requirement, independence requirement, continuation requirement, and any-time/any-place requirement apply to every part of Omni.**

---

## 36. Simplest Definition for a Non-Programmer

> **Omni is intended to be an all-purpose system for the digital world. You can give it an idea, an operation, source code, a partly built project, an existing digital thing, or a precise description of something new, and—when the needed information and technical conditions exist—it is designed to do the digital work needed to produce the result you want. It is also designed to create things that did not exist before, perform operations that had not been possible before, and eventually build and rebuild Omni itself without depending on the language that was used to bootstrap it.**
