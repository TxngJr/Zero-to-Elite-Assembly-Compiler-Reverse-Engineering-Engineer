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

.global isr_default
.type isr_default, @function
isr_default:
    cli
1:
    hlt
    jmp 1b
.size isr_default, .-isr_default

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
