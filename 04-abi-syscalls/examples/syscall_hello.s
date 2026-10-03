.intel_syntax noprefix
.section .rodata
msg: .ascii "hello via Linux syscall\n"
.set msg_len, . - msg
.text
.global _start
.type _start, @function
_start:
    mov eax, 1              # SYS_write
    mov edi, 1              # stdout
    lea rsi, msg[rip]
    mov edx, OFFSET msg_len
    syscall

    mov eax, 60             # SYS_exit
    xor edi, edi
    syscall
.size _start, .-_start
.section .note.GNU-stack,"",@progbits
