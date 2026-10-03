.intel_syntax noprefix
.section .data
.align 16
values:
    .long 10, 20, 30, 40
.text
.global main
.type main, @function
main:
    lea rdx, values[rip]
    mov ecx, 2
    mov eax, DWORD PTR [rdx + rcx*4]
    sub eax, 30
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
