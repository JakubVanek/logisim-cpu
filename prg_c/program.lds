/* inspired by https://interrupt.memfault.com/blog/how-to-write-linker-scripts-for-firmware */
/* also from https://github.com/payne92/bare-metal-arm/blob/master/mkl25z4.ld */
/* also from https://github.com/wntrblm/Castor_and_Pollux/blob/main/firmware/scripts/samd21g18a.ld */
/* also from GCC linker scripts */

OUTPUT_FORMAT("elf32-littlemips", "elf32-bigmips", "elf32-littlemips")
OUTPUT_ARCH(mips)
ENTRY(_start)

MEMORY
{
    rom  (rx) : ORIGIN = 0x80020000, LENGTH =  64K
    ram  (rw) : ORIGIN = 0x00000000, LENGTH = 128K
}

STACK_SIZE = 8K;

SECTIONS
{
    .text :
    {
        boot.o(*)

        *(.text .text.* .stub .gnu.linkonce.t.*)
        *(.rodata .rodata.* .gnu.linkonce.r.*)
        *(.rodata1)
    } >rom

    .data :
    {
        . = ALIGN(4);
        __data_start = .;
        *(.data .data.* .gnu.linkonce.d.*)
        SORT(CONSTRUCTORS)
        *(.data1)

        . = .;
        _gp = ALIGN (16) + 0x7ff0;
        *(.sdata .sdata.* .gnu.linkonce.s.*)
        *(.lit8)
        *(.lit4)
        . = ALIGN(4);
        __data_end = .;
    } >ram AT >rom

    __data_loadaddr = LOADADDR(.data);

    .bss (NOLOAD) :
    {
        . = ALIGN(4);
        __bss_start = .;
        *(.dynsbss)
        *(.sbss .sbss.* .gnu.linkonce.sb.*)
        *(.scommon)
        *(.dynbss)
        *(.bss .bss.* .gnu.linkonce.b.*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } >ram

    .stack (NOLOAD) :
    {
        . = ALIGN(4);
        __stack_start = .;
        . += STACK_SIZE;
        . = ALIGN(4);
        __stack_end = .;
    } > ram

    . = ALIGN(4);
    __heap_start = .;
}
