ENTRY(_start)

SECTIONS
{
  . = 1M;

  .multiboot : {
    KEEP(*(.multiboot))
  }

  . = ALIGN(4K);
  .text : {
    *(.text .text.*)
  }

  . = ALIGN(4K);
  .rodata : {
    *(.rodata .rodata.*)
  }

  . = ALIGN(4K);
  .data : {
    *(.data .data.*)
  }

  . = ALIGN(4K);
  .bss : {
    *(COMMON)
    *(.bss .bss.*)
  }

  kernel_end = .;

  /DISCARD/ : {
    *(.comment)
    *(.eh_frame .eh_frame.*)
    *(.note*)
  }
}
