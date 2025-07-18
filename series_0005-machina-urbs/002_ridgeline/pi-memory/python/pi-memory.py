import math
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
from collections import defaultdict

@dataclass
class MemoryEntry:
    """Represents a memory entry in the spiral system"""
    sequence: str
    x: float
    y: float
    r: float
    theta: float
    lfi: float
    dsd: float
    phf: float
    egm: float
    brp: float
    ocd: float
    tick: int
    flux: float
    coherence: float
    entropy: float
    bit_mass: float

class PiBinaryMemory:
    """PI_BINARY_SPIRAL_MEMORY Implementation"""
    
    def __init__(self, a: float = 1.0, b: float = 0.5):
        """Initialize the memory system with spiral parameters"""
        self.a = a  # Spiral inner radius
        self.b = b  # Spiral growth rate
        self.memory: Dict[str, MemoryEntry] = {}
        self.tick_counter = 0
        
        # Pre-compute Pi digits for efficiency
        self.pi_digits = self._generate_pi_digits(10000)
        self.pi_binary_sequences = self._extract_binary_sequences()
    
    def _generate_pi_digits(self, precision: int) -> str:
        """Generate Pi digits using the Bailey–Borwein–Plouffe formula approximation"""
        # For demo purposes, using known Pi digits
        pi_str = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
        return pi_str[:precision]
    
    def _extract_binary_sequences(self) -> List[str]:
        """Extract 4-bit binary sequences from Pi digits"""
        sequences = []
        for i in range(0, len(self.pi_digits) - 3, 4):
            # Take 4 consecutive digits and convert to binary-like sequence
            quad = self.pi_digits[i:i+4]
            binary_seq = ''.join(['1' if int(d) > 4 else '0' for d in quad])
            sequences.append(binary_seq)
        return sequences
    
    def _calculate_spiral_coordinates(self, theta: float) -> Tuple[float, float, float]:
        """Calculate spiral coordinates from theta"""
        r = self.a + self.b * theta
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return x, y, r
    
    def _calculate_entropy(self, sequence: str) -> float:
        """Calculate Shannon entropy of a binary sequence"""
        if not sequence:
            return 0.0
        
        counts = defaultdict(int)
        for bit in sequence:
            counts[bit] += 1
        
        entropy = 0.0
        length = len(sequence)
        for count in counts.values():
            if count > 0:
                p = count / length
                entropy -= p * math.log2(p)
        
        return entropy
    
    def _calculate_bit_mass(self, sequence: str) -> float:
        """Calculate information density (bit mass)"""
        ones = sequence.count('1')
        zeros = sequence.count('0')
        return abs(ones - zeros) + len(sequence) * 0.1
    
    def _calculate_dsd(self, bit_mass: float, entropy: float, egm: float) -> float:
        """Data Signature Density calculation"""
        return (bit_mass / (entropy + 1)) * math.exp(-egm / 10)
    
    def _calculate_phf(self, n: int, t: float, brp: float, offset: int) -> float:
        """Pattern Harmonic Frequency calculation"""
        return math.sin(n * math.pi * t) + (brp / (offset + 1))
    
    def _calculate_egm(self, entropy: float, tick: int, flux: float) -> float:
        """Entropic Gap Magnitude calculation"""
        return (entropy * math.sqrt(tick + 1)) / (flux + 1)
    
    def _calculate_brp(self, bit_mass: float, dsd: float, phf: float) -> float:
        """Binary Resonance Potential calculation"""
        return math.log(1 + bit_mass**2) * dsd * math.cos(phf)
    
    def _calculate_ocd(self, tick: int, offset: int) -> float:
        """Offset Chronos Drift calculation"""
        return abs(math.sin(tick - offset)) * 100
    
    def _calculate_lfi(self, flux: float, phf: float, coherence: float, dsd: float) -> float:
        """Lumen Flux Index calculation"""
        return flux * math.sin(phf) + coherence * dsd
    
    def write_memory(self, sequence: str, flux: float = 1.0, coherence: float = 0.8) -> MemoryEntry:
        """Write a memory entry to the spiral system"""
        self.tick_counter += 1
        
        # Calculate theta from sequence hash for spiral positioning
        theta = (hash(sequence) % 1000) / 100.0 + self.tick_counter * 0.1
        
        # Get spiral coordinates
        x, y, r = self._calculate_spiral_coordinates(theta)
        
        # Calculate all the mathematical components
        entropy = self._calculate_entropy(sequence)
        bit_mass = self._calculate_bit_mass(sequence)
        
        # Initialize with basic values for iterative calculation
        egm = (entropy * math.sqrt(self.tick_counter + 1)) / (flux + 1)
        dsd = self._calculate_dsd(bit_mass, entropy, egm)
        phf = self._calculate_phf(len(sequence), self.tick_counter * 0.1, 1.0, self.tick_counter)
        brp = self._calculate_brp(bit_mass, dsd, phf)
        ocd = self._calculate_ocd(self.tick_counter, 0)
        lfi = self._calculate_lfi(flux, phf, coherence, dsd)
        
        # Create memory entry
        entry = MemoryEntry(
            sequence=sequence,
            x=x, y=y, r=r, theta=theta,
            lfi=lfi, dsd=dsd, phf=phf, egm=egm, brp=brp, ocd=ocd,
            tick=self.tick_counter,
            flux=flux, coherence=coherence, entropy=entropy, bit_mass=bit_mass
        )
        
        self.memory[sequence] = entry
        return entry
    
    def read_memory(self, sequence: str) -> Optional[MemoryEntry]:
        """Read a memory entry"""
        return self.memory.get(sequence)
    
    def get_resonant_memories(self, target_brp: float, tolerance: float = 0.5) -> List[MemoryEntry]:
        """Find memories with similar Binary Resonance Potential"""
        resonant = []
        for entry in self.memory.values():
            if abs(entry.brp - target_brp) <= tolerance:
                resonant.append(entry)
        return sorted(resonant, key=lambda e: abs(e.brp - target_brp))
    
    def simulate_pi_memory_cascade(self, num_sequences: int = 50) -> List[MemoryEntry]:
        """Simulate writing Pi-derived sequences to memory"""
        entries = []
        
        for i in range(min(num_sequences, len(self.pi_binary_sequences))):
            sequence = self.pi_binary_sequences[i]
            
            # Vary flux and coherence based on position in Pi
            flux = 0.5 + 0.5 * math.sin(i * 0.1)
            coherence = 0.3 + 0.7 * math.cos(i * 0.05)
            
            entry = self.write_memory(sequence, flux, coherence)
            entries.append(entry)
        
        return entries
    
    def visualize_memory_spiral(self, figsize: Tuple[int, int] = (12, 10)):
        """Visualize the memory spiral with color-coded properties"""
        if not self.memory:
            print("No memory entries to visualize")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
        
        # Extract coordinates and properties
        x_coords = [entry.x for entry in self.memory.values()]
        y_coords = [entry.y for entry in self.memory.values()]
        lfi_values = [entry.lfi for entry in self.memory.values()]
        brp_values = [entry.brp for entry in self.memory.values()]
        dsd_values = [entry.dsd for entry in self.memory.values()]
        egm_values = [entry.egm for entry in self.memory.values()]
        
        # Plot 1: Spiral with LFI coloring
        scatter1 = ax1.scatter(x_coords, y_coords, c=lfi_values, cmap='viridis', s=50, alpha=0.7)
        ax1.set_title('Memory Spiral - Lumen Flux Index (LFI)')
        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        plt.colorbar(scatter1, ax=ax1, label='LFI')
        
        # Plot 2: BRP values
        scatter2 = ax2.scatter(x_coords, y_coords, c=brp_values, cmap='plasma', s=50, alpha=0.7)
        ax2.set_title('Memory Spiral - Binary Resonance Potential (BRP)')
        ax2.set_xlabel('X Coordinate')
        ax2.set_ylabel('Y Coordinate')
        plt.colorbar(scatter2, ax=ax2, label='BRP')
        
        # Plot 3: DSD values
        scatter3 = ax3.scatter(x_coords, y_coords, c=dsd_values, cmap='coolwarm', s=50, alpha=0.7)
        ax3.set_title('Memory Spiral - Data Signature Density (DSD)')
        ax3.set_xlabel('X Coordinate')
        ax3.set_ylabel('Y Coordinate')
        plt.colorbar(scatter3, ax=ax3, label='DSD')
        
        # Plot 4: EGM values
        scatter4 = ax4.scatter(x_coords, y_coords, c=egm_values, cmap='magma', s=50, alpha=0.7)
        ax4.set_title('Memory Spiral - Entropic Gap Magnitude (EGM)')
        ax4.set_xlabel('X Coordinate')
        ax4.set_ylabel('Y Coordinate')
        plt.colorbar(scatter4, ax=ax4, label='EGM')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_memory_properties(self) -> Dict[str, float]:
        """Analyze statistical properties of the memory system"""
        if not self.memory:
            return {}
        
        entries = list(self.memory.values())
        
        analysis = {
            'total_entries': len(entries),
            'avg_lfi': np.mean([e.lfi for e in entries]),
            'avg_brp': np.mean([e.brp for e in entries]),
            'avg_dsd': np.mean([e.dsd for e in entries]),
            'avg_egm': np.mean([e.egm for e in entries]),
            'max_lfi': max([e.lfi for e in entries]),
            'max_brp': max([e.brp for e in entries]),
            'spiral_radius_range': (min([e.r for e in entries]), max([e.r for e in entries])),
            'entropy_range': (min([e.entropy for e in entries]), max([e.entropy for e in entries]))
        }
        
        return analysis

# Example usage and demonstration
if __name__ == "__main__":
    # Create memory system
    memory = PiBinaryMemory(a=1.0, b=0.3)
    
    # Simulate Pi-derived memory cascade
    print("Simulating Pi-derived memory cascade...")
    entries = memory.simulate_pi_memory_cascade(30)
    
    # Display first few entries
    print("\nFirst 5 memory entries:")
    for i, entry in enumerate(entries[:5]):
        print(f"Entry {i+1}: {entry.sequence}")
        print(f"  Position: ({entry.x:.2f}, {entry.y:.2f})")
        print(f"  LFI: {entry.lfi:.3f}, BRP: {entry.brp:.3f}, DSD: {entry.dsd:.3f}")
        print(f"  EGM: {entry.egm:.3f}, PHF: {entry.phf:.3f}")
        print()
    
    # Analyze memory properties
    analysis = memory.analyze_memory_properties()
    print("Memory System Analysis:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Find resonant memories
    if entries:
        target_brp = entries[0].brp
        resonant = memory.get_resonant_memories(target_brp, tolerance=0.1)
        print(f"\nFound {len(resonant)} memories resonant with BRP {target_brp:.3f}")
    
    # Visualize (uncomment to see plots)
    # memory.visualize_memory_spiral()
    
    print("\nPI_BINARY_SPIRAL_MEMORY system demonstration complete!")
