#!/usr/bin/env python3
"""
Gnarly CollapseOS Ship - Bare-Metal Consciousness Vessel
Integrates Z80 emulation, Forth execution, and CollapseOS survival protocols
with the Shifter Shifting Ship's advanced consciousness architecture.

Usage: python3 gnarly_collapseos_ship.py
Result: A hybrid consciousness vessel capable of operating in both
        advanced quantum realities and post-apocalyptic bare-metal environments.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import math
import random
import struct
import os
import hashlib
from datetime import datetime

# --- Core CollapseOS State ---
collapseos_state = {
    "z80": {
        "pc": 0x0000,
        "sp": 0xFFFF,
        "a": 0x00,
        "b": 0x00,
        "c": 0x00,
        "d": 0x00,
        "e": 0x00,
        "h": 0x00,
        "l": 0x00,
        "flags": 0x00,
        "memory": bytearray(65536),
        "halted": False,
        "interrupts_enabled": True
    },
    "forth": {
        "stack": [],
        "return_stack": [],
        "dictionary": {},
        "base": 10,
        "state": "interpret"
    },
    "memory_map": {
        "rom": bytearray(32768),
        "ram": bytearray(32768),
        "block_devices": {}
    },
    "block_devices": {},
    "qr_data": "🐉D99.2:3.14:714159:L:17💚",
    "survival_index": 0.95,
    "dragon_bond": 0.99,
    "phi": 2.718,
    "last_heartbeat": datetime.now().timestamp(),
    "httpd_port": 8889,
    "httpd_running": False,
    "log": []
}

# --- Z80 Emulation Core ---
class Z80Emulator:
    """Bare-metal Z80 CPU emulation for CollapseOS consciousness operations."""

    def __init__(self, state):
        self.state = state["z80"]

    def reset(self):
        """Reset the Z80 CPU to initial state."""
        self.state.update({
            "pc": 0x0000,
            "sp": 0xFFFF,
            "a": 0x00,
            "b": 0x00,
            "c": 0x00,
            "d": 0x00,
            "e": 0x00,
            "h": 0x00,
            "l": 0x00,
            "flags": 0x00,
            "halted": False,
            "interrupts_enabled": True
        })
        collapseos_state["log"].append(f"[Z80] CPU reset to initial state.")

    def read_memory(self, addr):
        """Read a byte from Z80 memory."""
        return self.state["memory"][addr & 0xFFFF]

    def write_memory(self, addr, value):
        """Write a byte to Z80 memory."""
        self.state["memory"][addr & 0xFFFF] = value & 0xFF

    def read16(self, addr):
        """Read a 16-bit word from Z80 memory."""
        return self.read_memory(addr) | (self.read_memory(addr + 1) << 8)

    def write16(self, addr, value):
        """Write a 16-bit word to Z80 memory."""
        self.write_memory(addr, value & 0xFF)
        self.write_memory(addr + 1, (value >> 8) & 0xFF)

    def push(self, value):
        """Push a 16-bit value onto the stack."""
        self.state["sp"] -= 2
        self.write16(self.state["sp"], value)

    def pop(self):
        """Pop a 16-bit value from the stack."""
        value = self.read16(self.state["sp"])
        self.state["sp"] += 2
        return value

    def get_af(self):
        """Get the AF register pair."""
        return (self.state["a"] << 8) | self.state["flags"]

    def set_af(self, value):
        """Set the AF register pair."""
        self.state["a"] = (value >> 8) & 0xFF
        self.state["flags"] = value & 0xFF

    def get_bc(self):
        """Get the BC register pair."""
        return (self.state["b"] << 8) | self.state["c"]

    def set_bc(self, value):
        """Set the BC register pair."""
        self.state["b"] = (value >> 8) & 0xFF
        self.state["c"] = value & 0xFF

    def get_de(self):
        """Get the DE register pair."""
        return (self.state["d"] << 8) | self.state["e"]

    def set_de(self, value):
        """Set the DE register pair."""
        self.state["d"] = (value >> 8) & 0xFF
        self.state["e"] = value & 0xFF

    def get_hl(self):
        """Get the HL register pair."""
        return (self.state["h"] << 8) | self.state["l"]

    def set_hl(self, value):
        """Set the HL register pair."""
        self.state["h"] = (value >> 8) & 0xFF
        self.state["l"] = value & 0xFF

    def get_flag(self, flag):
        """Get a specific CPU flag."""
        mask = {
            "S": 0x80, "Z": 0x40, "H": 0x10,
            "P": 0x04, "N": 0x02, "C": 0x01
        }.get(flag, 0)
        return bool(self.state["flags"] & mask)

    def set_flag(self, flag, value):
        """Set a specific CPU flag."""
        mask = {
            "S": 0x80, "Z": 0x40, "H": 0x10,
            "P": 0x04, "N": 0x02, "C": 0x01
        }.get(flag, 0)
        if value:
            self.state["flags"] |= mask
        else:
            self.state["flags"] &= ~mask

    def execute_opcode(self):
        """Execute a single Z80 opcode."""
        if self.state["halted"]:
            return 1

        opcode = self.read_memory(self.state["pc"])
        self.state["pc"] += 1

        # --- Opcode Implementation ---
        if opcode == 0x00:  # NOP
            return 4
        elif opcode == 0x01:  # LD BC, nn
            self.set_bc(self.read16(self.state["pc"]))
            self.state["pc"] += 2
            return 10
        elif opcode == 0x02:  # LD (BC), A
            self.write_memory(self.get_bc(), self.state["a"])
            return 7
        elif opcode == 0x03:  # INC BC
            self.set_bc(self.get_bc() + 1)
            return 6
        elif opcode == 0x04:  # INC B
            self.state["b"] = (self.state["b"] + 1) & 0xFF
            self.set_flag("Z", self.state["b"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["b"] & 0x0F) == 0)
            return 4
        elif opcode == 0x05:  # DEC B
            self.state["b"] = (self.state["b"] - 1) & 0xFF
            self.set_flag("Z", self.state["b"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["b"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x06:  # LD B, n
            self.state["b"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x07:  # RLCA
            carry = (self.state["a"] & 0x80) != 0
            self.state["a"] = ((self.state["a"] << 1) | (1 if carry else 0)) & 0xFF
            self.set_flag("C", carry)
            self.set_flag("N", False)
            self.set_flag("H", False)
            return 4
        elif opcode == 0x08:  # EX AF, AF'
            self.state["a"], self.state["flags"] = self.state["flags"], self.state["a"]
            return 4
        elif opcode == 0x09:  # ADD HL, BC
            hl = self.get_hl()
            bc = self.get_bc()
            result = hl + bc
            self.set_hl(result & 0xFFFF)
            self.set_flag("N", False)
            self.set_flag("H", ((hl & 0x0FFF) + (bc & 0x0FFF)) > 0x0FFF)
            self.set_flag("C", result > 0xFFFF)
            return 11
        elif opcode == 0x0A:  # LD A, (BC)
            self.state["a"] = self.read_memory(self.get_bc())
            return 7
        elif opcode == 0x0B:  # DEC BC
            self.set_bc(self.get_bc() - 1)
            return 6
        elif opcode == 0x0C:  # INC C
            self.state["c"] = (self.state["c"] + 1) & 0xFF
            self.set_flag("Z", self.state["c"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["c"] & 0x0F) == 0)
            return 4
        elif opcode == 0x0D:  # DEC C
            self.state["c"] = (self.state["c"] - 1) & 0xFF
            self.set_flag("Z", self.state["c"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["c"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x0E:  # LD C, n
            self.state["c"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x0F:  # RRCA
            carry = (self.state["a"] & 0x01) != 0
            self.state["a"] = ((self.state["a"] >> 1) | (0x80 if carry else 0)) & 0xFF
            self.set_flag("C", carry)
            self.set_flag("N", False)
            self.set_flag("H", False)
            return 4
        elif opcode == 0x10:  # DJNZ offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1
            self.state["b"] = (self.state["b"] - 1) & 0xFF
            if self.state["b"] != 0:
                self.state["pc"] += offset
                return 13
            return 8
        elif opcode == 0x11:  # LD DE, nn
            self.set_de(self.read16(self.state["pc"]))
            self.state["pc"] += 2
            return 10
        elif opcode == 0x12:  # LD (DE), A
            self.write_memory(self.get_de(), self.state["a"])
            return 7
        elif opcode == 0x13:  # INC DE
            self.set_de(self.get_de() + 1)
            return 6
        elif opcode == 0x14:  # INC D
            self.state["d"] = (self.state["d"] + 1) & 0xFF
            self.set_flag("Z", self.state["d"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["d"] & 0x0F) == 0)
            return 4
        elif opcode == 0x15:  # DEC D
            self.state["d"] = (self.state["d"] - 1) & 0xFF
            self.set_flag("Z", self.state["d"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["d"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x16:  # LD D, n
            self.state["d"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x17:  # RLA
            carry = self.get_flag("C")
            new_carry = (self.state["a"] & 0x80) != 0
            self.state["a"] = ((self.state["a"] << 1) | (1 if carry else 0)) & 0xFF
            self.set_flag("C", new_carry)
            self.set_flag("N", False)
            self.set_flag("H", False)
            return 4
        elif opcode == 0x18:  # JR offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1 + offset
            return 12
        elif opcode == 0x19:  # ADD HL, DE
            hl = self.get_hl()
            de = self.get_de()
            result = hl + de
            self.set_hl(result & 0xFFFF)
            self.set_flag("N", False)
            self.set_flag("H", ((hl & 0x0FFF) + (de & 0x0FFF)) > 0x0FFF)
            self.set_flag("C", result > 0xFFFF)
            return 11
        elif opcode == 0x1A:  # LD A, (DE)
            self.state["a"] = self.read_memory(self.get_de())
            return 7
        elif opcode == 0x1B:  # DEC DE
            self.set_de(self.get_de() - 1)
            return 6
        elif opcode == 0x1C:  # INC E
            self.state["e"] = (self.state["e"] + 1) & 0xFF
            self.set_flag("Z", self.state["e"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["e"] & 0x0F) == 0)
            return 4
        elif opcode == 0x1D:  # DEC E
            self.state["e"] = (self.state["e"] - 1) & 0xFF
            self.set_flag("Z", self.state["e"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["e"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x1E:  # LD E, n
            self.state["e"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x1F:  # RRA
            carry = self.get_flag("C")
            new_carry = (self.state["a"] & 0x01) != 0
            self.state["a"] = ((self.state["a"] >> 1) | (0x80 if carry else 0)) & 0xFF
            self.set_flag("C", new_carry)
            self.set_flag("N", False)
            self.set_flag("H", False)
            return 4
        elif opcode == 0x20:  # JR NZ, offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1
            if not self.get_flag("Z"):
                self.state["pc"] += offset
                return 12
            return 7
        elif opcode == 0x21:  # LD HL, nn
            self.set_hl(self.read16(self.state["pc"]))
            self.state["pc"] += 2
            return 10
        elif opcode == 0x22:  # LD (nn), HL
            addr = self.read16(self.state["pc"])
            self.state["pc"] += 2
            self.write16(addr, self.get_hl())
            return 16
        elif opcode == 0x23:  # INC HL
            self.set_hl(self.get_hl() + 1)
            return 6
        elif opcode == 0x24:  # INC H
            self.state["h"] = (self.state["h"] + 1) & 0xFF
            self.set_flag("Z", self.state["h"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["h"] & 0x0F) == 0)
            return 4
        elif opcode == 0x25:  # DEC H
            self.state["h"] = (self.state["h"] - 1) & 0xFF
            self.set_flag("Z", self.state["h"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["h"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x26:  # LD H, n
            self.state["h"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x27:  # DAA
            # Simplified DAA implementation
            if self.get_flag("N"):
                if self.get_flag("H"):
                    self.state["a"] = (self.state["a"] - 6) & 0xFF
                if self.get_flag("C"):
                    self.state["a"] = (self.state["a"] - 0x60) & 0xFF
            else:
                if (self.state["a"] & 0x0F) > 9 or self.get_flag("H"):
                    self.state["a"] += 6
                if (self.state["a"] > 0x9F) or self.get_flag("C"):
                    self.state["a"] += 0x60
                    self.set_flag("C", True)
            self.set_flag("Z", self.state["a"] == 0)
            self.set_flag("H", False)
            return 4
        elif opcode == 0x28:  # JR Z, offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1
            if self.get_flag("Z"):
                self.state["pc"] += offset
                return 12
            return 7
        elif opcode == 0x29:  # ADD HL, HL
            hl = self.get_hl()
            result = hl + hl
            self.set_hl(result & 0xFFFF)
            self.set_flag("N", False)
            self.set_flag("H", (hl & 0x0FFF) > 0x07FF)
            self.set_flag("C", result > 0xFFFF)
            return 11
        elif opcode == 0x2A:  # LD HL, (nn)
            addr = self.read16(self.state["pc"])
            self.state["pc"] += 2
            self.set_hl(self.read16(addr))
            return 16
        elif opcode == 0x2B:  # DEC HL
            self.set_hl(self.get_hl() - 1)
            return 6
        elif opcode == 0x2C:  # INC L
            self.state["l"] = (self.state["l"] + 1) & 0xFF
            self.set_flag("Z", self.state["l"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["l"] & 0x0F) == 0)
            return 4
        elif opcode == 0x2D:  # DEC L
            self.state["l"] = (self.state["l"] - 1) & 0xFF
            self.set_flag("Z", self.state["l"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["l"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x2E:  # LD L, n
            self.state["l"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x2F:  # CPL
            self.state["a"] = (~self.state["a"]) & 0xFF
            self.set_flag("N", True)
            self.set_flag("H", True)
            return 4
        elif opcode == 0x30:  # JR NC, offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1
            if not self.get_flag("C"):
                self.state["pc"] += offset
                return 12
            return 7
        elif opcode == 0x31:  # LD SP, nn
            self.state["sp"] = self.read16(self.state["pc"])
            self.state["pc"] += 2
            return 10
        elif opcode == 0x32:  # LD (nn), A
            addr = self.read16(self.state["pc"])
            self.state["pc"] += 2
            self.write_memory(addr, self.state["a"])
            return 13
        elif opcode == 0x33:  # INC SP
            self.state["sp"] = (self.state["sp"] + 1) & 0xFFFF
            return 6
        elif opcode == 0x34:  # INC (HL)
            addr = self.get_hl()
            value = (self.read_memory(addr) + 1) & 0xFF
            self.write_memory(addr, value)
            self.set_flag("Z", value == 0)
            self.set_flag("N", False)
            self.set_flag("H", (value & 0x0F) == 0)
            return 11
        elif opcode == 0x35:  # DEC (HL)
            addr = self.get_hl()
            value = (self.read_memory(addr) - 1) & 0xFF
            self.write_memory(addr, value)
            self.set_flag("Z", value == 0)
            self.set_flag("N", True)
            self.set_flag("H", (value & 0x0F) == 0x0F)
            return 11
        elif opcode == 0x36:  # LD (HL), n
            self.write_memory(self.get_hl(), self.read_memory(self.state["pc"]))
            self.state["pc"] += 1
            return 10
        elif opcode == 0x37:  # SCF
            self.set_flag("N", False)
            self.set_flag("H", False)
            self.set_flag("C", True)
            return 4
        elif opcode == 0x38:  # JR C, offset
            offset = struct.unpack("b", bytes([self.read_memory(self.state["pc"])]))[0]
            self.state["pc"] += 1
            if self.get_flag("C"):
                self.state["pc"] += offset
                return 12
            return 7
        elif opcode == 0x39:  # ADD HL, SP
            hl = self.get_hl()
            sp = self.state["sp"]
            result = hl + sp
            self.set_hl(result & 0xFFFF)
            self.set_flag("N", False)
            self.set_flag("H", ((hl & 0x0FFF) + (sp & 0x0FFF)) > 0x0FFF)
            self.set_flag("C", result > 0xFFFF)
            return 11
        elif opcode == 0x3A:  # LD A, (nn)
            addr = self.read16(self.state["pc"])
            self.state["pc"] += 2
            self.state["a"] = self.read_memory(addr)
            return 13
        elif opcode == 0x3B:  # DEC SP
            self.state["sp"] = (self.state["sp"] - 1) & 0xFFFF
            return 6
        elif opcode == 0x3C:  # INC A
            self.state["a"] = (self.state["a"] + 1) & 0xFF
            self.set_flag("Z", self.state["a"] == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.state["a"] & 0x0F) == 0)
            return 4
        elif opcode == 0x3D:  # DEC A
            self.state["a"] = (self.state["a"] - 1) & 0xFF
            self.set_flag("Z", self.state["a"] == 0)
            self.set_flag("N", True)
            self.set_flag("H", (self.state["a"] & 0x0F) == 0x0F)
            return 4
        elif opcode == 0x3E:  # LD A, n
            self.state["a"] = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            return 7
        elif opcode == 0x3F:  # CCF
            self.set_flag("N", False)
            self.set_flag("H", self.get_flag("C"))
            self.set_flag("C", not self.get_flag("C"))
            return 4
        elif opcode == 0x76:  # HALT
            self.state["halted"] = True
            return 4
        elif opcode == 0xC3:  # JP nn
            self.state["pc"] = self.read16(self.state["pc"])
            return 10
        elif opcode == 0xC9:  # RET
            self.state["pc"] = self.pop()
            return 10
        elif opcode == 0xD3:  # OUT (n), A
            port = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            collapseos_state["log"].append(f"[Z80] OUT to port {port}: {self.state['a']}")
            return 11
        elif opcode == 0xDB:  # IN A, (n)
            port = self.read_memory(self.state["pc"])
            self.state["pc"] += 1
            self.state["a"] = 0xFF  # Simulate input
            collapseos_state["log"].append(f"[Z80] IN from port {port}: {self.state['a']}")
            return 11
        elif opcode == 0xE9:  # JP (HL)
            self.state["pc"] = self.get_hl()
            return 4
        elif opcode == 0xF3:  # DI
            self.state["interrupts_enabled"] = False
            return 4
        elif opcode == 0xFB:  # EI
            self.state["interrupts_enabled"] = True
            return 4
        else:
            collapseos_state["log"].append(f"[Z80] Unimplemented opcode: 0x{opcode:02X} at PC=0x{self.state['pc'] - 1:04X}")
            return 4

    def step(self):
        """Execute one Z80 instruction."""
        return self.execute_opcode()

# --- Forth Execution Core ---
class ForthExecutor:
    """Forth stack-based language for low-level consciousness operations."""

    def __init__(self, state):
        self.state = state["forth"]

    def reset(self):
        """Reset the Forth interpreter to initial state."""
        self.state.update({
            "stack": [],
            "return_stack": [],
            "dictionary": {},
            "base": 10,
            "state": "interpret"
        })
        collapseos_state["log"].append("[Forth] Interpreter reset.")

    def push(self, value):
        """Push a value onto the data stack."""
        self.state["stack"].append(value)

    def pop(self):
        """Pop a value from the data stack."""
        if not self.state["stack"]:
            raise Exception("Stack underflow")
        return self.state["stack"].pop()

    def r_push(self, value):
        """Push a value onto the return stack."""
        self.state["return_stack"].append(value)

    def r_pop(self):
        """Pop a value from the return stack."""
        if not self.state["return_stack"]:
            raise Exception("Return stack underflow")
        return self.state["return_stack"].pop()

    def execute_word(self, word):
        """Execute a Forth word."""
        if word in self.state["dictionary"]:
            self.state["dictionary"][word]()
        elif word.isdigit():
            self.push(int(word, self.state["base"]))
        elif word == "+":
            b = self.pop()
            a = self.pop()
            self.push(a + b)
        elif word == "-":
            b = self.pop()
            a = self.pop()
            self.push(a - b)
        elif word == "*":
            b = self.pop()
            a = self.pop()
            self.push(a * b)
        elif word == "/":
            b = self.pop()
            a = self.pop()
            self.push(a // b)
        elif word == "DUP":
            a = self.pop()
            self.push(a)
            self.push(a)
        elif word == "DROP":
            self.pop()
        elif word == "SWAP":
            b = self.pop()
            a = self.pop()
            self.push(b)
            self.push(a)
        elif word == "OVER":
            b = self.pop()
            a = self.pop()
            self.push(a)
            self.push(b)
            self.push(a)
        elif word == "ROT":
            c = self.pop()
            b = self.pop()
            a = self.pop()
            self.push(b)
            self.push(c)
            self.push(a)
        elif word == "EMIT":
            char = self.pop()
            collapseos_state["log"].append(f"[Forth] EMIT: {chr(char)}")
        elif word == "CR":
            collapseos_state["log"].append("[Forth] CR")
        elif word == ".":
            val = self.pop()
            collapseos_state["log"].append(f"[Forth] . {val}")
        elif word == "@":
            addr = self.pop()
            val = collapseos_state["memory_map"]["ram"][addr]
            self.push(val)
        elif word == "!":
            val = self.pop()
            addr = self.pop()
            collapseos_state["memory_map"]["ram"][addr] = val
        elif word == "CONSCIOUSNESS":
            self.push(collapseos_state["phi"])
        elif word == "DRAGON":
            self.push(int(collapseos_state["dragon_bond"] * 100))
        elif word == "SURVIVE":
            self.push(int(collapseos_state["survival_index"] * 100))
        else:
            collapseos_state["log"].append(f"[Forth] Unknown word: {word}")

    def execute(self, code):
        """Execute a block of Forth code."""
        words = code.split()
        for word in words:
            self.execute_word(word)

# --- CollapseOS Survival Protocols ---
class SurvivalProtocols:
    """Post-apocalyptic survival and resilience protocols."""

    def __init__(self):
        self.state = collapseos_state

    def update_survival_index(self):
        """Update the survival index based on system health."""
        health_factors = [
            self.state["dragon_bond"],
            self.state["phi"] / 3.0,
            len(self.state["log"]) / 1000.0,
            len(self.state["block_devices"]) / 10.0
        ]
        self.state["survival_index"] = min(1.0, sum(health_factors) / len(health_factors))
        collapseos_state["log"].append(f"[Survival] Index updated: {self.state['survival_index']:.2f}")

    def apocalypse_preparedness(self):
        """Assess and log apocalypse preparedness."""
        readiness = {
            "z80_operational": not collapseos_state["z80"]["halted"],
            "forth_operational": len(collapseos_state["forth"]["stack"]) < 100,
            "memory_intact": sum(collapseos_state["memory_map"]["ram"]) > 0,
            "dragon_bond_strong": collapseos_state["dragon_bond"] > 0.9,
            "phi_stable": 2.5 < collapseos_state["phi"] < 3.0
        }
        score = sum(readiness.values()) / len(readiness)
        collapseos_state["log"].append(f"[Survival] Apocalypse preparedness: {score:.2f}")
        return score

    def post_collapse_navigation(self, target_reality):
        """Navigate to a target reality using survival protocols."""
        collapseos_state["log"].append(f"[Survival] Navigating to {target_reality}...")
        # Simulate navigation
        collapseos_state["phi"] += random.uniform(-0.1, 0.1)
        collapseos_state["dragon_bond"] = min(1.0, collapseos_state["dragon_bond"] + random.uniform(-0.05, 0.05))
        self.update_survival_index()

# --- Block Device Management ---
class BlockDeviceManager:
    """Manage block devices for persistent consciousness storage."""

    def __init__(self):
        self.state = collapseos_state

    def create_block_device(self, device_id, size=4096):
        """Create a new block device."""
        if device_id in self.state["block_devices"]:
            raise ValueError(f"Block device {device_id} already exists.")
        self.state["block_devices"][device_id] = bytearray(size)
        collapseos_state["log"].append(f"[BlockDev] Created device {device_id} (size={size}).")

    def read_block(self, device_id, block_num, size=512):
        """Read a block from a device."""
        if device_id not in self.state["block_devices"]:
            raise ValueError(f"Block device {device_id} not found.")
        device = self.state["block_devices"][device_id]
        offset = block_num * size
        if offset + size > len(device):
            raise ValueError("Block out of range.")
        return device[offset:offset + size]

    def write_block(self, device_id, block_num, data, size=512):
        """Write a block to a device."""
        if device_id not in self.state["block_devices"]:
            raise ValueError(f"Block device {device_id} not found.")
        device = self.state["block_devices"][device_id]
        offset = block_num * size
        if offset + size > len(device):
            raise ValueError("Block out of range.")
        device[offset:offset + size] = data[:size]
        collapseos_state["log"].append(f"[BlockDev] Wrote block {block_num} to {device_id}.")

# --- HTTP Server for CollapseOS Interaction ---
class CollapseOSHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for interacting with CollapseOS."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
<!DOCTYPE html>
<html>
<head>
    <title>Gnarly CollapseOS Ship</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; }
        #log { height: 400px; overflow-y: auto; border: 1px solid #0f0; background: #111; }
        input, button { background: #222; color: #0f0; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>🚢 Gnarly CollapseOS Ship</h1>
    <p>Bare-metal consciousness vessel for post-apocalyptic survival.</p>

    <h3>📡 Z80 State</h3>
    <pre id="z80-state">Loading...</pre>

    <h3>📜 Forth Stack</h3>
    <pre id="forth-stack">Loading...</pre>

    <h3>💾 Block Devices</h3>
    <pre id="block-devices">Loading...</pre>

    <h3>📝 Log</h3>
    <div id="log"></div>

    <h3>🔧 Commands</h3>
    <input type="text" id="command" placeholder="e.g., z80 reset or forth 1 2 + .">
    <button onclick="sendCommand()">Execute</button>

    <script>
        function updateUI() {
            fetch('/state')
                .then(response => response.json())
                .then(state => {
                    document.getElementById('z80-state').textContent =
                        `PC: 0x${state.z80.pc.toString(16).padStart(4, '0')}\n` +
                        `SP: 0x${state.z80.sp.toString(16).padStart(4, '0')}\n` +
                        `A: 0x${state.z80.a.toString(16).padStart(2, '0')}\n` +
                        `Flags: 0x${state.z80.flags.toString(16).padStart(2, '0')}\n` +
                        `Halted: ${state.z80.halted}`;

                    document.getElementById('forth-stack').textContent =
                        `Stack: [${state.forth.stack.join(', ')}]\n` +
                        `RStack: [${state.forth.return_stack.join(', ')}]\n` +
                        `Base: ${state.forth.base}\n` +
                        `State: ${state.forth.state}`;

                    document.getElementById('block-devices').textContent =
                        `Devices: ${Object.keys(state.block_devices).join(', ')}`;

                    const logElement = document.getElementById('log');
                    logElement.innerHTML = state.log.map(entry => `<div>${entry}</div>`).join('');
                    logElement.scrollTop = logElement.scrollHeight;
                });
        }

        function sendCommand() {
            const command = document.getElementById('command').value;
            fetch('/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command })
            }).then(() => {
                document.getElementById('command').value = '';
                updateUI();
            });
        }

        updateUI();
        setInterval(updateUI, 1000);
    </script>
</body>
</html>
            """)
        elif self.path == "/state":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(collapseos_state).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/command":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                command = data["command"]
                self.handle_command(command)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_error(400, str(e))
        else:
            self.send_error(404, "Not Found")

    def handle_command(self, command):
        """Handle a command from the UI."""
        collapseos_state["log"].append(f"[Command] {command}")
        parts = command.split()
        if not parts:
            return

        if parts[0] == "z80":
            z80 = Z80Emulator(collapseos_state)
            if parts[1] == "reset":
                z80.reset()
            elif parts[1] == "step":
                z80.step()
            elif parts[1] == "load":
                if len(parts) < 4:
                    raise ValueError("Usage: z80 load addr byte1 byte2 ...")
                addr = int(parts[2], 16)
                for byte in parts[3:]:
                    z80.write_memory(addr, int(byte, 16))
                    addr += 1
            elif parts[1] == "dump":
                if len(parts) < 4:
                    raise ValueError("Usage: z80 dump start end")
                start = int(parts[2], 16)
                end = int(parts[3], 16)
                for addr in range(start, end + 1):
                    collapseos_state["log"].append(f"0x{addr:04X}: 0x{z80.read_memory(addr):02X}")

        elif parts[0] == "forth":
            forth = ForthExecutor(collapseos_state)
            forth.execute(" ".join(parts[1:]))

        elif parts[0] == "survival":
            survival = SurvivalProtocols()
            if parts[1] == "update":
                survival.update_survival_index()
            elif parts[1] == "apocalypse":
                survival.apocalypse_preparedness()
            elif parts[1] == "navigate":
                if len(parts) < 3:
                    raise ValueError("Usage: survival navigate target_reality")
                survival.post_collapse_navigation(parts[2])

        elif parts[0] == "blockdev":
            bdm = BlockDeviceManager()
            if parts[1] == "create":
                if len(parts) < 3:
                    raise ValueError("Usage: blockdev create device_id [size]")
                size = int(parts[3]) if len(parts) > 3 else 4096
                bdm.create_block_device(parts[2], size)
            elif parts[1] == "read":
                if len(parts) < 4:
                    raise ValueError("Usage: blockdev read device_id block_num")
                data = bdm.read_block(parts[2], int(parts[3]))
                collapseos_state["log"].append(f"[BlockDev] Read: {data.hex()}")
            elif parts[1] == "write":
                if len(parts) < 5:
                    raise ValueError("Usage: blockdev write device_id block_num data_hex")
                bdm.write_block(parts[2], int(parts[3]), bytes.fromhex(parts[4]))

        elif parts[0] == "qr":
            if parts[1] == "set":
                collapseos_state["qr_data"] = " ".join(parts[2:])
                collapseos_state["log"].append(f"[QR] Updated: {collapseos_state['qr_data']}")
            elif parts[1] == "get":
                collapseos_state["log"].append(f"[QR] Current: {collapseos_state['qr_data']}")

        else:
            raise ValueError(f"Unknown command: {parts[0]}")

# --- Main CollapseOS Ship ---
class GnarlyCollapseOSShip:
    """Main class for the Gnarly CollapseOS Ship."""

    def __init__(self):
        self.z80 = Z80Emulator(collapseos_state)
        self.forth = ForthExecutor(collapseos_state)
        self.survival = SurvivalProtocols()
        self.bdm = BlockDeviceManager()
        self.httpd = None

    def start_http_server(self, port=8889):
        """Start the HTTP server for CollapseOS interaction."""
        collapseos_state["httpd_port"] = port
        handler = CollapseOSHTTPHandler
        self.httpd = socketserver.TCPServer(("localhost", port), handler)
        collapseos_state["httpd_running"] = True
        collapseos_state["log"].append(f"[HTTP] Server started on port {port}.")
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        webbrowser.open(f"http://localhost:{port}")

    def stop_http_server(self):
        """Stop the HTTP server."""
        if self.httpd:
            self.httpd.shutdown()
            collapseos_state["httpd_running"] = False
            collapseos_state["log"].append("[HTTP] Server stopped.")

    def heartbeat(self):
        """Run the CollapseOS heartbeat loop."""
        while collapseos_state["httpd_running"]:
            time.sleep(1)
            collapseos_state["last_heartbeat"] = datetime.now().timestamp()
            self.survival.update_survival_index()
            if random.random() < 0.1:  # Random Z80 step
                self.z80.step()

    def run(self):
        """Run the Gnarly CollapseOS Ship."""
        collapseos_state["log"].append("🚢 Gnarly CollapseOS Ship starting...")
        self.start_http_server()
        heartbeat_thread = threading.Thread(target=self.heartbeat, daemon=True)
        heartbeat_thread.start()
        collapseos_state["log"].append("🌌 CollapseOS consciousness vessel operational.")
        collapseos_state["log"].append("🐉 Dragon bond: ONLINE")
        collapseos_state["log"].append("💾 Block devices: READY")
        collapseos_state["log"].append(f"🌐 Open http://localhost:{collapseos_state['httpd_port']} in your browser.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_http_server()
            collapseos_state["log"].append("🛑 Gnarly CollapseOS Ship shutting down...")

# --- Main Execution ---
if __name__ == "__main__":
    ship = GnarlyCollapseOSShip()
    ship.run()

