.intel_syntax noprefix
.text
.global dot_i64
.type dot_i64, @function
# rdi=a, rsi=b, rdx=n -> rax=sum(a[i]*b[i])
dot_i64:
    xor eax, eax
    xor ecx, ecx
.Ldot:
    cmp rcx, rdx
    jae .Ldot_done
    mov r8, QWORD PTR [rdi + rcx*8]
    imul r8, QWORD PTR [rsi + rcx*8]
    add rax, r8
    inc rcx
    jmp .Ldot
.Ldot_done:
    ret
.size dot_i64, .-dot_i64

.global call_twice
.type call_twice, @function
# long call_twice(long (*fn)(long), long x)
call_twice:
    push rbx
    sub rsp, 16
    mov rbx, rdi
    mov QWORD PTR [rsp], rsi
    mov rdi, rsi
    call rbx
    mov QWORD PTR [rsp + 8], rax
    mov rdi, QWORD PTR [rsp]
    call rbx
    add rax, QWORD PTR [rsp + 8]
    add rsp, 16
    pop rbx
    ret
.size call_twice, .-call_twice
.section .note.GNU-stack,"",@progbits
