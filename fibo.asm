// Directives to make interresting windows visible
#pragma qtmips show registers
#pragma qtmips show memory

.globl _start
.set noat
.set noreorder

.text

_start:
loop:
	addi $1, $0, 16
	addi $2, $0, 0
	addi $3, $0, 1
	addi $4, $0, 0
	lui  $6, 0xf000

fiboloop:
	sw $2, 0($4)
	sw $2, 0($6)
	add $5, $0, $3
	add $3, $3, $2
	add $2, $0, $5
	addi $4, $4, 4
	bne $1, $0, fiboloop
	addi $1, $1, -1
	break
	nop
