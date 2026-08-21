# Omni — Universal Digital Creation, Compilation & Installation System

## 1. Complete Definition

Omni is an independent, self-contained, terminal-based programming language and a universal digital creation, compilation, packaging, installation, and execution system.

Its ultimate purpose is to make the digital world programmable through Omni itself.

Omni is designed around these fundamental capabilities:

1. **Universal Digital Creation** — create any digital entity using Omni.
2. **Universal Compilation** — process and compile source code from existing, historical, and future programming languages for existing, historical, and future targets.
3. **Universal Operating-System Creation** — create operating-system source code, kernels, runtimes, drivers, system components, and complete operating-system distributions for operating systems that exist today, existed in the past, or may exist in the future.
4. **Universal Packaging & Installation** — transform a completed digital system into a complete installable artifact and create the installer, installation environment, package format, bootable media, recovery environment, or deployment mechanism required by its target.
5. **Self-Hosting** — Omni must ultimately be capable of building and compiling its own compiler, runtime, tools, libraries, and infrastructure without fundamentally depending on another programming language or external compiler.

These capabilities are open-world capabilities. Omni must not be limited to a permanently hard-coded list of languages, operating systems, architectures, runtimes, formats, installers, or digital entities.

---

## 2. Omni Is an Independent Programming Language

Omni is a real programming language, not a wrapper around another language or compiler.

Omni is not fundamentally based on Python, C, C++, Go, Rust, Java, or another programming language.

The core Omni system must not require the user to install another language or compiler merely to use Omni's fundamental compilation capabilities.

The long-term architecture must reach true self-hosting:

```text
Omni Source
    ↓
Omni Compiler
    ↓
Universal Semantic IR
    ↓
Omni-owned compilation infrastructure
    ↓
Target Artifact
```

External tools may be supported as optional interoperability mechanisms where appropriate, but they must not define Omni's fundamental architecture or be treated as Omni's compiler.

---

## 3. Universal Digital Entity Creation

A **Digital Entity** is anything that can be digitally defined, represented, generated, stored, processed, executed, installed, distributed, or used.

Omni must be capable of creating, among other things:

- Software
- Desktop applications
- Mobile applications
- Websites and web applications
- Games and game engines
- AI models, AI agents, and AI systems
- Operating systems
- Kernels
- Bootloaders
- Drivers
- Runtimes
- Virtual machines
- Compilers and interpreters
- Programming languages
- IDEs and developer tools
- Databases
- APIs and network services
- CMS platforms, including systems comparable to WordPress
- Website builders
- App builders
- Game engines
- Software-generation systems
- Tools that create other tools
- Libraries and packages
- Plugins and extensions
- Protocols
- Data formats
- Images
- Audio and music
- Video and animation
- 3D models
- Digital documents and books
- Installation systems
- Package managers
- Bootable images
- Recovery systems
- Deployment systems
- Any digital entity that has not yet been invented

A system that creates software, a language that creates languages, or a system that creates other digital systems is itself a Digital Entity and must remain inside Omni's scope.

---

## 4. Universal Compilation

Omni must be able to process source code written in programming languages that exist today, existed historically, or may exist in the future.

Examples include:

- C
- C++
- Go
- Python
- Rust
- Java
- Kotlin
- JavaScript
- TypeScript
- C#
- Swift
- Dart
- PHP
- Zig
- Assembly
- LLVM IR
- Omni itself
- Historical languages
- Future languages
- User-defined languages

The architecture must be open-world rather than a hard-coded language list.

A language can be introduced through a sufficiently precise formal definition containing the information Omni needs to understand its syntax, semantics, type system, execution model, memory model, standard library interfaces, ABI/API expectations, and other relevant rules.

The intended model is:

```text
Source Code
    ↓
Omni Source Understanding
    ↓
Universal Semantic Representation
    ↓
Semantic Analysis
    ↓
Target Resolution
    ↓
Universal Backend / Emitter
    ↓
Target Artifact
```

Omni must not merely perform textual substitution. It must preserve or explicitly model program semantics.

---

## 5. Operating-System Source Creation, Compilation & Installation

This is a fundamental Omni requirement.

Omni must be able to create **source code for operating systems**, compile that source code, package the resulting system, and produce a complete installation solution.

This requirement applies to three categories of operating systems:

### 5.1 Existing Operating Systems

Omni must be architected to create, compile, package, and prepare installation artifacts for operating systems that currently exist, subject to their published technical specifications and target capabilities.

Examples include:

- Windows
- Linux distributions
- macOS
- ChromeOS
- Android
- iOS
- Other existing operating systems

### 5.2 Historical Operating Systems

Omni must also be capable of targeting operating systems that existed in the past.

If the historical target's specifications, ABI, executable format, boot protocol, hardware requirements, filesystem expectations, or other necessary information are available, Omni should be able to model that target and produce compatible source code, binaries, packages, disk images, or installation artifacts.

Examples may include historical operating systems and their historical hardware/platform environments.

Omni must not treat a historical operating system as impossible merely because it is no longer commercially supported.

### 5.3 Future Operating Systems

Omni must be able to model and target operating systems that do not yet exist when sufficient formal specifications are provided.

For a future operating system, Omni may require a target definition describing, for example:

- Kernel interface
- System calls
- ABI
- Executable format
- Boot protocol
- Runtime model
- Filesystem model
- Device model
- Hardware architecture
- Security model
- Package model
- Installation protocol
- Required platform capabilities

This does not mean Omni performs magic prediction. It means Omni is designed so that a sufficiently specified future operating system can be introduced as a new target without redesigning the compiler around a fixed list.

---

## 6. Complete Operating-System Build Pipeline

For an operating-system project, Omni must ultimately support a pipeline conceptually equivalent to:

```text
OS Specification / Omni Source / Source Code
                    ↓
          Source Understanding
                    ↓
          Universal Semantic IR
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
          Disk / System Image
                    ↓
       Installation Definition
                    ↓
       Installer / Bootable Media
                    ↓
        Complete Installable OS
```

Omni should therefore not stop at producing a kernel or executable. The architecture must include the ability to represent the **complete distributable system** and the process required to install it.

---

## 7. Universal Installer Creation

Omni must be capable of creating installers as Digital Entities.

An installer may include:

- Graphical installer
- Terminal installer
- Command-line installer
- Bootable installer
- Network installer
- Package installer
- System image installer
- Recovery installer
- Firmware-assisted installation
- Custom installation environments
- Future installation mechanisms

Omni must be capable of generating the installer software, its installation logic, its package metadata, its bootable media image where required, and the target-specific artifacts needed for a complete installation process.

The architecture must support operations such as:

```text
omni build my-os.omni
omni compile kernel.omni --target future-os
omni package my-os --target future-os
omni installer my-os --target future-os
omni image my-os --target future-os
```

These commands describe architectural goals; the exact CLI may evolve.

An installation target must be formally described sufficiently for Omni to know how the generated artifact is expected to be installed. Omni must not claim to install an undefined future operating system without the necessary target specification.

---

## 8. Historical, Existing, and Future Targets Are First-Class

The target model must not classify targets solely by whether they are currently popular or supported.

A target can be:

```text
Historical Target
Existing Target
Future Target
User-Defined Target
```

All of them must use the same extensible target architecture.

A target definition may contain:

- Operating system identity
- Version
- Architecture
- CPU model
- ABI
- Runtime
- Executable format
- Object format
- Calling convention
- Memory model
- Device model
- Boot model
- Filesystem model
- Security capabilities
- Package format
- Installation protocol
- Hardware capabilities
- Runtime capabilities
- Arbitrary future capabilities

No permanent closed target catalog is allowed by the architecture.

---

## 9. Self-Compilation of Omni

Omni source code must itself be compilable by Omni.

The intended direction is:

```text
Omni Source
    ↓
Omni Compiler
    ↓
Universal IR
    ↓
Target Backend
    ↓
Executable / Library / Runtime / Installer / Artifact
```

For example:

```text
Omni Code → Windows
Omni Code → Linux
Omni Code → macOS
Omni Code → Android
Omni Code → Historical Target
Omni Code → Future Target
```

This is a fundamental part of the path toward true self-hosting.

---

## 10. Future Languages and Open-World Semantics

Omni must not contain a permanently fixed list such as C++, Go, Python, and Rust and then stop.

Instead:

```text
Future Language
      ↓
Formal Language Definition
      ↓
Omni Language Model
      ↓
Universal Semantic Representation
      ↓
Target Resolution
      ↓
Output
```

A future language can be supported when sufficient information about its syntax, semantics, execution model, and target requirements is available.

---

## 11. Ecosystem Compatibility

Omni must support interoperability with:

- Libraries
- Packages
- Frameworks
- Plugins
- Extensions
- Dependencies
- Runtime components
- APIs
- ABI-compatible components
- Omni-native libraries
- Omni-native packages
- Omni-native plugins

Examples include ecosystems associated with C/C++, Python, Go, Rust, Java, JavaScript, and future ecosystems.

Compatibility must be designed as an extensible capability rather than a hard-coded list of known packages.

---

## 12. Multimedia and Non-Executable Digital Entities

Digital entities are not limited to executable programs.

Omni must be able to model and generate or process:

- Images
- Audio
- Music
- Video
- Animation
- 3D models
- Documents
- Books
- Data files
- Future media formats

The same open-world entity architecture must apply to these formats.

---

## 13. Future Digital Entities

Omni must be designed to create digital entities that do not yet exist.

This includes future:

- Applications
- Operating systems
- Programming languages
- Libraries
- Plugins
- File formats
- Architectures
- CPUs
- Runtimes
- ABIs
- Package systems
- Installation systems
- Digital media types
- Entire classes of digital systems

Omni does not need supernatural knowledge of undefined systems. A genuinely new system must provide, or be represented by, enough formal specifications and semantics for Omni to reason about it.

---

## 14. Universal Installation & Distribution Model

Omni must treat distribution and installation as first-class digital build stages rather than external afterthoughts.

A complete project may therefore contain:

```text
Source
  ↓
Semantic Model
  ↓
Compilation
  ↓
Artifacts
  ↓
Packaging
  ↓
Installer Generation
  ↓
Bootable / Deployable Media
  ↓
Installable Product
```

For an application, this may produce an application package or installer.

For an operating system, this may produce a disk image, bootable media, installation environment, package repository, recovery image, and installer.

For another digital entity, Omni may define a different distribution mechanism through its open-world entity and target models.

---

## 15. Architecture

The intended high-level architecture is:

```text
                  Any Digital Concept
                         │
                         ▼
              Omni Language / Input Layer
                         │
                         ▼
                Source Understanding
                         │
                         ▼
             Universal Semantic Model / UIR
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Digital Entity Model   Universal Compiler
              │                     │
              ▼                     ▼
       Creation / Generation   Semantic Translation
              │                     │
              └──────────┬──────────┘
                         ▼
                 Target Resolution
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Historical       Existing       Future
       Targets         Targets        Targets
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                Backend / Materializer
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Executable      Package       OS Image
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                Installer Generation
                         │
                         ▼
              Complete Installable Artifact
```

---

## 16. Terminal Experience

From the user's perspective, Omni is a terminal-based language and toolchain.

Examples of the intended interface include:

```text
omni build project.omni
omni run project.omni
omni compile program.cpp --target windows
omni compile program.c --target historical-os
omni compile program.future --target future-os
omni os build my-os.omni
omni package my-os
omni installer my-os --target windows
omni installer my-os --target future-os
omni image my-os --target future-os
```

The exact commands are implementation details and may evolve. The capabilities they represent are architectural requirements.

---

## 17. Fundamental Constraint: Specifications Matter

Omni is intentionally ambitious but not magical.

Omni can only correctly compile, create, package, or install a target when the information necessary to define that target is available.

For existing targets, this may include published specifications and compatibility information.

For historical targets, historical technical documentation and target information may be required.

For future targets, a formal target specification must be supplied before Omni can generate a correct target-specific artifact.

Therefore:

> Open-world does not mean undefined-world. Omni must be able to model any sufficiently specified digital world without redesigning its fundamental architecture.

---

## 18. Final Definition

> **Omni is an independent, self-contained, terminal-based programming language and universal digital creation, compilation, packaging, installation, and execution system. Its goal is to make it possible to create any digital entity with Omni itself, including software, websites, games, AI systems, operating systems, kernels, runtimes, compilers, programming languages, databases, APIs, libraries, plugins, multimedia, installers, and systems that create other systems. Omni must also be able to process and compile source code from programming languages that exist today, existed historically, or may exist in the future, without making external compilers a fundamental requirement of Omni. It must be able to target operating systems, architectures, runtimes, ABIs, execution environments, package formats, and installation systems that exist today, existed in the past, or may exist in the future, provided the necessary specifications are available. For operating systems in particular, Omni must be capable of creating source code, compiling it, assembling the complete system, packaging it, generating installation artifacts and installers, producing bootable or deployable media where required, and preparing a complete installable operating-system distribution. The architecture must be open-world, extensible, semantically driven, and ultimately self-hosting, so that Omni itself can build and compile its compiler, runtime, libraries, tools, and infrastructure.**

---

## 19. Simplest Definition for Non-Programmers

> **Omni aims to be an all-purpose language for the digital world: a language with which you can build digital things, create and compile operating systems from different eras, build installers and complete installable systems, compile code for today's and tomorrow's platforms, and extend the system to support new languages, technologies, and digital entities that do not exist yet—when their required specifications are available.**
