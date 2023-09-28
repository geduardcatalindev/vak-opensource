#!/usr/bin/env python3
#
# Generate assembly code for testing conditional branch instructions.
#

label_count = 0
def get_label():
    global label_count
    label_count += 1
    return label_count

#
# Generate one branch instruction.
#
def gen_branch(suffix, jump_flag):
    if jump_flag:
        # This instruction will jump.
        label = get_label()
        print(f"    b{suffix} {label}f")
        print(f"    b fail")
        print(f"{label}:")
    else:
        # No jump.
        print(f"    b{suffix} fail")

#
# Iterate all branch instructions.
#
# cond Mnemonic   Meaning                         Condition flags
# ---------------------------------------------------------------
# 0000 EQ         Equal                           Z==1
# 0001 NE         Not equal                       Z==0
# 0010 CS         Carry set                       C==1
# 0011 CC         Carry clear                     C==0
# 0100 MI         Minus, negative                 N==1
# 0101 PL         Plus, positive or zero          N==0
# 0110 VS         Overflow                        V==1
# 0111 VC         No overflow                     V==0
# 1000 HI         Unsigned higher                 C==1 and Z==0
# 1001 LS         Unsigned lower or same          C==0 or Z==1
# 1010 GE         Signed greater than or equal    N==V
# 1011 LT         Signed less than                N!=V
# 1100 GT         Signed greater than             Z==0 and N==V
# 1101 LE         Signed less than or equal       Z==1 or N!=V
#
def gen_cond(cond):
    n = (cond >> 3) & 1
    z = (cond >> 2) & 1
    c = (cond >> 1) & 1
    v = (cond >> 0) & 1

    print("")
    print(f"    // Condition codes: N={n} Z={z} C={c} V={v}")
    print(f"    ldr X1, =0x{cond:x}0000000")
    print("    msr NZCV, X1")

    gen_branch("eq", z == 1)
    gen_branch("ne", z == 0)
    gen_branch("cs", c == 1)
    gen_branch("cc", c == 0)
    gen_branch("mi", n == 1)
    gen_branch("pl", n == 0)
    gen_branch("vs", v == 1)
    gen_branch("vc", v == 0)
    gen_branch("hi", c == 1 and z == 0)
    gen_branch("ls", c == 0 or z == 1)
    gen_branch("ge", n == v)
    gen_branch("lt", n != v)
    gen_branch("gt", z == 0 and n == v)
    gen_branch("le", z == 1 or n != v)

print("    .text")
print("    .align  2           // Make sure everything is aligned properly")
print("    .global _start")
print("_start:")

#
# Iterate all conbinations of condition codes.
#
for cond in range(0, 16):
    gen_cond(cond)

#
# Print "Test passed"
#
print("    mov X0, #1          // Print to StdOut")
print("    adr X1, passed      // Put address of text message into register X1")
print("    mov X2, #12         // Length of our string")
print("    mov X16, #4         // Unix write() system call")
print("    svc #0x80           // Call kernel to output the string")
print("    mov X0, #0          // Exit code")
print("    mov X16, #1         // Unix _exit() system call")
print("    svc #0x80           // Call kernel to terminate the program")
print("passed:")
print("    .ascii \"Test passed\\n\"")

#
# Print "Test failed"
#
print("fail:")
print("    mov X0, #1          // Print to StdOut")
print("    adr X1, failed      // Put address of text message into register X1")
print("    mov X2, #12         // Length of our string")
print("    mov X16, #4         // Unix write() system call")
print("    svc #0x80           // Call kernel to output the string")
print("    mov X0, #255        // Exit code")
print("    mov X16, #1         // Unix _exit() system call")
print("    svc #0x80           // Call kernel to terminate the program")
print("failed:")
print("    .ascii \"Test failed\\n\"")
