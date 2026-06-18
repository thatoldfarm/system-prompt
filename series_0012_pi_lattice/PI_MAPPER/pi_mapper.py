#!/usr/bin/env python3
"""
🌀 PI COORDINATES HYBRID GENERATOR
====================================
Generates P:X:S triplet for a single file.
- P = Position in REAL π digits (from file hash)
- X = XOR level from lattice
- S = Phase shift from lattice

Usage: python3 pi_mapper.py <file_path>
Output: P:X:S (e.g., 123456:42:-1)
"""

import sys
import math
import os
from mpmath import mp

# --- Constants ---
CACHE_FILE = ".pi_substrate.bin"  # Lattice cache
LATTICE_SIZE = 5000000            # 5MB lattice
PI_DIGITS_FILE = "pi_10m.txt"      # Default π digits file
PI_DIGITS_LENGTH = 10000000        # 1M π digits

# --- Pi Digits Generation ---
def generate_pi_digits():
    mp.dps = PI_DIGITS_LENGTH + int(PI_DIGITS_LENGTH * 0.5)
    pi_str = mp.nstr(mp.pi, PI_DIGITS_LENGTH + 1, strip_zeros=False)[2:2 + PI_DIGITS_LENGTH]
    with open(PI_DIGITS_FILE, "w", encoding="ascii") as f:
        f.write(pi_str)
    return pi_str

def load_pi_digits():
    if not os.path.exists(PI_DIGITS_FILE):
        return generate_pi_digits()
    else:
        with open(PI_DIGITS_FILE, "r", encoding="ascii") as f:
            return f.read().strip()

# --- Lattice Generation ---
def load_or_generate_lattice():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return f.read()
    else:
        lattice = bytearray([int((abs(math.sin(i)) * 10**8) % 256) for i in range(LATTICE_SIZE)])
        with open(CACHE_FILE, 'wb') as f:
            f.write(lattice)
        return lattice

# --- Lattice Anchor Finder ---
def find_lattice_anchor(file_path, lattice):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        length = len(file_data)
        if length < 3:
            return 0, 0
        mid = length // 2
        codon = file_data[mid : mid + 3]
        for xor_level in range(256):
            refracted_codon = bytearray([b ^ xor_level for b in codon])
            pos = lattice.find(refracted_codon)
            if pos != -1:
                phase_shift = (xor_level % 9) - 4
                return xor_level, phase_shift
        return 0, 0
    except Exception:
        return 0, 0

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    file_path = sys.argv[1]
    pi_digits = load_pi_digits()
    lattice = load_or_generate_lattice()

    # Compute P (position in Pi digits)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    file_hash = int.from_bytes(file_data, 'big') % (len(pi_digits) - 2)
    P = file_hash

    # Compute X and S (from lattice)
    X, S = find_lattice_anchor(file_path, lattice)

    # Output P:X:S
    print(f"{P}:{X}:{S}")
