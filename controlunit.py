#!/usr/bin/env python3

from dataclasses import dataclass

IGNORED_MUX = 0

REG_DST_RD = 0
REG_DST_RT = 1
REG_DST_RA = 2

BRANCH_TYPE_NONE = 0
BRANCH_TYPE_IMM_OFF = 1
BRANCH_TYPE_REG = 2
BRANCH_TYPE_IMM_DIR = 3

BRANCH_COND_NEVER = 0
BRANCH_COND_ALWAYS = 1
BRANCH_COND_ZERO_GT = 2
BRANCH_COND_ZERO_GE = 3
BRANCH_COND_ZERO_LT = 4
BRANCH_COND_ZERO_LE = 5
BRANCH_COND_CMP_EQ = 6
BRANCH_COND_CMP_NE = 7

ALU_OP_ADD = 0
ALU_OP_SUB = 1
ALU_OP_SLT = 2
ALU_OP_SLTU = 3
ALU_OP_AND = 4
ALU_OP_OR = 5
ALU_OP_XOR = 6
ALU_OP_NOR = 7
ALU_OP_SLL = 8
ALU_OP_SRL = 9
ALU_OP_SRA = 10
ALU_OP_LUI = 11
ALU_OP_PASS_B = 12
ALU_OP_MFLO = 13
ALU_OP_MFHI = 14
ALU_OP_MTLO = 15
ALU_OP_MTHI = 16
ALU_OP_MULT = 17
ALU_OP_MULTU = 18
ALU_OP_DIV = 19
ALU_OP_DIVU = 20
ALU_OP_IGNORE = 31

ALU_B_SRC_RT = 0
ALU_B_SRC_IMM = 1
ALU_B_SRC_PC = 2

BREAK_NONE = 0
BREAK_INSTR = 1
BREAK_UNDEF = 2
BREAK_SYSCALL = 3

MEM_LEN_NONE = 3
MEM_LEN_1 = 0
MEM_LEN_2 = 1
MEM_LEN_4 = 3


@dataclass
class Instruction:
    valid: bool  # .......... num  0, 1 bit, start  0
    reg_dst_mux: int  # ..... num  1, 2 bit, start  1
    is_branch: bool  # ...... num  2, 1 bit, start  3
    branch_type_mux: int  # . num  3, 2 bit, start  4
    branch_cond_mux: int  # . num  4, 3 bit, start  6
    alu_b_src_mux: int  # ... num  5, 2 bit, start  9
    alu_op: int  # .......... num  6, 5 bit, start 11
    reg_write: bool  # ...... num  7, 1 bit, start 16
    mem_write: bool  # ...... num  8, 1 bit, start 17
    mem_to_reg: bool  # ..... num  9, 1 bit, start 18
    do_sign_ext: bool  # .... num 10, 1 bit, start 19
    break_code: int  # ...... num 11, 2 bit, start 20
    shamt_from_reg: bool  # . num 12, 1 bit, start 22
    mem_len: int  # ......... num 13, 2 bit, start 23
    mem_signext: bool  # .... num 14, 1 bit, start 25


def serialize_instr(instr: Instruction) -> int:
    result = 0
    result |= (1 if instr.valid else 0) << 0
    result |= instr.reg_dst_mux << 1
    result |= (1 if instr.is_branch else 0) << 3
    result |= instr.branch_type_mux << 4
    result |= instr.branch_cond_mux << 6
    result |= instr.alu_b_src_mux << 9
    result |= instr.alu_op << 11
    result |= (1 if instr.reg_write else 0) << 16
    result |= (1 if instr.mem_write else 0) << 17
    result |= (1 if instr.mem_to_reg else 0) << 18
    result |= (1 if instr.do_sign_ext else 0) << 19
    result |= instr.break_code << 20
    result |= (1 if instr.shamt_from_reg else 0) << 22
    result |= instr.mem_len << 23
    result |= (1 if instr.mem_signext else 0) << 25
    return result


def make_3r_alu(aluop: int, reg_shamt: bool = False) -> Instruction:
    return Instruction(True, REG_DST_RD, False, IGNORED_MUX, IGNORED_MUX,
                       ALU_B_SRC_RT, aluop, True, False, False, True,
                       BREAK_NONE, reg_shamt, MEM_LEN_NONE, False)


def make_2r_alu(aluop: int, sign_ext: bool = True) -> Instruction:
    return Instruction(True, REG_DST_RT, False, IGNORED_MUX, IGNORED_MUX,
                       ALU_B_SRC_IMM, aluop, True, False, False,
                       sign_ext, BREAK_NONE, False, MEM_LEN_NONE, False)


def make_lui() -> Instruction:
    return Instruction(True, REG_DST_RT, False, IGNORED_MUX, IGNORED_MUX,
                       ALU_B_SRC_IMM, ALU_OP_LUI, True, False, False,
                       False, BREAK_NONE, False, MEM_LEN_NONE, False)


def make_break(reason) -> Instruction:
    return Instruction(True, IGNORED_MUX, False, IGNORED_MUX, IGNORED_MUX,
                       IGNORED_MUX, ALU_OP_IGNORE, False, False, False,
                       True, reason, False, MEM_LEN_NONE, False)


def make_jr(link: bool) -> Instruction:
    return Instruction(True, REG_DST_RA, True, BRANCH_TYPE_REG,
                       BRANCH_COND_ALWAYS, ALU_B_SRC_PC,
                       ALU_OP_PASS_B, link, False, False, True,
                       BREAK_NONE, False, MEM_LEN_NONE, False)


def make_j(link: bool) -> Instruction:
    return Instruction(True, REG_DST_RA, True, BRANCH_TYPE_IMM_DIR,
                       BRANCH_COND_ALWAYS, ALU_B_SRC_PC,
                       ALU_OP_PASS_B, link, False, False, True,
                       BREAK_NONE, False, MEM_LEN_NONE, False)


def make_condjmp(cond: int, link: bool) -> Instruction:
    return Instruction(True, REG_DST_RA, True, BRANCH_TYPE_IMM_OFF,
                       cond, ALU_B_SRC_PC,
                       ALU_OP_PASS_B, link, False, False, True,
                       BREAK_NONE, False, MEM_LEN_NONE, False)


def make_lw(mlen, signext) -> Instruction:
    return Instruction(True, REG_DST_RT, False, IGNORED_MUX, IGNORED_MUX,
                       ALU_B_SRC_IMM, ALU_OP_ADD, True, False, True,
                       True, BREAK_NONE, False, mlen, signext)


def make_sw(mlen) -> Instruction:
    return Instruction(True, IGNORED_MUX, False, IGNORED_MUX, IGNORED_MUX,
                       ALU_B_SRC_IMM, ALU_OP_ADD, False, True, False,
                       True, BREAK_NONE, False, mlen, False)


def make_undef() -> Instruction:
    instr = make_break(BREAK_UNDEF)
    instr.valid = False
    return instr


RTYPE_BITS = 6
rtype_ops = {
    0b100000: make_3r_alu(ALU_OP_ADD),
    0b100001: make_3r_alu(ALU_OP_ADD),
    0b100100: make_3r_alu(ALU_OP_AND),
    0b100111: make_3r_alu(ALU_OP_NOR),
    0b100101: make_3r_alu(ALU_OP_OR),
    0b101010: make_3r_alu(ALU_OP_SLT),
    0b101011: make_3r_alu(ALU_OP_SLTU),
    0b100010: make_3r_alu(ALU_OP_SUB),
    0b100011: make_3r_alu(ALU_OP_SUB),
    0b100110: make_3r_alu(ALU_OP_XOR),
    0b000000: make_3r_alu(ALU_OP_SLL),
    0b000100: make_3r_alu(ALU_OP_SLL, True),
    0b000011: make_3r_alu(ALU_OP_SRA),
    0b000111: make_3r_alu(ALU_OP_SRA, True),
    0b000010: make_3r_alu(ALU_OP_SRL),
    0b000110: make_3r_alu(ALU_OP_SRL, True),
    0b001101: make_break(BREAK_INSTR),
    0b001001: make_jr(True),
    0b001000: make_jr(False),
    0b001100: make_break(BREAK_SYSCALL),
    0b011010: make_3r_alu(ALU_OP_DIV),
    0b011011: make_3r_alu(ALU_OP_DIVU),
    0b010000: make_3r_alu(ALU_OP_MFHI),
    0b010010: make_3r_alu(ALU_OP_MFLO),
    0b010001: make_3r_alu(ALU_OP_MTHI),
    0b010011: make_3r_alu(ALU_OP_MTLO),
    0b011000: make_3r_alu(ALU_OP_MULT),
    0b011001: make_3r_alu(ALU_OP_MULTU)
}

INSTR_BITS = 6
instrs = {
    0b000000: make_undef(),  # shadowed
    0b000001: make_undef(),  # shadowed
    0b001000: make_2r_alu(ALU_OP_ADD),
    0b001001: make_2r_alu(ALU_OP_ADD),
    0b001100: make_2r_alu(ALU_OP_AND, False),
    0b001111: make_lui(),
    0b001101: make_2r_alu(ALU_OP_OR, False),
    0b001010: make_2r_alu(ALU_OP_SLT),
    0b001011: make_2r_alu(ALU_OP_SLTU),
    0b001110: make_2r_alu(ALU_OP_XOR, False),

    0b000010: make_j(False),
    0b000011: make_j(True),

    0b000100: make_condjmp(BRANCH_COND_CMP_EQ, False),
    0b000101: make_condjmp(BRANCH_COND_CMP_NE, False),
    0b000111: make_condjmp(BRANCH_COND_ZERO_GT, False),
    0b000110: make_condjmp(BRANCH_COND_ZERO_LE, False),

    0b100000: make_lw(MEM_LEN_1, True),
    0b100100: make_lw(MEM_LEN_1, False),
    0b100001: make_lw(MEM_LEN_2, True),
    0b100101: make_lw(MEM_LEN_2, False),
    0b100011: make_lw(MEM_LEN_4, False),
    0b101000: make_sw(MEM_LEN_1),
    0b101001: make_sw(MEM_LEN_2),
    0b101011: make_sw(MEM_LEN_4),
}

JUMP_BITS = 5
jump_ugliness = {
    0b00001: make_condjmp(BRANCH_COND_ZERO_GE, False),
    0b10001: make_condjmp(BRANCH_COND_ZERO_GE, True),
    0b00000: make_condjmp(BRANCH_COND_ZERO_LT, False),
    0b10000: make_condjmp(BRANCH_COND_ZERO_LT, True),
}


def gen_rom_file(insns, bits, fp):
    print("v3.0 hex words plain", file=fp)
    for i in range(0, 2 ** bits):
        if i in insns:
            insn = insns[i]
        else:
            insn = make_undef()
        cword = serialize_instr(insn)
        print(f"{cword:06x}", file=fp)


def main():
    with open("rtype.rom", "w") as fp:
        gen_rom_file(rtype_ops, RTYPE_BITS, fp)
    with open("instrs.rom", "w") as fp:
        gen_rom_file(instrs, INSTR_BITS, fp)
    with open("jumps.rom", "w") as fp:
        gen_rom_file(jump_ugliness, JUMP_BITS, fp)


if __name__ == '__main__':
    main()
