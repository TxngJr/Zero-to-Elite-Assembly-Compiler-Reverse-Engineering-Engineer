# Answers and Hints

- IR separates source syntax from target machine details.
- SysV integer args 1–6 use RDI, RSI, RDX, RCX, R8, R9.
- ELF sections are logical/tooling units; segments are loader mapping units.
- CR3 points at the top-level page-table physical root for the current address space.
- PMM manages physical frames, VMM manages mappings, heap manages variable-size allocations.
- COW initially shares read-only frames and copies only when a writer faults.
- Reverse engineering recovers evidence-backed behavior, not necessarily original source.
- Sanitizers/fuzzers increase evidence and test coverage but do not prove security.
- Capstone hashes identify exact generated artifacts; they do not establish trust by themselves.
