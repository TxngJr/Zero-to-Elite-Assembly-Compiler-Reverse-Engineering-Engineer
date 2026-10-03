# Theory — Integrating the Full Systems Stack

## 1. The Course Is One Pipeline

The chapters are not isolated subjects.

```text
C / Assembly knowledge
       ↓
compiler output understanding
       ↓
ELF/linking/debugging
       ↓
kernel/toolchain engineering
       ↓
reverse engineering
       ↓
defensive root-cause analysis
```

Each layer gives evidence about adjacent layers.

## 2. Source to Execution

EliteC pipeline:

```text
characters
→ tokens
→ AST
→ type checking
→ IR/basic blocks
→ optional optimization
→ x86-64 assembly
→ assembler
→ ELF
→ dynamic loader/runtime
→ CPU
```

At every arrow ask:
- what representation changed?
- which invariants were introduced?
- what information was lost?
- what information was added?

## 3. Representation Boundaries

Good systems engineering depends on explicit boundaries.

Examples:
- AST has source structure but no target registers
- IR has control/data flow but no exact x86 encoding
- assembly has target instructions but symbolic labels
- ELF adds sections/symbols/relocations/load metadata
- process memory adds runtime addresses/mappings

Confusing these layers causes debugging mistakes.

## 4. Compiler Correctness vs Optimization

A correct compiler preserves supported language semantics.

Optimization is secondary.

The course backend intentionally starts with stack slots because an inefficient correct compiler is a much better engineering base than an aggressively optimized incorrect one.

## 5. ABI as a Bridge

ABI connects compiler-generated code to other compiled functions and runtime startup.

Important facts:
- argument registers
- stack arguments
- return registers
- caller/callee saved registers
- stack alignment
- object/linkage conventions

The ABI is where compiler, linker, debugger and OS-user-space assumptions meet.

## 6. ELF as Shared Evidence

ELF appears in:
- compiler output
- linker output
- dynamic loading
- debugger symbols
- reverse engineering
- kernel image construction

Learning ELF once pays across many disciplines.

## 7. Hosted vs Freestanding

EliteC user programs are hosted Linux executables.

EliteOS64 is freestanding:

```text
user program:
runtime / libc-ish startup / kernel already exist

kernel:
must establish stack, mappings, interrupts and devices itself
```

Never transfer hosted assumptions into early kernel code blindly.

## 8. Boot as Representation Transition

EliteOS64 boot sequence changes machine state:

```text
GRUB contract
→ protected-mode entry
→ early physical structures
→ page tables
→ control registers/MSRs
→ long mode
→ C kernel ABI
```

Boot debugging means locating the first failed transition.

## 9. OS Mechanisms Build on Hardware Contracts

Page tables, GDT, IDT, PIC/PIT and privilege levels are not abstractions invented by C code. The kernel programs hardware-defined interfaces.

Always verify privileged mechanisms against architecture documentation when evolving beyond the course.

## 10. Algorithms Before Privileged Integration

Chapter 15 deliberately models scheduler/COW/VFS/IPC in user-space.

Why?

- deterministic tests
- no boot cycle for every algorithm bug
- clear invariants
- easier sanitizers/debuggers

Then integration into the kernel becomes a separate engineering problem.

## 11. Reverse Engineering Is the Pipeline in Reverse

Forward:

```text
source intent → compiler → machine artifact
```

Reverse:

```text
machine artifact → evidence → reconstructed structure → tentative semantics
```

Reverse engineering cannot always recover original names/types/comments/source structure exactly.

## 12. Facts vs Inference

Example:

Fact:
```text
instruction accesses [rdi+8] as a 64-bit value
```

Inference:
```text
this may be an 8-byte struct field at offset 8
```

Unsupported claim:
```text
this is definitely user.balance
```

Capstone reports should preserve that distinction.

## 13. Debugging and RE Meet at Runtime State

GDB provides:
- mappings
- registers
- memory
- call stack
- instruction stream

This runtime evidence can confirm or reject static hypotheses.

## 14. Defensive Security Is Debugging Under a Trust Boundary

Security root-cause analysis adds questions:

- can untrusted input reach this code?
- what invariant is violated?
- what data/control is affected?
- what privileges does the process have?
- what evidence supports impact?

Do not jump from bug class to dramatic exploit claims.

## 15. Sanitizers as Evidence

ASan/UBSan are dynamic instruments.

They are excellent for:
- finding invalid operation near root cause
- regression
- fuzz integration

They do not prove absence of defects.

## 16. Fuzzing as Search

Fuzzing searches state space.

A good fuzz target is:
- deterministic
- fast
- isolated
- explicit input buffer + size
- free from external side effects

Every discovered case should become a regression input after root-cause confirmation.

## 17. Reproducibility

Final engineering artifacts should include:

- commit
- tool versions
- commands
- build flags/options
- SHA-256 hashes
- test results
- limitations

“Works on my machine” is not enough evidence.

## 18. Artifact Hashes

Hashing helps identify exactly which artifact was inspected/tested.

It does **not** prove software is safe or authentic by itself unless tied to trusted provenance/signatures.

## 19. Integration Tests

Unit tests prove local behavior.

Integration tests prove boundaries connect.

Capstone checks:
- EliteC → executable
- executable → ELF/RE tooling
- EliteOS source → kernel ELF/Multiboot validation
- advanced-OS algorithms → deterministic tests
- defensive labs → regression/fuzz checks

## 20. Why the Capstone Does Not Run the Full Root Verifier

Root verifier executes Chapter 18.

If Chapter 18 called root verifier, recursion would occur:

```text
verify → capstone → verify → capstone → ...
```

Capstone therefore calls selected integration gates only.

## 21. Failure Classification

When final audit fails, classify first:

- source/compiler error
- assembler/linker error
- runtime semantic error
- ELF inspection mismatch
- kernel build/image error
- simulator invariant failure
- RE tooling parsing limitation
- defensive regression failure
- environment/tool missing

Classification prevents random edits.

## 22. Engineering Claims Need Evidence

Bad:
> My compiler is production ready.

Better:
> The educational compiler passes recursion, loops, short-circuit and >6-argument ABI tests on Linux x86-64, while full SSA, production register allocation and source-level DWARF remain incomplete.

Precision makes a portfolio stronger.

## 23. Technical Debt Is Part of the Result

EliteC debt examples:
- full SSA integration
- real register allocation
- richer type system
- object emission
- source debug info

EliteOS debt examples:
- robust exception frames
- VMM
- user mode
- scheduler integration
- syscalls
- VFS
- APIC/SMP

Documenting debt demonstrates engineering maturity.

## 24. Validation Pyramid

```text
static checks
→ unit tests
→ integration tests
→ sanitizer/fuzz tests
→ VM/boot tests
→ hardware tests
```

Not every environment supports every level. Report which were actually performed.

## 25. QEMU vs Hardware

QEMU is a controlled platform for OS development.

A successful emulator boot does not prove hardware compatibility across firmware/chipsets/devices.

## 26. Security Scope

Capstone RE/security analysis remains on course-owned or explicitly authorized targets.

No capstone grade requires bypassing real security controls or touching external systems.

## 27. Portfolio Structure

Strong portfolio artifact:

1. architecture diagram
2. design decisions
3. runnable demonstration
4. tests
5. disassembly/ELF evidence
6. debugging case study
7. security root-cause case study
8. limitations
9. future work

## 28. Oral Defense

You should be able to answer:

- Why does stack alignment matter?
- Why can PIE runtime addresses differ?
- Why is `.bss` not stored as full zero bytes?
- Why can a TLB miss succeed without page fault?
- Why does COW require write-protected mappings?
- Why is sanitizer crash location not always original corruption point?
- Why can O2 destroy source-like function boundaries?

## 29. Independent Rebuild

A meaningful final exercise is deleting generated artifacts and rebuilding from source.

Capstone `make clean test` is designed for this.

## 30. Final Mental Model

```text
Representation
→ Contract
→ Mechanism
→ Evidence
→ Test
→ Explanation
```

If you can repeatedly move through these six steps across compiler, OS, debugging, RE and defensive security tasks, you have the foundation this course is designed to build.
