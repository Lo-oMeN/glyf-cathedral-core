"""
The Atlas Redrawn: Trinary-PGA Lattice
3×3×3×3×3 = 729 slots, each a 16D PGA multivector.

Systematic Correspondence:
- Contraction (−1): Meet (∧), grade collapse
- Void (0): Degenerate e₀ direction
- Expansion (+1): Join (∨), φ-scaled rotors

Embodied Orientation:
- Shells: Vertical (inner→middle→outer)
- Sectors: Forward (past→present→future)
- Sub-cells: Lateral (thesis↔antithesis↔void)

Ontological Projection:
Each slot = 16D PGA multivector with semantic density σ(g)
"""
import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from enum import IntEnum

# PHI and its powers
PHI = (1 + np.sqrt(5)) / 2
PHI_POWERS = [PHI ** i for i in range(-3, 4)]  # φ⁻³ to φ³

class Orientation(IntEnum):
    """Embodied orientation in 3D lattice space."""
    # Vertical (Shells)
    INNER = 0      # Foundational
    MIDDLE = 1     # Relational
    OUTER = 2      # Eschatological
    
    # Forward (Sectors)
    PAST = 0
    PRESENT = 1
    FUTURE = 2
    
    # Lateral (Sub-cells)
    THESIS = 0      # +1, Actualized, UP
    ANTITHESIS = 1  # -1, Null, DOWN
    VOID = 2        # 0, Potential, horizon

@dataclass
class LatticeAddress:
    """
    5-dimensional address in the trinary-PGA atlas.
    
    (shell, sector, sub_cell, bigram_x, bigram_y)
    
    shell:     0=inner, 1=middle, 2=outer (vertical elevation)
    sector:    0=past, 1=present, 2=future (forward motion)
    sub_cell:  0=thesis, 1=antithesis, 2=void (lateral force)
    bigram_x:  0-2 (first letter coordinate)
    bigram_y:  0-2 (second letter coordinate)
    """
    shell: int      # 0, 1, 2
    sector: int     # 0, 1, 2
    sub_cell: int   # 0, 1, 2
    bigram_x: int   # 0, 1, 2
    bigram_y: int   # 0, 1, 2
    
    def __post_init__(self):
        assert all(0 <= x <= 2 for x in [self.shell, self.sector, self.sub_cell, 
                                          self.bigram_x, self.bigram_y])
    
    @property
    def linear_index(self) -> int:
        """Flatten 5D address to 0-728.
        
        Order: shell (slowest) -> sector -> sub_cell -> bigram_x -> bigram_y (fastest)
        """
        return (self.shell * 81 + 
                self.sector * 27 + 
                self.sub_cell * 9 + 
                self.bigram_x * 3 + 
                self.bigram_y)
    
    @classmethod
    def from_linear(cls, idx: int) -> 'LatticeAddress':
        """Reconstruct 5D address from linear index."""
        assert 0 <= idx < 729
        # Little-endian: last dimension varies fastest
        # 729 = 3^6, but we only have 5 dimensions (3^5 = 243 per shell-group)
        # Shell uses divisor 243 to create 3 groups of 243
        bigram_y = idx % 3
        bigram_x = (idx // 3) % 3
        sub_cell = (idx // 9) % 3
        sector = (idx // 27) % 3
        shell = (idx // 243) % 3  # Fixed: was 81, should be 243
        return cls(shell, sector, sub_cell, bigram_x, bigram_y)
    
    @property
    def orientation_name(self) -> str:
        """Human-readable orientation."""
        shells = ['inner', 'middle', 'outer']
        sectors = ['past', 'present', 'future']
        sub_cells = ['thesis', 'antithesis', 'void']
        return f"{shells[self.shell]}-{sectors[self.sector]}-{sub_cells[self.sub_cell]}"
    
    @property
    def trinary_state(self) -> int:
        """
        Extract trinary state from sub_cell:
        thesis=+1, antithesis=-1, void=0
        """
        return {0: 1, 1: -1, 2: 0}[self.sub_cell]


class PGAMultivector16D:
    """
    16D PGA (Projective Geometric Algebra) multivector.
    
    Components indexed as:
    0: scalar (grade 0)
    1-4: vectors e₀, e₁, e₂, e₃ (grade 1)
    5-10: bivectors e₀₁, e₀₂, e₀₃, e₁₂, e₁₃, e₂₃ (grade 2)
    11-14: trivectors e₀₁₂, e₀₁₃, e₀₂₃, e₁₂₃ (grade 3)
    15: pseudoscalar e₀₁₂₃ (grade 4)
    """
    
    # Grade indices
    GRADE_INDICES = {
        0: [0],
        1: [1, 2, 3, 4],
        2: [5, 6, 7, 8, 9, 10],
        3: [11, 12, 13, 14],
        4: [15]
    }
    
    def __init__(self, values: Optional[np.ndarray] = None):
        self.values = np.zeros(16, dtype=np.float64) if values is None else values.copy()
        assert len(self.values) == 16
    
    @classmethod
    def from_trinary_state(cls, state: int, shell: int, sector: int, 
                           magnitude: float = 1.0) -> 'PGAMultivector16D':
        """
        Create multivector from trinary state and position.
        
        state: -1 (contraction), 0 (void), +1 (expansion)
        shell: 0-2 (inner to outer)
        sector: 0-2 (past to future)
        """
        mv = cls()
        phi_scale = PHI_POWERS[shell + 3]  # Map shell to φ^scale
        
        if state == 1:  # Expansion: join (∨), generates rotors
            # Create a simple rotor in e₁₂ plane
            angle = np.pi / 4 * phi_scale
            mv.values[0] = np.cos(angle / 2)  # Scalar
            mv.values[8] = np.sin(angle / 2)  # e₁₂ bivector
            
        elif state == -1:  # Contraction: meet (∧), grade collapse
            # Collapse toward e₀ (degenerate direction)
            mv.values[1] = magnitude * phi_scale  # e₀ vector
            
        else:  # state == 0: Void, encodes degenerate e₀
            # Pure degenerate direction
            mv.values[1] = magnitude * 0.618  # e₀ (degenerate)
            mv.values[0] = 0.382  # Scalar component
        
        # Sector modulation (temporal phase)
        phase = sector * (2 * np.pi / 3)
        mv.values[2] = magnitude * np.cos(phase) * phi_scale * 0.1  # e₁
        mv.values[3] = magnitude * np.sin(phase) * phi_scale * 0.1  # e₂
        
        return mv
    
    def meet(self, other: 'PGAMultivector16D') -> 'PGAMultivector16D':
        """
        Meet operation (∧): intersection of subspaces.
        Contraction operation for -1 states.
        """
        result = PGAMultivector16D()
        # Simplified: grade-2 components participate in meet
        for i in self.GRADE_INDICES[2]:
            result.values[i] = min(self.values[i], other.values[i])
        return result
    
    def join(self, other: 'PGAMultivector16D') -> 'PGAMultivector16D':
        """
        Join operation (∨): union of subspaces.
        Expansion operation for +1 states.
        """
        result = PGAMultivector16D()
        for i in range(16):
            result.values[i] = max(self.values[i], other.values[i])
        return result
    
    def geometric_product(self, other: 'PGAMultivector16D') -> 'PGAMultivector16D':
        """
        Full geometric product (simplified: grade-wise multiplication).
        """
        result = PGAMultivector16D()
        # Scalar product
        result.values[0] = self.values[0] * other.values[0]
        # Vector products (simplified)
        for i in range(1, 5):
            result.values[i] = self.values[0] * other.values[i] + self.values[i] * other.values[0]
        return result
    
    @property
    def scalar(self) -> float:
        return self.values[0]
    
    @property
    def norm(self) -> float:
        return np.linalg.norm(self.values)
    
    @property
    def coherence(self) -> float:
        """
        Coherence κ = scalar / ||multivector||
        Alignment with identity (Node0).
        """
        n = self.norm
        return self.scalar / n if n > 0 else 0.0


@dataclass
class LatticeCell:
    """
    A single cell in the 729-slot atlas.
    
    Stores:
    - 16D PGA multivector (the geometric content)
    - Bigram string (the linguistic content)
    - Semantic density σ(g) = H × C × D
    - Metadata (provenance, reliability, kenosis score)
    """
    address: LatticeAddress
    multivector: PGAMultivector16D
    bigram: str = ""
    semantic_density: float = 0.0
    entropy: float = 0.0  # H(g)
    coherence_score: float = 0.0  # C(g)
    dominance: float = 0.0  # D(g)
    # Metadata
    provenance_curator: str = ""
    reliability_sem: float = 1.0
    kenosis_fruit_score: float = 0.0
    
    def compute_semantic_density(self):
        """σ(g) = H(g) × C(g) × D(g)"""
        self.semantic_density = self.entropy * self.coherence_score * self.dominance


class TrinaryPGALattice:
    """
    The complete 729-slot atlas.
    
    27 positions (3 shells × 3 sectors × 3 sub-cells)
    × 27 bigram addresses (3×3 × 3×3)
    = 729 total slots
    
    53 spare slots reserved for:
    - 9 paraclete.keys (seamless_gate through thorn_crown)
    - 14 Greek lexemes (βασιλεία, μεριμνάω, etc.)
    - 30 metadata / system / expansion
    """
    
    SPARE_INDICES = list(range(676, 729))  # Last 53 slots
    
    # Special landmark mappings
    PARACLETE_KEYS = {
        'seamless_gate': 676,
        'water_into_wine': 677,
        'temple_cleansing': 678,
        'nicodemus_night': 679,
        'samaritan_well': 680,
        ' Bethesda_pool': 681,
        'five_loaves': 682,
        'walking_water': 683,
        'thorn_crown': 684,
    }
    
    GREEK_LEXEMES = {
        'βασιλεία': 685,    # shell-inner-thesis
        'ἐχθρός': 686,      # shell-inner-antithesis
        'ἀφίημι': 687,      # shell-inner-void
        'ταπεινόω': 688,    # shell-middle-thesis
        'μεριμνάω': 689,    # shell-middle-antithesis
        'καρδία': 690,      # shell-middle-void
        'σῶμα': 691,        # shell-outer-thesis
        'ἀνάστασις': 692,   # shell-outer-antithesis
        'δοῦλος': 693,      # shell-outer-void
        'ἀγάπη': 694,
        'εἰρήνη': 695,
        'χαρά': 696,
        'μακροθυμία': 697,
        'χρηστότης': 698,
    }
    
    def __init__(self):
        self.cells: Dict[int, LatticeCell] = {}
        self._initialize_lattice()
        self._initialize_landmarks()
    
    def _initialize_lattice(self):
        """Initialize all 729 slots with appropriate multivectors."""
        for idx in range(729):
            addr = LatticeAddress.from_linear(idx)
            
            # Create multivector from trinary state
            mv = PGAMultivector16D.from_trinary_state(
                state=addr.trinary_state,
                shell=addr.shell,
                sector=addr.sector
            )
            
            # Generate bigram string
            bigram = self._index_to_bigram(idx)
            
            # Compute initial semantic metrics
            entropy = self._compute_entropy(addr)
            coherence = abs(mv.coherence)
            dominance = abs(addr.trinary_state) if addr.trinary_state != 0 else 0.5
            
            cell = LatticeCell(
                address=addr,
                multivector=mv,
                bigram=bigram,
                entropy=entropy,
                coherence_score=coherence,
                dominance=dominance
            )
            cell.compute_semantic_density()
            
            self.cells[idx] = cell
    
    def _initialize_landmarks(self):
        """Initialize special landmark slots."""
        # βασιλεία at shell-inner-thesis (sovereignty)
        addr = LatticeAddress(0, 0, 0, 0, 0)  # inner-past-thesis
        idx = self.GREEK_LEXEMES['βασιλεία']
        if idx in self.cells:
            self.cells[idx].bigram = "βασιλεία"
            self.cells[idx].kenosis_fruit_score = 0.95
        
        # μεριμνάω at shell-middle-antithesis (anxiety/worry)
        addr = LatticeAddress(1, 1, 1, 1, 1)  # middle-present-antithesis
        idx = self.GREEK_LEXEMES['μεριμνάω']
        if idx in self.cells:
            self.cells[idx].bigram = "μεριμνάω"
            self.cells[idx].kenosis_fruit_score = 0.3
    
    def _index_to_bigram(self, idx: int) -> str:
        """Generate a bigram string from linear index."""
        if idx >= 676:
            return ""
        
        # Map to two letters (simplified: use printable ASCII)
        first = chr(ord('a') + (idx // 26) % 26)
        second = chr(ord('a') + (idx % 26))
        return first + second
    
    def _compute_entropy(self, addr: LatticeAddress) -> float:
        """
        Compute entropy based on position in lattice.
        Higher entropy at boundaries, lower at center.
        """
        # Distance from center of lattice
        center = np.array([1, 1, 1, 1, 1])
        pos = np.array([addr.shell, addr.sector, addr.sub_cell, 
                       addr.bigram_x, addr.bigram_y])
        dist = np.linalg.norm(pos - center)
        return 1.0 - (dist / 5.0)  # Normalize
    
    def lookup(self, bigram: str) -> Optional[LatticeCell]:
        """Find cell by bigram string."""
        for cell in self.cells.values():
            if cell.bigram == bigram:
                return cell
        return None
    
    def get_by_address(self, shell: int, sector: int, sub_cell: int,
                       bigram_x: int, bigram_y: int) -> LatticeCell:
        """Get cell by 5D address."""
        addr = LatticeAddress(shell, sector, sub_cell, bigram_x, bigram_y)
        return self.cells[addr.linear_index]
    
    def get_neighborhood(self, center_idx: int, radius: int = 1) -> List[LatticeCell]:
        """
        Get cells in neighborhood (Moore neighborhood in 5D).
        """
        center_addr = LatticeAddress.from_linear(center_idx)
        neighbors = []
        
        for ds in range(-radius, radius + 1):
            for dse in range(-radius, radius + 1):
                for dsc in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            try:
                                addr = LatticeAddress(
                                    max(0, min(2, center_addr.shell + ds)),
                                    max(0, min(2, center_addr.sector + dse)),
                                    max(0, min(2, center_addr.sub_cell + dsc)),
                                    max(0, min(2, center_addr.bigram_x + dx)),
                                    max(0, min(2, center_addr.bigram_y + dy))
                                )
                                neighbors.append(self.cells[addr.linear_index])
                            except (AssertionError, ValueError):
                                continue
        
        return neighbors
    
    def geometric_transform(self, input_mv: PGAMultivector16D, 
                           operation: str) -> PGAMultivector16D:
        """
        Geometric Transformer operation.
        
        Routes to rotation, projection, or intersection expert
        based on input multivector properties.
        """
        coherence = input_mv.coherence
        
        if operation == 'rotation':
            # Generate rotor for rotation
            angle = np.arccos(np.clip(coherence, -1, 1))
            rotor = PGAMultivector16D()
            rotor.values[0] = np.cos(angle / 2)
            rotor.values[8] = np.sin(angle / 2)  # e₁₂ plane rotation
            return input_mv.geometric_product(rotor)
        
        elif operation == 'projection':
            # Project onto scalar component
            projected = PGAMultivector16D()
            projected.values[0] = input_mv.scalar
            return projected
        
        elif operation == 'intersection':
            # Meet with canonical plane
            canonical = PGAMultivector16D()
            canonical.values[8] = 1.0  # e₁₂ plane
            return input_mv.meet(canonical)
        
        return input_mv
    
    def stats(self) -> dict:
        """Compute lattice statistics."""
        total = len(self.cells)
        occupied = sum(1 for c in self.cells.values() if c.bigram)
        
        coherences = [c.multivector.coherence for c in self.cells.values()]
        densities = [c.semantic_density for c in self.cells.values()]
        
        return {
            'total_slots': total,
            'occupied_slots': occupied,
            'spare_slots': len(self.SPARE_INDICES),
            'mean_coherence': np.mean(coherences),
            'mean_semantic_density': np.mean(densities),
            'max_density_cell': max(self.cells.values(), key=lambda c: c.semantic_density).bigram
        }


def test_atlas():
    """Test the redrawn atlas."""
    print("=== THE ATLAS REDRAWN ===\n")
    
    lattice = TrinaryPGALattice()
    stats = lattice.stats()
    
    print(f"Lattice Statistics:")
    print(f"  Total slots: {stats['total_slots']}")
    print(f"  Occupied bigram slots: {stats['occupied_slots']}")
    print(f"  Spare landmark slots: {stats['spare_slots']}")
    print(f"  Mean coherence: {stats['mean_coherence']:.4f}")
    print(f"  Mean semantic density: {stats['mean_semantic_density']:.4f}")
    print()
    
    # Sample cells
    print("Sample Cells:")
    sample_indices = [0, 13, 42, 100, 350, 675]
    for idx in sample_indices:
        cell = lattice.cells[idx]
        addr = cell.address
        print(f"  [{idx:3d}] {cell.bigram:3s} @ {addr.orientation_name:20s} "
              f"κ={cell.multivector.coherence:+.3f} σ={cell.semantic_density:.3f}")
    
    print()
    
    # Landmarks
    print("Landmark Cells:")
    for name, idx in list(lattice.GREEK_LEXEMES.items())[:5]:
        cell = lattice.cells[idx]
        print(f"  {name}: κ={cell.multivector.coherence:.3f}, "
              f"fruit_score={cell.kenosis_fruit_score:.2f}")
    
    print()
    
    # Geometric transformation
    print("Geometric Transformation Test:")
    test_mv = PGAMultivector16D.from_trinary_state(1, 1, 1)  # expansion
    print(f"  Input:  κ={test_mv.coherence:.3f}")
    
    rotated = lattice.geometric_transform(test_mv, 'rotation')
    print(f"  Rotated: κ={rotated.coherence:.3f}")
    
    projected = lattice.geometric_transform(test_mv, 'projection')
    print(f"  Projected: κ={projected.coherence:.3f}")
    
    intersected = lattice.geometric_transform(test_mv, 'intersection')
    print(f"  Intersected: κ={intersected.coherence:.3f}")
    
    print("\n=== ATLAS ACTIVE ===")


if __name__ == "__main__":
    test_atlas()
