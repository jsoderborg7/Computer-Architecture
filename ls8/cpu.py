"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Gotta have a filename")
            sys.exit(1)

        address = 0
        program = sys.argv[1]
        with open(program) as f:
            for line in f:
                line = line.strip()
                split = line.split('#')[0]
                if split == '':
                    continue
                value = int(split, 2)
                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b0000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        SP = 255

        """Run the CPU."""
        running = True
        while running:
        # set some values, make life easier
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # LDI
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            # PRN
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            # MUL
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            # PUSH
            elif IR == PUSH:
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2
            # POP
            elif IR == POP:
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.pc += 2
            # HLT
            elif IR == HLT:
                running = False
            
            else:
                self.pc = self.pc + 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value