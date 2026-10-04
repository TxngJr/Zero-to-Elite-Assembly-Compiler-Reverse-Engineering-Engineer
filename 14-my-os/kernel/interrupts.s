.intel_syntax noprefix

.section .bss
.align 8
.global timer_ticks
timer_ticks:
.quad 0

.global last_scancode
last_scancode:
.byte 0

.section .text
.code64

.extern exception_panic

.global isr_default
.type isr_default, @function
isr_default:
    cli
1:
    hlt
    jmp 1b
.size isr_default, .-isr_default

/*
 * Normalized exception frame passed to exception_common:
 *   [rsp + 0]  vector
 *   [rsp + 8]  error code (synthetic zero for exceptions without one)
 *   [rsp + 16] RIP pushed by hardware
 *
 * The panic handler never returns, so exception_common may realign RSP
 * destructively before entering C.
 */
.macro EXC_NOERR name, vector
.global \name
.type \name, @function
\name:
    push 0
    push \vector
    jmp exception_common
.size \name, .-\name
.endm

.macro EXC_ERR name, vector
.global \name
.type \name, @function
\name:
    push \vector
    jmp exception_common
.size \name, .-\name
.endm

EXC_NOERR exception_de_stub, 0
EXC_NOERR exception_ud_stub, 6
EXC_ERR   exception_gp_stub, 13
EXC_ERR   exception_pf_stub, 14

.type exception_common, @function
exception_common:
    mov rdi, QWORD PTR [rsp]
    mov rsi, QWORD PTR [rsp + 8]
    mov rdx, QWORD PTR [rsp + 16]
    and rsp, -16
    call exception_panic
    ud2
.size exception_common, .-exception_common

.global irq0_stub
.type irq0_stub, @function
irq0_stub:
    push rax
    inc QWORD PTR [rip + timer_ticks]
    mov al, 0x20
    out 0x20, al
    pop rax
    iretq
.size irq0_stub, .-irq0_stub

.global irq1_stub
.type irq1_stub, @function
irq1_stub:
    push rax
    in al, 0x60
    mov BYTE PTR [rip + last_scancode], al
    mov al, 0x20
    out 0x20, al
    pop rax
    iretq
.size irq1_stub, .-irq1_stub

.section .note.GNU-stack,"",@progbits
