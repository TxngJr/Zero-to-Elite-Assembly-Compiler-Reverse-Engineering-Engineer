# Troubleshooting

## Python compiler imports fail
Run tools inside the repository layout. Chapter 10 imports the frontend snapshot from Chapter 09; Chapter 11 imports both earlier stages using repository-relative paths.

## Unexpected character
Check the byte position and EliteLang grammar. Current identifiers/operators are intentionally small and `//` comments are supported.

## duplicate/shadowed variable
The course frontend intentionally forbids active-name shadowing. Full scoped shadowing is a Chapter 09 challenge.

## function does not return on all obvious paths
Return analysis is intentionally conservative. Return in both `if/else` arms or add an explicit return.

## `--ssa` is not full SSA
Correct: Chapter 10 implements educational phi-candidate analysis. Full dominance-frontier placement + renaming is a challenge/Chapter 12 integration item.

## optimizer does not fold across blocks
The implemented pass is local constant propagation/folding. Global propagation requires CFG data-flow facts and side-effect/trap handling.

## generated assembly links but runtime is wrong
Inspect `objdump -d -Mintel`, stack alignment, argument mapping and Chapter 04 SysV ABI rules.

## calls with more than 6 args are wrong
Check reverse stack-argument push order, 16-byte padding, and callee offsets starting at `[rbp+16]`.

## division traps
EliteLang `/` and `%` use signed `idiv`. Division by zero is a runtime trap. The short-circuit test deliberately proves a dangerous RHS is skipped.

## exit status differs from a large return value
Process exit status is limited. Use small values in status-based tests or add an interpreter/runtime output path for larger values.

## pipefail + objdump/grep returns 141
A consumer may exit early and cause SIGPIPE. The backend test writes disassembly to a file before grep.

## Tool missing
Run `./scripts/install-fedora-tools.sh` and `./scripts/check-environment.sh`.
