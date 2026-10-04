# Troubleshooting

## Full verifier takes a while
Expected. Chapters 00–18 build and test many compiler/kernel/analysis projects. For one area, run that chapter's `make test` first.

## Capstone audit fails at EliteC
Run:
```bash
make -C 12-my-compiler clean test
python3 12-my-compiler/projects/elitec/elitec.py --check 18-capstone/examples/capstone.el
```

## Capstone audit fails at ELF/RE tools
Confirm `file`, `readelf`, `objdump`, `nm`, `strings` are installed from binutils/file packages.

## Capstone kernel gate fails
Run `make -C 14-my-os clean test` first. The automated capstone does not require QEMU/GRUB; it validates the kernel ELF and Multiboot2 contract.

## Capstone Advanced-OS gate fails
Run `make -C 15-advanced-os clean test`. These are host-side deterministic models, not privileged kernel execution.

## Capstone RE gate fails
Run `make -C 16-reverse-engineering clean test`. Targets are generated locally from course source.

## Capstone defensive gate fails
Run `make -C 17-security-lab clean test`. Default tests use fixed code; the deliberately buggy sanitizer target is separate.

## audit-summary git_commit says unavailable
The audit can run from a source archive without `.git`. Artifact hashes/test evidence remain useful; record the source release/archive provenance manually.

## QEMU / hardware
Chapter 14 QEMU smoke testing remains optional for the standard root verifier. Emulator success does not prove all physical hardware is supported.

## Reverse engineering / security scope
Do not substitute arbitrary third-party targets for course binaries unless you have explicit authorization. The course completion criteria require no unauthorized testing.

## gcc / clang / gdb / binutils missing
Run:
```bash
./scripts/install-fedora-tools.sh
./scripts/check-environment.sh
```

## Environment-specific debugging restrictions
ptrace/core/perf/virtualization can be restricted by containers or policy. Do not disable security controls at random; use an environment where debugging your own code is permitted.


## QEMU shows `elite>` but typing used to do nothing
Current Chapter 14 polls COM1 receive bytes as well as PS/2 scancodes. Use the updated kernel and run:

```bash
make -C 14-my-os clean qemu
```

With `-serial stdio -display none`, type `help` then Enter. PIT interrupts wake the halted CPU so serial input is polled.

## Static Chapter 14 test passes but QEMU test fails
That distinction is intentional. `make test` validates the kernel image; `make qemu-test` validates runtime boot milestones and requires actual PIT IRQ ticks before shell-ready.

Inspect:

```bash
cat 14-my-os/build/serial.log
```

Find the first missing `[BOOT]` marker and debug that boundary.

## GRUB rescue command has a different name
Fedora commonly provides `grub2-mkrescue`; Debian/Ubuntu commonly provides `grub-mkrescue`. The Makefile/QEMU script accepts either.

## Course CI fails quality structure before code tests
Run:

```bash
python3 scripts/check-course-quality.py
```

It checks self-study files, evidence contracts, rubrics, capstone scaffolding and local Markdown links. Fix the reported chapter rather than bypassing the gate.
