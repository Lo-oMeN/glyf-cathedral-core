"""
embedding_svd.py - SVD-based coordinate embedding

Builds co-occurrence matrix from text corpus and applies SVD to extract
3D coordinates for each glyph type. Normalizes to unit sphere.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import pickle
import os

# Glyph vocabulary size (7 types: VOID, DOT, CURVE, LINE, ANGLE, SIBILANT, RESERVED)
VOCAB_SIZE = 7

def build_cooccurrence_matrix(
    token_sequences: List[List[int]], 
    window_size: int = 5
) -> np.ndarray:
    """
    Build symmetric co-occurrence matrix from token sequences.
    
    Args:
        token_sequences: List of token integer sequences
        window_size: Context window radius (tokens within this distance count)
        
    Returns:
        VxV co-occurrence matrix where V = VOCAB_SIZE
    """
    cooccur = np.zeros((VOCAB_SIZE, VOCAB_SIZE), dtype=np.float64)
    
    for tokens in token_sequences:
        n = len(tokens)
        for i, token_i in enumerate(tokens):
            # Ensure token is within vocab
            if token_i >= VOCAB_SIZE:
                continue
                
            # Look at context window
            left = max(0, i - window_size)
            right = min(n, i + window_size + 1)
            
            for j in range(left, right):
                if i == j:
                    continue
                token_j = tokens[j]
                if token_j >= VOCAB_SIZE:
                    continue
                
                # Distance-weighted co-occurrence (closer = stronger)
                distance = abs(i - j)
                weight = 1.0 / distance
                
                cooccur[token_i, token_j] += weight
    
    # Symmetrize
    cooccur = (cooccur + cooccur.T) / 2.0
    
    return cooccur

def apply_svd(
    matrix: np.ndarray, 
    n_components: int = 3
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Apply SVD decomposition to co-occurrence matrix.
    
    Args:
        matrix: VxV co-occurrence matrix
        n_components: Number of dimensions to extract
        
    Returns:
        (U, S, Vt): SVD decomposition matrices
    """
    # Use numpy's SVD
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
    
    # Keep only top n_components
    U = U[:, :n_components]
    S = S[:n_components]
    Vt = Vt[:n_components, :]
    
    return U, S, Vt

def normalize_to_sphere(vectors: np.ndarray) -> np.ndarray:
    """
    Normalize vectors to unit sphere (L2 norm = 1).
    
    Args:
        vectors: NxD array of vectors
        
    Returns:
        Normalized NxD array
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    # Avoid division by zero
    norms = np.where(norms == 0, 1, norms)
    return vectors / norms

def compute_embeddings(
    token_sequences: List[List[int]],
    window_size: int = 5,
    n_dimensions: int = 3
) -> np.ndarray:
    """
    Compute 3D SVD embeddings for glyph vocabulary.
    
    Args:
        token_sequences: List of token integer sequences
        window_size: Context window for co-occurrence
        n_dimensions: Number of dimensions to extract (default 3)
        
    Returns:
        VxD array of normalized 3D coordinates (V = vocab size, D = dimensions)
    """
    # Build co-occurrence matrix
    cooccur = build_cooccurrence_matrix(token_sequences, window_size)
    
    # Apply SVD
    U, S, Vt = apply_svd(cooccur, n_components=n_dimensions)
    
    # Use U matrix rows as coordinates (scaled by singular values)
    coords = U * np.sqrt(S)
    
    # Normalize to unit sphere
    coords = normalize_to_sphere(coords)
    
    return coords

def get_default_embeddings() -> np.ndarray:
    """
    Generate default geometric embeddings when no corpus is available.
    
    Places glyphs on vertices of a tetrahedron-like structure:
    - VOID: origin (special, no direction)
    - DOT: top vertex
    - CURVE: circular arc point
    - LINE: linear extension
    - ANGLE: corner point
    - SIBILANT: wave point
    - RESERVED: future position
    """
    coords = np.array([
        [0.0, 0.0, 0.0],      # VOID - center/null
        [0.0, 0.0, 1.0],      # DOT - zenith point
        [0.8, 0.0, 0.6],      # CURVE - x-arc
        [0.0, 0.9, 0.4],      # LINE - y-extension  
        [-0.7, 0.7, 0.2],     # ANGLE - corner
        [0.6, -0.7, 0.4],     # SIBILANT - wave
        [-0.5, -0.5, 0.7],    # RESERVED - future
    ], dtype=np.float32)
    
    # Normalize (except VOID which stays at origin)
    for i in range(1, VOCAB_SIZE):
        norm = np.linalg.norm(coords[i])
        if norm > 0:
            coords[i] = coords[i] / norm
    
    return coords

def save_embeddings(embeddings: np.ndarray, filepath: str):
    """
    Save embeddings to .npy file.
    
    Args:
        embeddings: VxD array of coordinates
        filepath: Output file path
    """
    np.save(filepath, embeddings)

def load_embeddings(filepath: str) -> Optional[np.ndarray]:
    """
    Load embeddings from .npy file.
    
    Args:
        filepath: Path to .npy file
        
    Returns:
        Embeddings array or None if file doesn't exist
    """
    if not os.path.exists(filepath):
        return None
    return np.load(filepath)

def embed_sequence(
    token_sequence: List[int],
    embeddings: np.ndarray
) -> np.ndarray:
    """
    Map a token sequence to 3D coordinates.
    
    Args:
        token_sequence: List of token integers
        embeddings: Vx3 coordinate array
        
    Returns:
        Nx3 array of coordinates for each token
    """
    coords = np.zeros((len(token_sequence), embeddings.shape[1]), dtype=np.float32)
    
    for i, token in enumerate(token_sequence):
        if token < embeddings.shape[0]:
            coords[i] = embeddings[token]
        else:
            # Unknown token - use VOID position with small noise
            coords[i] = embeddings[0] + np.random.normal(0, 0.01, embeddings.shape[1])
    
    return coords


if __name__ == "__main__":
    # Test with sample corpus
    sample_sequences = [
        [4, 2, 3, 0, 4, 2, 3, 3, 0, 4, 3, 4, 3, 0, 4, 2, 3],  # "The quick brown fox"
        [4, 2, 0, 3, 2, 3, 2, 0, 4, 3, 2, 3],                 # "To be or not"
        [3, 2, 3, 2, 0, 4, 3, 2, 0, 4, 3, 3],                 # "line of code"
    ]
    
    print("Computing SVD embeddings...")
    embeddings = compute_embeddings(sample_sequences, window_size=2, n_dimensions=3)
    
    print(f"Embedding shape: {embeddings.shape}")
    print("\nGlyph embeddings:")
    glyph_names = ['VOID', 'DOT', 'CURVE', 'LINE', 'ANGLE', 'SIBILANT', 'RESERVED']
    
    for i, name in enumerate(glyph_names):
        coords = embeddings[i]
        norm = np.linalg.norm(coords)
        print(f"  {name:10s}: [{coords[0]:7.4f}, {coords[1]:7.4f}, {coords[2]:7.4f}]  |v|={norm:.4f}")
    
    # Test sequence embedding
    test_tokens = [4, 2, 3, 0, 4, 2]  # "The qu"
    seq_coords = embed_sequence(test_tokens, embeddings)
    print(f"\nSequence embedding shape: {seq_coords.shape}")
    print(f"Sample coordinates:\n{seq_coords}")
