# Troubleshooting

## Chapter 15 simulator differs from real kernel behavior
Expected. Chapter 15 projects model algorithms in user-space so they can be tested deterministically. They do not claim to implement privileged context switching, TSS, CR3 changes or real filesystem drivers.

## vm-cow-sim reports missing page
The simulator only translates pages explicitly mapped with `map_zero`. Check page alignment and virtual page number.

## Challenge-suite build fails on `-no-pie`
Course targets Fedora/Linux x86-64 GCC/Clang. Confirm compiler driver supports the Linux option and that you are not using a non-Linux target.

## `strip` not found
`strip` comes from GNU binutils, installed as a required course package.

## binary-report fails on a random third-party file
The tool is intended for authorized/course ELF binaries. Confirm the target is an ELF file and that `file/readelf/nm/strings` are installed.

## cfg-extract misses an indirect branch
Expected. It is a small text parser over objdump output, not a full recursive-descent disassembler. Indirect jump/call resolution is intentionally an advanced challenge.

## PIE address in GDB differs from objdump
Runtime PIE has a load base. Use `info proc mappings` and image-relative offsets rather than comparing absolute addresses directly.

## Parser lab rejects oversized packet
That is the fixed behavior. The default build checks both destination capacity and available input bytes.

## sanitizer-demo exits non-zero
Expected. `make sanitizer-demo` intentionally builds the compile-time injected defect and expects ASan/UBSan to terminate/report it. It is a local course demonstration only.

## ASan is unavailable
GCC/Clang Fedora packages normally provide sanitizer runtimes. Base `make test` does not require running the buggy sanitizer demo; `make sanitize` does require sanitizer support.

## Fuzzing finds no crash
A clean deterministic smoke run is not proof of security. Increase corpus quality/coverage tooling in authorized local work, then keep discovered cases as regression tests.

## Security report severity feels uncertain
Do not infer severity from bug class alone. State reachability, attacker control, privileges and demonstrated impact, and mark uncertainty explicitly.

## gcc / clang / gdb / binutils missing
Run `./scripts/install-fedora-tools.sh` then `./scripts/check-environment.sh`.

## Kernel / QEMU issues
See Chapter 14 README and inspect Multiboot header, ELF entry, page tables and serial checkpoints before changing several subsystems at once.
