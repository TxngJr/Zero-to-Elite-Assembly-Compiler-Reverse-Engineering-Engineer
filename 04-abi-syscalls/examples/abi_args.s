.intel_syntax noprefix
.text
.global sum_six
.type sum_six, @function
sum_six:
    lea rax, [rdi + rsi]
    add rax, rdx
    add rax, rcx
    add rax, r8
    add rax, r9
    ret
.size sum_six, .-sum_six

.global sum_eight
.type sum_eight, @function
sum_eight:
    lea rax, [rdi + rsi]
    add rax, rdx
    add rax, rcx
    add rax, r8
    add rax, r9
    add rax, QWORD PTR [rsp + 8]
    add rax, QWORD PTR [rsp + 16]
    ret
.size sum_eight, .-sum_eight
.section .note.GNU-stack,"",@progbits
