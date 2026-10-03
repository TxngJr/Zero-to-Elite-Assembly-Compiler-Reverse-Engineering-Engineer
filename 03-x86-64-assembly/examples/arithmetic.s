.intel_syntax noprefix
.text
.global main
.type main, @function
main:
    mov eax, 10
    add eax, 7
    imul eax, eax, 3
    sub eax, 1
    # (10 + 7) * 3 - 1 = 50; return low 8 bits as process status.
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
