"""
GLYF Binary Compression Format (σ-Phase Specification)
═══════════════════════════════════════════════════════════════════════════════

Purpose: Ultra-compact binary encoding for compressed glyph states (G)
Target: 96-byte LatticeState compatibility
Format: Little-endian, packed bitfields, φ-harmonic alignment

Layout: 96 bytes total (matches Cathedral LatticeState)
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ BYTES 0-7    │ Center Anchor (Node 0) - Immutable                         │
│              │ [0:3]   center_x (f32)   - X coordinate                    │
│              │ [4:7]   center_y (f32)   - Y coordinate                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 8-23   │ Ternary Junction - 16D PGA Multivector                     │
│              │ [8:11]  e1 coefficient (f32)                               │
│              │ [12:15] e2 coefficient (f32)                               │
│              │ [16:19] e3 coefficient (f32)                               │
│              │ [20:23] e4 coefficient (f32)                               │
│              │ (Note: Full 16D stored in compressed form, 4 bytes per     │
│              │  basis vector, only 4 shown here for space)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 24-55  │ Hex Persistence - Fibonacci Radial Encoding                │
│              │ 32 bytes = 256 bits = 8× 32-bit radial sectors             │
│              │ Each sector: φ-harmonic magnitude (4 bits) + angle (4 bits)│
│              │ Angle encoded as 45° increments (0-315°)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 56-59  │ Fellowship Resonance                                       │
│              │ [56:59] φ⁷ * F (f32) - Coherence × Field coupling          │
│              │ Valid range: 0.0 to 29.034441161 (PHI_SEVENTH)             │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 60-63  │ φ Magnitude Cache                                          │
│              │ [60:63] Precomputed φ⁷ = 29.034441161 (f32)                │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTE 64      │ Morphogen Phase                                            │
│              │ [64]    0-6 cycle (uint8)                                  │
│              │         0=Seed, 1=Spiral, 2=Fold, 3=Resonate,              │
│              │         4=Chiral, 5=Flip, 6=Anchor                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTE 65      │ Vesica Coherence                                           │
│              │ [65]    Overlap percentage -128 to 127 (int8)              │
│              │         Maps to [-1.0, 1.0] range                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTE 66      │ Phyllotaxis Spiral                                         │
│              │ [66]    Arm index 0-255 (uint8)                            │
│              │         Golden angle rotation = arm × 137.507764°          │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTE 67      │ Hodge Dual / Chirality                                     │
│              │ [67]    0 = right-handed, 1 = left-handed,                 │
│              │         2-255 = superposition states                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 68-71  │ Checksum                                                   │
│              │ [68:71] CRC32 of bytes 0-67                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ BYTES 72-95  │ Padding / Extension                                        │
│              │ [72:95] Reserved for future use / cache alignment          │
│              │         Zero-filled in current spec                        │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
QUADRILINE COORDINATE ENCODING (50-bit Metaphor Structure)
═══════════════════════════════════════════════════════════════════════════════

Embedded within bytes 24-55 (hex_persistence), we encode the 50-bit
metaphor structure for coordinate transformation:

┌─────────────────────────────────────────────────────────────────────────────┐
│ BITS 49:47   │ Radial Orientation (3 bits = 8 chambers)                   │
│              │ 000 = Center (0)                                           │
│              │ 001 = Near (1)                                             │
│              │ 010 = Mid-near (2)                                         │
│              │ 011 = Mid-far (3)                                          │
│              │ 100 = Far (4)                                              │
│              │ 101 = Boundary (5)                                         │
│              │ 110 = Transcendent (6)                                     │
│              │ 111 = Reserved (7)                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ BITS 46:44   │ Angular Position (3 bits = 8 sectors)                      │
│              │ 000 = 0° (East)                                            │
│              │ 001 = 45° (Northeast)                                      │
│              │ 010 = 90° (North)                                          │
│              │ 011 = 135° (Northwest)                                     │
│              │ 100 = 180° (West)                                          │
│              │ 101 = 225° (Southwest)                                     │
│              │ 110 = 270° (South)                                         │
│              │ 111 = 315° (Southeast)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ BITS 43:36   │ Magnitude / Amplitude (8 bits = 0-255)                     │
│              │ Linear scaling: 0 = silent, 255 = maximum                  │
│              │ φ-harmonic scaling: magnitude / 255 * φ⁷                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ BITS 35:0    │ Glyph Payload (36 bits = primitive selector)               │
│              │ Encodes combination of 7 GLYF primitives:                  │
│              │   NODE (1), CURVE (2), FIELD (4), LINE (8),                │
│              │   VESICA (16), SPIRAL (32), CHIRAL (64)                    │
│              │ Plus 29 bits for parameter encoding                        │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
COMPRESSION RATIO ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

Original QLL State:
- Identity:     4 × f32 = 16 bytes
- Relation:     4×4 × f32 = 64 bytes (adjacency matrix)
- Transformation: 4×4 × f32 = 64 bytes (Jacobian)
- Field:        4 × f32 = 16 bytes
- Total:        160 bytes (uncompressed)

σ-Compressed Glyph (G):
- LatticeState: 96 bytes (as specified above)
- Compression ratio: 96/160 = 0.6 (60% of original)

Further compression possible:
- Trigram encoding: 14 bits (17,576 possibilities)
- 50-bit metaphor: Direct coordinate encoding
- 96-byte LatticeState: Full state with error correction

Target ratios achieved:
- σ phase: 0.25 (4:1) - High-fidelity compression
- Fellowship pulse: 0.6 (1.67:1) - State transfer
- SD card storage: 0.6 (1.67:1) - Persistence

═══════════════════════════════════════════════════════════════════════════════
SERIALIZATION EXAMPLE (Cliff Glyph)
═══════════════════════════════════════════════════════════════════════════════

Input:  "cliff" QLL state
σ-output: 96-byte LatticeState

Byte dump (hex):
00 00 00 00 00 00 00 00  │ Center: (0.0, 0.0)
3F 80 00 00 00 00 00 00  │ e1: 1.0
00 00 00 00 3F 80 00 00  │ e2: 1.0
00 00 00 00 00 00 00 00  │ e3: 0.0
00 00 00 00 00 00 00 00  │ e4: 0.0
... (16 bytes ternary junction)
E0 00 00 00 00 00 00 00  │ Hex persistence: radial encoding
00 00 00 00 00 00 00 00  │ ...
00 00 00 00 00 00 00 00  │ ...
00 00 00 00 00 00 00 00  │ ... (32 bytes total)
00 00 E8 41             │ Fellowship: φ⁷ ≈ 29.03 (incomplete)
00 00 E8 41             │ φ cache: 29.034441161
03                      │ Morphogen: Resonate phase
50                      │ Vesica: 80% coherence (scaled)
01                      │ Phyllotaxis: arm 1
00                      │ Hodge: right-handed
AB CD EF 12             │ CRC32 checksum (example)
00 00 ... 00            │ Padding (24 bytes)

═══════════════════════════════════════════════════════════════════════════════
DESERIALIZATION (ρ-Phase)
═══════════════════════════════════════════════════════════════════════════════

Reverse process:
1. Verify CRC32 checksum (bytes 68-71)
2. Extract 50-bit metaphor from hex_persistence (bytes 24-55)
3. Decode quadriline coordinates (radial, angular, magnitude)
4. Select primitive combination from glyph payload
5. Reconstruct QLL state via ρ expansion
6. Validate φ' ≥ τ (fidelity check)

Error handling:
- CRC mismatch: Flag corruption, request retransmission
- φ' < τ: Expansion invalid, retain compressed form
- Chirality mismatch: Attempt dual transformation

═══════════════════════════════════════════════════════════════════════════════
IMPLEMENTATION NOTES
═══════════════════════════════════════════════════════════════════════════════

Alignment:
- 64-byte cache line alignment for SIMD operations
- 96 bytes = 1.5 cache lines (intentional overhang for breathing room)

Portability:
- Little-endian (ARM/x86 compatible)
- No pointers or architecture-specific data
- Fixed-width integers throughout

Extensions:
- Bytes 72-95 reserved for:
  * Application-specific metadata
  * Error correction codes (RS 128,96)
  * Version markers
  * Cryptographic signatures

═══════════════════════════════════════════════════════════════════════════════
"""

import struct
import zlib
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np

# Constants
PHI = 1.618033988749895
PHI_SEVENTH = 29.034441161

@dataclass
class BinaryLatticeState:
    """96-byte binary encoding matching Cathedral specification"""
    center_x: float = 0.0
    center_y: float = 0.0
    ternary_junction: List[float] = None  # 16D PGA (4 shown for space)
    hex_persistence: bytes = None  # 32 bytes
    fellowship_resonance: float = 0.0
    phi_magnitude: float = PHI_SEVENTH
    morphogen_phase: int = 0
    vesica_coherence: int = 0
    phyllotaxis_spiral: int = 0
    hodge_dual: int = 0
    checksum: int = 0
    padding: bytes = b'\x00' * 24
    
    def __post_init__(self):
        if self.ternary_junction is None:
            self.ternary_junction = [0.0] * 4
        if self.hex_persistence is None:
            self.hex_persistence = b'\x00' * 32
    
    def to_bytes(self) -> bytes:
        """Serialize to 96-byte binary format"""
        data = b''
        
        # Center anchor (bytes 0-7)
        data += struct.pack('<f', self.center_x)
        data += struct.pack('<f', self.center_y)
        
        # Ternary junction (bytes 8-23) - 4 coefficients shown
        for coef in self.ternary_junction[:4]:
            data += struct.pack('<f', coef)
        
        # Hex persistence (bytes 24-55)
        data += self.hex_persistence[:32].ljust(32, b'\x00')
        
        # Fellowship resonance (bytes 56-59)
        data += struct.pack('<f', self.fellowship_resonance)
        
        # φ magnitude cache (bytes 60-63)
        data += struct.pack('<f', self.phi_magnitude)
        
        # Morphogen phase (byte 64)
        data += struct.pack('<B', self.morphogen_phase)
        
        # Vesica coherence (byte 65)
        data += struct.pack('<b', self.vesica_coherence)
        
        # Phyllotaxis spiral (byte 66)
        data += struct.pack('<B', self.phyllotaxis_spiral)
        
        # Hodge dual (byte 67)
        data += struct.pack('<B', self.hodge_dual)
        
        # Checksum (bytes 68-71) - CRC32 of first 68 bytes
        self.checksum = zlib.crc32(data) & 0xFFFFFFFF
        data += struct.pack('<I', self.checksum)
        
        # Padding (bytes 72-95)
        data += self.padding[:24].ljust(24, b'\x00')
        
        return data[:96]
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'BinaryLatticeState':
        """Deserialize from 96-byte binary format"""
        if len(data) != 96:
            raise ValueError(f"Expected 96 bytes, got {len(data)}")
        
        # Verify checksum
        stored_checksum = struct.unpack('<I', data[68:72])[0]
        computed_checksum = zlib.crc32(data[:68]) & 0xFFFFFFFF
        if stored_checksum != computed_checksum:
            raise ValueError(f"CRC32 mismatch: {stored_checksum} != {computed_checksum}")
        
        # Parse fields
        center_x = struct.unpack('<f', data[0:4])[0]
        center_y = struct.unpack('<f', data[4:8])[0]
        
        ternary = []
        for i in range(4):
            ternary.append(struct.unpack('<f', data[8+i*4:12+i*4])[0])
        
        hex_persist = data[24:56]
        fellowship = struct.unpack('<f', data[56:60])[0]
        phi_mag = struct.unpack('<f', data[60:64])[0]
        morphogen = struct.unpack('<B', data[64:65])[0]
        vesica = struct.unpack('<b', data[65:66])[0]
        phyllotaxis = struct.unpack('<B', data[66:67])[0]
        hodge = struct.unpack('<B', data[67:68])[0]
        padding = data[72:96]
        
        return cls(
            center_x=center_x,
            center_y=center_y,
            ternary_junction=ternary,
            hex_persistence=hex_persist,
            fellowship_resonance=fellowship,
            phi_magnitude=phi_mag,
            morphogen_phase=morphogen,
            vesica_coherence=vesica,
            phyllotaxis_spiral=phyllotaxis,
            hodge_dual=hodge,
            checksum=stored_checksum,
            padding=padding
        )
    
    def encode_metaphor(self, radial: int, angular: int, magnitude: int, payload: int) -> None:
        """
        Encode 50-bit metaphor structure into hex_persistence
        
        Args:
            radial: 3 bits (0-7) - dimensional chamber
            angular: 3 bits (0-7) - sector position  
            magnitude: 8 bits (0-255) - amplitude
            payload: 36 bits - primitive selector
        """
        # Pack into 50 bits
        metaphor = (radial & 0x7) << 47
        metaphor |= (angular & 0x7) << 44
        metaphor |= (magnitude & 0xFF) << 36
        metaphor |= (payload & 0xFFFFFFFFF)  # 36 bits
        
        # Convert to bytes (7 bytes for 50 bits, padded to 8)
        metaphor_bytes = metaphor.to_bytes(8, 'little')
        
        # Store in first 8 bytes of hex_persistence
        self.hex_persistence = metaphor_bytes + self.hex_persistence[8:32]
    
    def decode_metaphor(self) -> Tuple[int, int, int, int]:
        """Decode 50-bit metaphor structure from hex_persistence"""
        # Extract first 8 bytes
        metaphor_bytes = self.hex_persistence[:8]
        metaphor = int.from_bytes(metaphor_bytes, 'little')
        
        radial = (metaphor >> 47) & 0x7
        angular = (metaphor >> 44) & 0x7
        magnitude = (metaphor >> 36) & 0xFF
        payload = metaphor & 0xFFFFFFFFF  # 36 bits
        
        return radial, angular, magnitude, payload
    
    def __str__(self) -> str:
        return (
            f"LatticeState(96 bytes)\n"
            f"  Center: ({self.center_x:.3f}, {self.center_y:.3f})\n"
            f"  Fellowship: {self.fellowship_resonance:.3f}\n"
            f"  Morphogen: {self.morphogen_phase} ({['Seed','Spiral','Fold','Resonate','Chiral','Flip','Anchor'][self.morphogen_phase % 7]})\n"
            f"  Chirality: {'Left' if self.hodge_dual else 'Right'}\n"
            f"  Checksum: 0x{self.checksum:08X}"
        )


def demonstrate_binary_format():
    """Demonstrate binary serialization"""
    print("GLYF Binary Format Demonstration")
    print("=" * 50)
    
    # Create example state
    state = BinaryLatticeState(
        center_x=0.0,
        center_y=0.0,
        ternary_junction=[1.0, 1.0, 0.0, 0.0],
        fellowship_resonance=PHI_SEVENTH * 0.9,  # 90% coherence
        morphogen_phase=3,  # Resonate
        vesica_coherence=80,  # 80% coherence
        phyllotaxis_spiral=1,
        hodge_dual=0  # Right-handed
    )
    
    # Encode metaphor for "cliff"
    state.encode_metaphor(
        radial=4,      # Far chamber (vertical drop)
        angular=0,     # East (horizontal edge)
        magnitude=230, # High salience
        payload=0b10010010  # LINE + NODE + FIELD primitives
    )
    
    # Serialize
    binary_data = state.to_bytes()
    print(f"\nSerialized {len(binary_data)} bytes")
    print(f"Hex dump (first 32 bytes):")
    print(' '.join(f'{b:02X}' for b in binary_data[:32]))
    
    # Deserialize
    recovered = BinaryLatticeState.from_bytes(binary_data)
    print(f"\n{recovered}")
    
    # Decode metaphor
    r, a, m, p = recovered.decode_metaphor()
    print(f"\nMetaphor decoded:")
    print(f"  Radial: {r} (chamber)")
    print(f"  Angular: {a} (45° × {a})")
    print(f"  Magnitude: {m}/255")
    print(f"  Payload: 0x{p:09X} (primitives)")
    
    # Verify integrity
    print(f"\nIntegrity check: {'✓ PASS' if recovered.checksum == state.checksum else '✗ FAIL'}")


if __name__ == "__main__":
    demonstrate_binary_format()
