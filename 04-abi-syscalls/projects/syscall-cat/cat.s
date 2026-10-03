.intel_syntax noprefix
.equ SYS_read, 0
.equ SYS_write, 1
.equ SYS_close, 3
.equ SYS_exit, 60
.equ SYS_openat, 257
.equ AT_FDCWD, -100
.equ O_RDONLY, 0
.equ BUF_SIZE, 4096
.bss
.align 16
buffer: .skip BUF_SIZE
.text
.global _start
.type _start, @function
_start:
    mov r12, QWORD PTR [rsp]       # argc
    cmp r12, 2
    jne .usage
    mov r13, QWORD PTR [rsp + 16]  # argv[1]

    mov eax, SYS_openat
    mov edi, AT_FDCWD
    mov rsi, r13
    mov edx, O_RDONLY
    xor r10d, r10d
    syscall
    test rax, rax
    js .open_fail
    mov r12, rax                   # fd

.read_loop:
    mov eax, SYS_read
    mov rdi, r12
    lea rsi, buffer[rip]
    mov edx, BUF_SIZE
    syscall
    test rax, rax
    js .io_fail
    jz .done
    mov r13, rax                   # bytes remaining
    lea r14, buffer[rip]
.write_loop:
    mov eax, SYS_write
    mov edi, 1
    mov rsi, r14
    mov rdx, r13
    syscall
    test rax, rax
    jle .io_fail
    add r14, rax
    sub r13, rax
    jne .write_loop
    jmp .read_loop

.done:
    mov eax, SYS_close
    mov rdi, r12
    syscall
    xor edi, edi
    jmp .exit

.usage:
    mov edi, 2
    jmp .exit
.open_fail:
    mov edi, 3
    jmp .exit
.io_fail:
    mov edi, 4
.exit:
    mov eax, SYS_exit
    syscall
.size _start, .-_start
.section .note.GNU-stack,"",@progbits
