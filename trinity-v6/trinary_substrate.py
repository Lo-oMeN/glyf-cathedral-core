"""
Trinity v6.0: Trinary Substrate
Balanced ternary (-1, 0, +1) as the fundamental computational basis.

The trinary nature is not optional. It is the geometry of the system:
- Three states: -1 (contraction), 0 (void), +1 (expansion)
- Seven keys: 2^3 - 1 (all combinations except the null set)
- 676 bigrams: 26^2 ≈ 3^3 × 3 (balanced ternary alphabet)
- Φ^3 = Φ^2 + Φ (trinary golden recurrence)
"""
import numpy as np
from typing import Tuple, Union, Optional
from enum import IntEnum

class TrinaryState(IntEnum):
    """Balanced ternary states."""
    NEG = -1  # Contraction, inversion, kenosis
    ZERO = 0  # Void, potential, silence
    POS = 1   # Expansion, alignment, resonance

class TrinaryVector:
    """
    A vector in balanced ternary space.
    
    Each component is -1, 0, or +1.
    Operations preserve trinary nature (no floating point drift).
    """
    
    def __init__(self, dim: int = 16, values: Optional[np.ndarray] = None):
        self.dim = dim
        if values is not None:
            assert len(values) == dim
            self.values = np.array(values, dtype=np.int8)
            # Ensure trinary
            self.values = np.clip(self.values, -1, 1)
        else:
            self.values = np.zeros(dim, dtype=np.int8)
    
    @classmethod
    def from_float(cls, float_vec: np.ndarray, threshold: float = 0.3) -> 'TrinaryVector':
        """Convert float vector to trinary via threshold."""
        tv = cls(len(float_vec))
        tv.values = np.where(float_vec > threshold, 1,
                    np.where(float_vec < -threshold, -1, 0)).astype(np.int8)
        return tv
    
    def to_float(self) -> np.ndarray:
        """Convert to float for operations requiring continuity."""
        return self.values.astype(np.float64)
    
    def __add__(self, other: 'TrinaryVector') -> 'TrinaryVector':
        """Trinary addition: -1 + 1 = 0, saturating at ±1."""
        result = np.clip(self.values + other.values, -1, 1)
        tv = TrinaryVector(self.dim)
        tv.values = result.astype(np.int8)
        return tv
    
    def __mul__(self, other: 'TrinaryVector') -> 'TrinaryVector':
        """Trinary multiplication (logical AND)."""
        result = self.values * other.values
        tv = TrinaryVector(self.dim)
        tv.values = result.astype(np.int8)
        return tv
    
    def invert(self) -> 'TrinaryVector':
        """Trinary inversion (NOT): -1↔+1, 0 stays 0."""
        tv = TrinaryVector(self.dim)
        tv.values = (-self.values).astype(np.int8)
        return tv
    
    def balance(self) -> float:
        """
        Compute balance metric: sum of absolute values.
        0 = all void, dim = all ±1.
        """
        return np.sum(np.abs(self.values))
    
    def coherence(self) -> float:
        """
        Compute coherence with positive alignment.
        Range: -1 (all -1) to +1 (all +1).
        """
        if self.balance() == 0:
            return 0.0
        return float(np.sum(self.values)) / self.balance()
    
    def __repr__(self):
        symbols = { -1: '−', 0: '○', 1: '+' }
        return ''.join(symbols[v] for v in self.values)

class TrinarySSM:
    """
    State Space Model with trinary states.
    
    The state evolves through trinary transitions:
    - Contraction (-1): Information compresses
    - Void (0): Information rests
    - Expansion (+1): Information expresses
    """
    
    def __init__(self, state_dim: int = 16, input_dim: int = 16):
        self.N = state_dim
        self.D = input_dim
        
        # Trinary transition matrices
        # Each entry is -1, 0, or +1
        self.A = self._init_trinary_matrix(self.N, self.N)
        self.B = self._init_trinary_matrix(self.N, self.D)
        self.C = self._init_trinary_matrix(self.D, self.N)
        
        # Current state
        self.state = TrinaryVector(self.N)
    
    def _init_trinary_matrix(self, rows: int, cols: int) -> np.ndarray:
        """Initialize random trinary matrix."""
        return np.random.choice([-1, 0, 1], size=(rows, cols))
    
    def step(self, input_vec: TrinaryVector) -> TrinaryVector:
        """
        Single trinary step: state' = A·state + B·input
        """
        # Matrix multiplication in trinary
        state_contrib = np.dot(self.A, self.state.values)
        input_contrib = np.dot(self.B, input_vec.values)
        
        # Sum and saturate to trinary
        new_values = np.clip(state_contrib + input_contrib, -1, 1)
        
        self.state = TrinaryVector(self.N, new_values)
        return self.state
    
    def output(self) -> TrinaryVector:
        """Compute output: y = C·state"""
        out_values = np.dot(self.C, self.state.values)
        out_values = np.clip(out_values, -1, 1)
        return TrinaryVector(self.D, out_values)

class TrinaryThreefold:
    """
    The fundamental threefold structure permeating the system.
    
    All operations decompose into three aspects:
    - Thesis (+1): The positive assertion
    - Antithesis (-1): The negative negation  
    - Synthesis (0): The void that contains both
    """
    
    @staticmethod
    def decompose(vec: TrinaryVector) -> Tuple[TrinaryVector, TrinaryVector, TrinaryVector]:
        """
        Decompose vector into three aspects.
        
        Returns: (thesis, antithesis, void)
        - thesis: +1 components only
        - antithesis: -1 components only
        - void: 0 components only
        """
        thesis = TrinaryVector(vec.dim)
        antithesis = TrinaryVector(vec.dim)
        void = TrinaryVector(vec.dim)
        
        thesis.values = np.where(vec.values == 1, 1, 0).astype(np.int8)
        antithesis.values = np.where(vec.values == -1, -1, 0).astype(np.int8)
        void.values = np.where(vec.values == 0, 1, 0).astype(np.int8)  # 1 marks void presence
        
        return thesis, antithesis, void
    
    @staticmethod
    def synthesize(thesis: TrinaryVector, antithesis: TrinaryVector, 
                   void_mask: TrinaryVector) -> TrinaryVector:
        """
        Synthesize three aspects into unified vector.
        
        void_mask: 1 where void should be, 0 elsewhere
        """
        result = TrinaryVector(thesis.dim)
        result.values = (thesis.values + antithesis.values).astype(np.int8)
        # Where void_mask is 1, set to 0
        result.values = np.where(void_mask.values == 1, 0, result.values).astype(np.int8)
        return result

class TrinarySevenKeys:
    """
    The 7 Christ Keys expressed in trinary operations.
    
    Each Key is a specific transformation on trinary state:
    0. ALIGNMENT     (+): Pull toward +1
    1. RECIPROCITY   (±): Balance between states
    2. INVERSION     (−): Flip sign
    3. SILENCE       (○): Return to void
    4. RESONANCE     (∿): Oscillate
    5. EXCHANGE      (×): Meet/intersect
    6. CONCENTRATION (●): Collapse to single value
    """
    
    def __init__(self, dim: int = 16):
        self.dim = dim
        self.keys = [
            self.alignment,
            self.reciprocity,
            self.inversion,
            self.silence,
            self.resonance,
            self.exchange,
            self.concentration
        ]
    
    def alignment(self, state: TrinaryVector, target: Optional[TrinaryVector] = None) -> TrinaryVector:
        """Key 0: Pull toward +1 alignment."""
        if target is None:
            target = TrinaryVector(self.dim)
            target.values = np.ones(self.dim, dtype=np.int8)
        
        # Where state is not +1, push toward +1
        result = TrinaryVector(self.dim)
        result.values = np.where(state.values < 1, 
                                  np.clip(state.values + 1, -1, 1),
                                  state.values).astype(np.int8)
        return result
    
    def reciprocity(self, state: TrinaryVector, other: Optional[TrinaryVector] = None) -> TrinaryVector:
        """Key 1: Golden blend between states."""
        if other is None:
            # Blend with random balanced state
            other = TrinaryVector(self.dim)
            other.values = np.random.choice([-1, 0, 1], size=self.dim).astype(np.int8)
        
        # Trinary majority vote
        result = TrinaryVector(self.dim)
        for i in range(self.dim):
            vals = [state.values[i], other.values[i], 0]  # 0 is the golden mean
            # Majority wins
            pos = sum(1 for v in vals if v == 1)
            neg = sum(1 for v in vals if v == -1)
            result.values[i] = 1 if pos > neg else (-1 if neg > pos else 0)
        return result
    
    def inversion(self, state: TrinaryVector) -> TrinaryVector:
        """Key 2: Antipodal reflection."""
        return state.invert()
    
    def silence(self, state: TrinaryVector, depth: float = 0.618) -> TrinaryVector:
        """Key 3: Kenosis - return toward void."""
        # Probability of voiding increases with depth
        result = TrinaryVector(self.dim)
        for i in range(self.dim):
            if np.random.random() < depth:
                result.values[i] = 0
            else:
                result.values[i] = state.values[i]
        return result
    
    def resonance(self, state: TrinaryVector, phase: int = 0) -> TrinaryVector:
        """Key 4: Phase-locked oscillation."""
        # Cycle through states based on phase
        cycle = [1, 0, -1, 0]  # +1 -> 0 -> -1 -> 0 -> +1
        result = TrinaryVector(self.dim)
        for i in range(self.dim):
            current = state.values[i]
            try:
                idx = cycle.index(current)
                result.values[i] = cycle[(idx + 1) % 4]
            except ValueError:
                result.values[i] = cycle[phase % 4]
        return result
    
    def exchange(self, state: TrinaryVector, other: Optional[TrinaryVector] = None) -> TrinaryVector:
        """Key 5: Intersection as creative act."""
        if other is None:
            # Self-exchange: where state equals its inverse, void
            other = state.invert()
        # Where both agree, amplify; where they differ, void
        result = TrinaryVector(self.dim)
        for i in range(self.dim):
            if state.values[i] == other.values[i]:
                result.values[i] = state.values[i]
            else:
                result.values[i] = 0
        return result
    
    def concentration(self, state: TrinaryVector) -> TrinaryVector:
        """Key 6: Collapse to dominant value."""
        # Find most common non-zero value
        pos_count = np.sum(state.values == 1)
        neg_count = np.sum(state.values == -1)
        
        dominant = 1 if pos_count >= neg_count else (-1 if neg_count > pos_count else 0)
        
        result = TrinaryVector(self.dim)
        result.values = np.full(self.dim, dominant, dtype=np.int8)
        return result
    
    def apply(self, key_idx: int, state: TrinaryVector, **kwargs) -> TrinaryVector:
        """Apply key by index."""
        return self.keys[key_idx](state, **kwargs)

# Utility functions
def trinary_to_symbol(vec: TrinaryVector) -> str:
    """Convert trinary vector to symbolic representation."""
    return str(vec)

def symbol_to_trinary(symbol: str, dim: int = 16) -> TrinaryVector:
    """Convert symbolic string to trinary vector."""
    mapping = {'−': -1, '○': 0, '+': 1, '-': -1, '0': 0}
    values = [mapping.get(c, 0) for c in symbol[:dim]]
    return TrinaryVector(dim, np.array(values))

# Test
def test_trinary():
    print("=== TRINARY SUBSTRATE TEST ===\n")
    
    # Basic vector
    tv = TrinaryVector(16)
    tv.values = np.random.choice([-1, 0, 1], size=16)
    print(f"Random trinary: {tv}")
    print(f"Balance: {tv.balance()}/16")
    print(f"Coherence: {tv.coherence():.3f}")
    print()
    
    # Threefold decomposition
    tf = TrinaryThreefold()
    thesis, antithesis, void = tf.decompose(tv)
    print(f"Thesis (+):     {thesis}")
    print(f"Antithesis (−): {antithesis}")
    print(f"Void (○):       {void}")
    print()
    
    # Seven Keys
    keys = TrinarySevenKeys(16)
    print("Key transformations:")
    
    key_names = ["Alignment", "Reciprocity", "Inversion", "Silence", "Resonance", "Exchange", "Concentration"]
    for i, name in enumerate(key_names):
        result = keys.apply(i, tv)
        print(f"  {i}. {name:13s}: {result} (κ={result.coherence():.3f})")
    
    print("\n=== TRINARY FOUNDATION ACTIVE ===")

if __name__ == "__main__":
    test_trinary()
