.intel_syntax noprefix
.text
.global main
.type main, @function
main:
    mov eax, 20
    mov ecx, 22
    cmp eax, ecx
    jl .less
    mov eax, 1
    ret
.less:
    xor eax, eax
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
