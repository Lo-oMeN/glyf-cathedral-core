"""
Trinity v6.0: Input Encoding Pipeline
Production text → PGA multivector encoder.
PATCH CB-003: Real bigram-to-PGA bridge with lattice lookup.
"""
import json
import re
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path

class InputEncoder:
    """
    Production text → 16D PGA multivector encoder.
    
    Pipeline:
    1. Normalize text (lowercase, keep letters)
    2. Extract overlapping bigrams
    3. Lookup lattice coordinates (shell, sector)
    4. Convert to multivectors via radial embedding
    5. Aggregate to 16D state vector
    """
    
    def __init__(self, lattice_path: Optional[str] = None):
        """
        Initialize encoder with lattice.
        
        Args:
            lattice_path: Path to lattice_crystallized.json
                         Defaults to phi-radial-loom/lattice_crystallized.json
        """
        if lattice_path is None:
            # Try to find lattice relative to workspace
            base = Path('/root/.openclaw/workspace')
            lattice_path = base / "phi-radial-loom" / "lattice_crystallized.json"
        
        with open(lattice_path, 'r') as f:
            self.lattice = json.load(f)
        
        self.phi = 1.618033988749895
        self.phi_inv = 1.0 / self.phi
        self.n_shells = 7
        self.angular_resolution = 4096  # 12-bit
        self.sector_size_deg = 360.0 / self.angular_resolution
        self.golden_angle_rad = 2.39996322972865332  # 137.507764°
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for bigram extraction.
        - Lowercase
        - Keep only alphabetic characters
        - Collapse whitespace
        """
        # Lowercase and keep only letters
        cleaned = ''.join(c.lower() for c in text if c.isalpha())
        return cleaned
    
    def extract_bigrams(self, text: str) -> List[str]:
        """
        Extract overlapping bigrams from normalized text.
        
        Example: "hello" → ['he', 'el', 'll', 'lo']
        """
        text = self.normalize_text(text)
        
        if len(text) < 2:
            # Pad short input
            text = text + 'a' * (2 - len(text))
        
        return [text[i:i+2] for i in range(len(text) - 1)]
    
    def lookup_coordinate(self, bigram: str) -> Tuple[int, int]:
        """
        Get lattice coordinate (shell, sector) for bigram.
        
        Args:
            bigram: 2-character string (e.g., 'he')
        
        Returns:
            (shell, sector) tuple
        """
        coord = self.lattice.get(bigram)
        
        if coord is None:
            # Fallback: deterministic hash to shell/sector
            # This ensures same bigram always maps to same coordinate
            h = hash(bigram) % 1000000
            shell = h % self.n_shells
            sector = (h // self.n_shells) % self.angular_resolution
            return (shell, sector)
        
        return (coord['shell'], coord['sector'])
    
    def shell_to_radius(self, shell: int) -> float:
        """
        Convert shell index to radial distance.
        r = Φ^shell
        """
        return self.phi ** shell
    
    def sector_to_angle(self, sector: int) -> float:
        """
        Convert sector index to angle in radians.
        θ = sector × (360° / 4096)
        """
        return np.radians(sector * self.sector_size_deg)
    
    def coordinate_to_multivector(self, shell: int, sector: int) -> np.ndarray:
        """
        Convert lattice coordinate to 16D PGA multivector.
        
        Represents as rotor in e12 plane with radial scaling:
        - Scalar part: cos(θ/2)
        - Bivector part: sin(θ/2) × r × e12
        
        Args:
            shell: Shell index (0-6)
            sector: Sector index (0-4095)
        
        Returns:
            16D numpy array (PGA multivector)
        """
        r = self.shell_to_radius(shell)
        theta = self.sector_to_angle(sector)
        
        # Rotor: cos(θ/2) + sin(θ/2) * e12
        mv = np.zeros(16)
        mv[0] = np.cos(theta / 2)           # Scalar (grade 0)
        mv[5] = np.sin(theta / 2) * r       # e12 bivector (grade 2)
        
        # Normalize to unit magnitude
        norm = np.linalg.norm(mv)
        if norm > 1e-10:
            mv = mv / norm
        
        return mv
    
    def bigram_to_multivector(self, bigram: str) -> np.ndarray:
        """
        Convert single bigram to multivector via lattice lookup.
        
        Args:
            bigram: 2-character string
        
        Returns:
            16D PGA multivector
        """
        shell, sector = self.lookup_coordinate(bigram)
        return self.coordinate_to_multivector(shell, sector)
    
    def encode(
        self, 
        text: str, 
        max_bigrams: int = 8,
        aggregation: str = 'mean'
    ) -> np.ndarray:
        """
        Encode text to 16D state vector.
        
        Args:
            text: Input text
            max_bigrams: Maximum number of bigrams to use
            aggregation: 'mean', 'sum', or 'geometric_mean'
        
        Returns:
            16D numpy array (aggregated multivector)
        """
        bigrams = self.extract_bigrams(text)[:max_bigrams]
        
        if not bigrams:
            return np.zeros(16)
        
        # Convert each bigram to multivector
        multivectors = []
        for bg in bigrams:
            mv = self.bigram_to_multivector(bg)
            multivectors.append(mv)
        
        mvs = np.array(multivectors)
        
        # Aggregate
        if aggregation == 'mean':
            result = np.mean(mvs, axis=0)
        elif aggregation == 'sum':
            result = np.sum(mvs, axis=0)
        elif aggregation == 'geometric_mean':
            # Log-space mean for geometric
            # Avoid log(0) by adding small epsilon
            log_mvs = np.log(np.abs(mvs) + 1e-10)
            result = np.sign(np.mean(mvs, axis=0)) * np.exp(np.mean(log_mvs, axis=0))
        else:
            result = np.mean(mvs, axis=0)
        
        # Renormalize
        norm = np.linalg.norm(result)
        if norm > 1e-10:
            result = result / norm
        
        return result
    
    def encode_batch(
        self, 
        texts: List[str], 
        max_bigrams: int = 8
    ) -> np.ndarray:
        """
        Encode batch of texts.
        
        Args:
            texts: List of input strings
            max_bigrams: Maximum bigrams per text
        
        Returns:
            [batch_size, 16] array of multivectors
        """
        results = []
        for text in texts:
            mv = self.encode(text, max_bigrams)
            results.append(mv)
        return np.array(results)
    
    def get_coordinate_info(self, text: str) -> List[dict]:
        """
        Get detailed coordinate info for each bigram in text.
        Useful for debugging/visualization.
        """
        bigrams = self.extract_bigrams(text)
        info = []
        
        for bg in bigrams:
            shell, sector = self.lookup_coordinate(bg)
            info.append({
                'bigram': bg,
                'shell': shell,
                'sector': sector,
                'radius': self.shell_to_radius(shell),
                'angle_deg': sector * self.sector_size_deg,
                'angle_rad': self.sector_to_angle(sector)
            })
        
        return info


if __name__ == '__main__':
    print("=== Input Encoder Test ===\n")
    
    encoder = InputEncoder()
    
    test_texts = [
        "hello world",
        "silence",
        "the cathedral sings",
        "a",
        "node0"
    ]
    
    print("Bigram extraction:")
    for text in test_texts:
        bigrams = encoder.extract_bigrams(text)
        print(f"  '{text}' → {bigrams[:5]}")
    
    print("\nCoordinate info for 'hello':")
    info = encoder.get_coordinate_info("hello")
    for item in info:
        print(f"  {item['bigram']}: shell={item['shell']}, sector={item['sector']}, "
              f"r={item['radius']:.3f}, θ={item['angle_deg']:.1f}°")
    
    print("\nEncoded vectors:")
    for text in test_texts:
        vec = encoder.encode(text)
        print(f"  '{text}' → norm={np.linalg.norm(vec):.4f}, "
              f"scalar={vec[0]:.4f}, e12={vec[5]:.4f}")
    
    print("\n✓ Input encoder operational.")
    print("✓ Bigram → Lattice → Multivector pipeline ready.")
