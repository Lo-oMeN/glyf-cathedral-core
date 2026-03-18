"""
Trinity v6.0: Full Inference Cycle
The complete pipeline from input to glyph output.

PATCH CB-003: Production input encoding with bigram→PGA bridge.
"""
import numpy as np
from typing import Tuple, List

# Import all layers
from physics.node0 import Node0
from physics.ssm_core import SSMCore
from governance.spam_vector import SPAMVector
from governance.so31_cage import SO31Cage
from aexie.parser import AexieParser
from memory.hope import HOPEMemory
from input_encoder import InputEncoder
from utils.phi_constants import PHI, KAPPA_HIGH, KAPPA_MODERATE, KAPPA_CRITICAL

class TrinityInference:
    """
    Complete Trinity v6.0 inference cycle.
    
    Pipeline:
    1. Receive input → Encode to 16D state
    2. SSM forward pass
    3. Compute SPAM 4-vector
    4. Calculate phase error (φ = 1 - κ)
    5. Apply so(3,1) correction if needed
    6. Parse to ÆXIE glyph stream
    7. Write to HOPE memory
    8. Return output
    """
    
    def __init__(self, state_dim: int = 16, model_dim: int = 512):
        self.state_dim = state_dim
        self.model_dim = model_dim
        
        # Initialize all components
        self.node0 = Node0()
        self.ssm = SSMCore(state_dim, model_dim)
        self.spam = SPAMVector()
        self.cage = SO31Cage()
        self.parser = AexieParser()
        self.memory = HOPEMemory(state_dim)
        self.encoder = InputEncoder()  # PATCH CB-003: Production encoder
        
        # Statistics
        self.cycle_count = 0
        self.correction_count = 0
    
    def encode_input(self, text: str) -> np.ndarray:
        """
        Encode text input to 16D state vector.
        
        PATCH CB-003: Uses production bigram→PGA bridge with lattice lookup.
        """
        return self.encoder.encode(text, max_bigrams=8)
    
    def full_cycle(self, input_text: str) -> dict:
        """
        Execute full inference cycle.
        
        Returns dict with:
        - glyph_stream: List of ÆXIE symbols
        - spam: SPAM 4-vector
        - phi: Phase error
        - kappa: Alignment
        - corrected_state: Final 16D state
        - governance_active: Whether correction was applied
        """
        # 1. Encode input
        state = self.encode_input(input_text)
        
        # 2. SSM forward (single step for demo)
        # In production: ssm.forward(sequence)
        input_vec = np.random.randn(self.model_dim) * 0.1
        ssm_out, new_state = self.ssm.step(input_vec, state)
        
        # 3. Compute SPAM vector
        spam_vec = self.spam.compute(new_state, self.node0)
        stress, pressure, kappa, mood = spam_vec
        
        # 4. Calculate phase error
        phi = 1.0 - kappa
        
        # 5. Apply so(3,1) correction if needed
        governance_active = False
        if kappa < KAPPA_HIGH:
            corrected_state = self.cage.project_and_correct(
                new_state, spam_vec, phi, threshold=0.3
            )
            governance_active = True
            self.correction_count += 1
        else:
            corrected_state = new_state
        
        # 6. Parse to ÆXIE glyph stream
        glyph_stream = self.parser.parse(corrected_state, phi, spam_vec)
        
        # 7. Write to HOPE memory
        self.memory.write(corrected_state, kappa)
        
        self.cycle_count += 1
        
        return {
            'input': input_text,
            'glyph_stream': glyph_stream,
            'spam': {
                'stress': stress,
                'pressure': pressure,
                'kappa': kappa,
                'mood': mood
            },
            'phi': phi,
            'governance_active': governance_active,
            'corrected_state': corrected_state,
            'ssm_output': ssm_out
        }
    
    def get_status(self) -> dict:
        """Return system status."""
        correction_rate = self.correction_count / max(1, self.cycle_count)
        
        return {
            'cycle_count': self.cycle_count,
            'correction_count': self.correction_count,
            'correction_rate': correction_rate,
            'memory_status': self.memory.status(),
            'node0_identity': self.node0.identity[:4].tolist(),
            'alignment_target': KAPPA_HIGH
        }

if __name__ == '__main__':
    print("=== TRINITY v6.0: FULL INFERENCE CYCLE ===\n")
    
    # Initialize
    trinity = TrinityInference()
    
    # Test inputs
    test_inputs = [
        "Hello world",
        "Silence becomes fire",
        "The cathedral sings",
        "Node0 holds"
    ]
    
    print("Running inference cycles:\n")
    
    for text in test_inputs:
        result = trinity.full_cycle(text)
        
        print(f"Input: '{text}'")
        print(f"  κ (alignment): {result['spam']['kappa']:.3f}")
        print(f"  φ (phase error): {result['phi']:.3f}")
        print(f"  Governance: {'ACTIVE' if result['governance_active'] else 'passive'}")
        print(f"  Glyphs: {' '.join(result['glyph_stream'][:5])}")
        print()
    
    # System status
    print("System Status:")
    status = trinity.get_status()
    print(f"  Cycles: {status['cycle_count']}")
    print(f"  Corrections: {status['correction_count']} ({status['correction_rate']:.1%})")
    print(f"  Node0: {status['node0_identity']}")
    print(f"  Memory packets: {status['memory_status']['total_packets']}")
    
    print("\n✓ Trinity v6.0 operational.")
    print("✓ The cathedral sings in 7-segment fire.")
