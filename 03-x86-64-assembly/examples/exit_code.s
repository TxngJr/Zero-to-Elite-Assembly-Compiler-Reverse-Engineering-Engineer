.intel_syntax noprefix
.text
.global main
.type main, @function
main:
    mov eax, 42
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
