.intel_syntax noprefix
.text
.global use_rbx_safely
.type use_rbx_safely, @function
use_rbx_safely:
    push rbx
    mov rbx, rdi
    imul rbx, rbx, 3
    lea rax, [rbx + 1]
    pop rbx
    ret
.size use_rbx_safely, .-use_rbx_safely
.section .note.GNU-stack,"",@progbits
