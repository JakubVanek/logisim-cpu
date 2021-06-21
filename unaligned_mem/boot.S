# Logisim CPU startup routine

.extern main
.extern __data_start
.extern __data_end
.extern __data_loadaddr
.extern __bss_start
.extern __bss_end
.extern __stack_end

.text
.set noreorder
.globl _start
.ent   _start
_start:

/* signal boot */
    la $s0, 0xf0000000
    li $t0, -1
    sw $t0, 0($s0)

/* register init */
    la $sp, __stack_end
    la $gp, _gp
    move $fp, $sp


/* bss initialization */
    la $t0, __bss_start
    la $t1, __bss_end
    beq $t0, $t1, zeroloop_skip
    nop
    zeroloop:
    sw $zero, 0($t0)
    bne $t0, $t1, zeroloop
    addi $t0, $t0, 4
    zeroloop_skip:

/* data initialization */
    la $t0, __data_start
    la $t1, __data_end
    la $t2, __data_loadaddr
    beq $t0, $t1, copyloop_skip
    nop
    copyloop:
    lw $t3, 0($t2)
    sw $t3, 0($t0)
    addi $t2, $t2, 4
    bne $t0, $t1, copyloop
    addi $t0, $t0, 4
    copyloop_skip:

/* jump to main */
    li $a0, 0
    li $a1, 0
    sw $a0, 0($s0)
    jal main
    nop

    endloop:
    break
    beq $zero, $zero, endloop
    nop

.end   _start
