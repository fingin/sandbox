# Assembler for Leg processor

# Valid register addresses:
# 0: R0
# 1: R1
# 2: R2
# 3: R3
# 4: R4
# 5: R5
# 6: Program counter
# 7: I/O

# Valid instructions:
# 0: add
# 1: sub
# 2: and
# 3: or
# 4: not
# 5: xor

# Valid jump instructions:
# 32: if_equal
# 33: if_not_equal
# 34: if_less
# 35: if_less_or_equal
# 36: if_greater
# 37: if_greater_or_equal

# Helper function to convert decimal number to binary string with leading zeros
def decimal_to_binary(decimal, bits):
    binary = bin(decimal)[2:]
    while len(binary) < bits:
        binary = '0' + binary
    return binary

# Dictionary to map register names to their addresses
registers = {
    'R0': '0',#'00000000',
    'R1': '1',#'00000001',
    'R2': '2',#'00000010',
    'R3': '3',#'00000011',
    'R4': '4',#'00000100',
    'R5': '5',#'00000101',
    'PC': '6',#'00000110',
    'IO': '7'#'00000111'
}

# Dictionary to map instruction names to their opcodes
instructions = {
    'add': '0',#'00000000',
    'sub': '1',#'00000001',
    'and': '2',#'00000010',
    'or': '3',#'00000011',
    'not': '4',#'00000100',
    'xor': '5',#'00000101',
    'if_equal': '32',#'00100000',
    'if_not_equal': '33',#'00100001',
    'if_less': '34',#'00100010',
    'if_less_or_equal': '35',#'00100011',
    'if_greater': '36',#'00100100',
    'if_greater_or_equal': '37'#'00100101'
}

# Example assembly code
assembly = [
    'add 255 R2 R1',
    'sub 50 5 R0',
    'not R0 R1 R3',
    'add 128 0 R2',
    'add 0 0 R5',
    'if_less R0 R2 R5',


]

# Machine code generated from assembly code
machine_code = ''
for instruction in assembly:
    parts = instruction.split()
    opcode = instructions[parts[0]]
    try :
        arg1 = str(int(parts[1]))
        opcode = str(int(opcode) + 64)
    except:
        arg1 = registers[parts[1]]
    try :
        arg2 = str(int(parts[2]))
        opcode = str(int(opcode) + 128)
    except:
        arg2 = registers[parts[2]]
    arg3 = registers[parts[3]]
    print(opcode)
    print(arg1)
    print(arg2)
    print(arg3)


# Print the machine code
print(machine_code)
