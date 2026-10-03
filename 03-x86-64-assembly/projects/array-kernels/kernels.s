.intel_syntax noprefix
.text
.global asm_sum_i64
.type asm_sum_i64, @function
# Preview contract for Chapter 04: rdi=array pointer, rsi=count, rax=return value.
asm_sum_i64:
    xor eax, eax
    xor ecx, ecx
.Lsum_loop:
    cmp rcx, rsi
    jae .Lsum_done
    add rax, QWORD PTR [rdi + rcx*8]
    inc rcx
    jmp .Lsum_loop
.Lsum_done:
    ret
.size asm_sum_i64, .-asm_sum_i64

.global asm_max_i64
.type asm_max_i64, @function
asm_max_i64:
    test rsi, rsi
    jz .Lmax_empty
    mov rax, QWORD PTR [rdi]
    mov rcx, 1
.Lmax_loop:
    cmp rcx, rsi
    jae .Lmax_done
    mov rdx, QWORD PTR [rdi + rcx*8]
    cmp rdx, rax
    cmovg rax, rdx
    inc rcx
    jmp .Lmax_loop
.Lmax_done:
    ret
.Lmax_empty:
    xor eax, eax
    ret
.size asm_max_i64, .-asm_max_i64

.global asm_xor_reduce_u64
.type asm_xor_reduce_u64, @function
asm_xor_reduce_u64:
    xor eax, eax
    xor ecx, ecx
.Lxor_loop:
    cmp rcx, rsi
    jae .Lxor_done
    xor rax, QWORD PTR [rdi + rcx*8]
    inc rcx
    jmp .Lxor_loop
.Lxor_done:
    ret
.size asm_xor_reduce_u64, .-asm_xor_reduce_u64
.section .note.GNU-stack,"",@progbits
