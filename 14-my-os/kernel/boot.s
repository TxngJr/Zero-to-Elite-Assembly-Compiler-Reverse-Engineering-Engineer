.intel_syntax noprefix

.section .multiboot,"a"
.align 8
header_start:
.long 0xe85250d6
.long 0
.long header_end - header_start
.long -(0xe85250d6 + 0 + (header_end - header_start))
.short 0
.short 0
.long 8
header_end:

.section .bss
.align 16
stack_bottom:
.skip 16384
stack_top:

.align 4096
pml4:
.skip 4096
pdpt:
.skip 4096
pd:
.skip 16384

boot_magic:
.long 0
boot_info:
.long 0

.section .rodata
.align 8
gdt64:
.quad 0x0000000000000000
.quad 0x00af9a000000ffff
.quad 0x00af92000000ffff
gdt64_end:
gdt64_ptr:
.word gdt64_end - gdt64 - 1
.quad gdt64

.section .text
.code32
.global _start
.type _start, @function
.extern kernel_main

_start:
    cli
    mov DWORD PTR [boot_magic], eax
    mov DWORD PTR [boot_info], ebx
    mov esp, OFFSET stack_top

    mov eax, OFFSET pdpt
    or eax, 0x3
    mov DWORD PTR [pml4], eax
    mov DWORD PTR [pml4 + 4], 0

    xor ecx, ecx
.setup_pdpt:
    mov eax, OFFSET pd
    mov edx, ecx
    shl edx, 12
    add eax, edx
    or eax, 0x3
    mov DWORD PTR [pdpt + ecx*8], eax
    mov DWORD PTR [pdpt + ecx*8 + 4], 0
    inc ecx
    cmp ecx, 4
    jne .setup_pdpt

    xor ecx, ecx
.map_pd:
    mov eax, ecx
    shl eax, 21
    or eax, 0x83
    mov DWORD PTR [pd + ecx*8], eax
    mov DWORD PTR [pd + ecx*8 + 4], 0
    inc ecx
    cmp ecx, 2048
    jne .map_pd

    mov eax, cr4
    or eax, 1 << 5
    mov cr4, eax

    mov eax, OFFSET pml4
    mov cr3, eax

    mov ecx, 0xC0000080
    rdmsr
    or eax, 1 << 8
    wrmsr

    mov eax, cr0
    or eax, 1 << 31
    mov cr0, eax

    lgdt [gdt64_ptr]

    .byte 0xEA
    .long long_mode_start
    .word 0x08

.code64
long_mode_start:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov fs, ax
    mov gs, ax

    mov rsp, OFFSET stack_top
    xor rbp, rbp

    mov edi, DWORD PTR [boot_magic]
    mov esi, DWORD PTR [boot_info]
    call kernel_main

.hang:
    cli
    hlt
    jmp .hang

.size _start, .-_start
.section .note.GNU-stack,"",@progbits
