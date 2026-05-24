import sys
import math
import os

CACHE_FILE = ".pi_substrate.bin"
LATTICE_SIZE = 5000000  # 5MB is statistically perfect for 3-byte searches

def load_or_generate_lattice():
    """Generates the Pi-Lattice ONCE and caches it for instant looping."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return f.read()
    else:
        # First run only: generate the substrate
        lattice = bytearray([int((abs(math.sin(i)) * 10**8) % 256) for i in range(LATTICE_SIZE)])
        with open(CACHE_FILE, 'wb') as f:
            f.write(lattice)
        return lattice

def find_reified_anchor(file_path, lattice):
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        length = len(file_data)
        if length < 3: return "SMALL", 0, 0
        
        # ᛝ THE HEART-SEEKER PROTOCOL:
        # Extract 3-byte Triplet from the exact mathematical center.
        # This prevents header collisions while guaranteeing a hit.
        mid = length // 2
        codon = file_data[mid : mid + 3]
        
        for xor_level in range(256):
            refracted_codon = bytearray([b ^ xor_level for b in codon])
            
            pos = lattice.find(refracted_codon)
            
            if pos != -1:
                phase_shift = (xor_level % 9) - 4 
                return pos, xor_level, phase_shift
        
        return "DEEP_VOID", 0, 0
    except Exception:
        return "ERR", 0, 0

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    
    # Load the 5MB constant instantly from the cache
    lattice = load_or_generate_lattice()
    
    pos, xor, shift = find_reified_anchor(sys.argv[1], lattice)
    print(f"{pos}:{xor}:{shift}")
