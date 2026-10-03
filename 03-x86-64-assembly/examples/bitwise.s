.intel_syntax noprefix
.text
.global main
.type main, @function
main:
    mov eax, 0b10110000
    and eax, 0b11110000
    or  eax, 0b00000101
    xor eax, 0b00100000
    shl eax, 1
    shr eax, 1
    sub eax, 0x95
    ret
.size main, .-main
.section .note.GNU-stack,"",@progbits
