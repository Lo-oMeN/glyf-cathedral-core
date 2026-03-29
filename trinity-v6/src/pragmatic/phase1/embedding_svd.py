"""
embedding_svd.py - SVD-based geometric embedding module

Builds co-occurrence matrices from glyph token sequences and applies
Truncated SVD to generate 3D embeddings normalized to the unit sphere.
"""
import numpy as np
from sklearn.decomposition import TruncatedSVD
from typing import List, Optional
import hashlib
import os

# Glyph vocabulary size (0-6)
NUM_GLYPH_TYPES = 7

def build_cooccurrence(tokens: List[int], window: int = 5) -> np.ndarray:
    """
    Build [7, 7] co-occurrence matrix for 7 glyph types.
    
    Counts how often each glyph type appears within a context window
    of every other glyph type.
    
    Args:
        tokens: List of integer glyph type values (0-6)
        window: Context window size (default: 5)
        
    Returns:
        7x7 co-occurrence matrix
    """
    matrix = np.zeros((NUM_GLYPH_TYPES, NUM_GLYPH_TYPES), dtype=np.float64)
    
    for i, t in enumerate(tokens):
        # Look at context window around position i
        start = max(0, i - window)
        end = min(len(tokens), i + window + 1)  # +1 for inclusive range
        
        for j in range(start, end):
            if i != j:  # Don't count self-co-occurrence
                context_token = tokens[j]
                matrix[t][context_token] += 1.0
    
    return matrix


def svd_embed(tokens: List[int], 
              n_components: int = 3,
              window: int = 5,
              cache_dir: Optional[str] = None) -> np.ndarray:
    """
    Return [N, 3] coordinate array for each token using SVD embeddings.
    
    Builds a co-occurrence matrix from the token sequence, applies Truncated SVD
    to reduce to n_components dimensions, then normalizes each token's
    coordinates to the unit sphere.
    
    Args:
        tokens: List of integer glyph type values (0-6)
        n_components: Number of dimensions for embedding (default: 3)
        window: Context window size for co-occurrence (default: 5)
        cache_dir: Optional directory to cache embeddings as .npy files
        
    Returns:
        Array of shape [len(tokens), n_components] with normalized coordinates
    """
    # Check cache first if provided
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        # Create cache key from tokens and parameters
        cache_key = hashlib.md5(
            f"{str(tokens)}:{window}:{n_components}".encode()
        ).hexdigest()
        cache_path = os.path.join(cache_dir, f"svd_embed_{cache_key}.npy")
        
        if os.path.exists(cache_path):
            coords = np.load(cache_path)
            return coords
    
    # Build co-occurrence matrix
    cooccurrence = build_cooccurrence(tokens, window=window)
    
    # Handle edge case: empty co-occurrence (no context)
    if cooccurrence.sum() == 0:
        # Return zero coordinates for all tokens
        coords = np.zeros((len(tokens), n_components))
        if cache_dir:
            np.save(cache_path, coords)
        return coords
    
    # Apply Truncated SVD
    # Note: We fit on the glyph types (rows), not the tokens directly
    svd = TruncatedSVD(n_components=min(n_components, NUM_GLYPH_TYPES - 1))
    glyph_embeddings = svd.fit_transform(cooccurrence)
    
    # Map each token to its glyph type's embedding
    coords = np.array([glyph_embeddings[t] for t in tokens])
    
    # Normalize to unit sphere (each row has L2 norm = 1)
    norms = np.linalg.norm(coords, axis=1, keepdims=True)
    # Avoid division by zero
    norms[norms == 0] = 1.0
    coords = coords / norms
    
    # Cache result if directory provided
    if cache_dir:
        np.save(cache_path, coords)
    
    return coords


def batch_svd_embed(token_sequences: List[List[int]],
                    n_components: int = 3,
                    window: int = 5,
                    cache_dir: Optional[str] = None) -> List[np.ndarray]:
    """
    Process multiple token sequences with SVD embedding.
    
    Args:
        token_sequences: List of token sequences
        n_components: Number of dimensions for embedding (default: 3)
        window: Context window size (default: 5)
        cache_dir: Optional directory to cache embeddings
        
    Returns:
        List of embedding arrays, one per sequence
    """
    return [
        svd_embed(tokens, n_components=n_components, window=window, cache_dir=cache_dir)
        for tokens in token_sequences
    ]


def clear_embedding_cache(cache_dir: str) -> int:
    """
    Clear all cached embedding files.
    
    Args:
        cache_dir: Directory containing cached .npy files
        
    Returns:
        Number of files removed
    """
    if not os.path.exists(cache_dir):
        return 0
    
    count = 0
    for filename in os.listdir(cache_dir):
        if filename.startswith("svd_embed_") and filename.endswith(".npy"):
            os.remove(os.path.join(cache_dir, filename))
            count += 1
    
    return count


if __name__ == "__main__":
    # Test with the tokenizer
    from glyph_tokenizer import tokenize_to_integers
    
    text = "The quick brown fox"
    tokens = tokenize_to_integers(text)
    
    print(f"Input text: {text!r}")
    print(f"Tokens: {tokens}")
    
    # Get embeddings
    coords = svd_embed(tokens, n_components=3, window=5)
    
    print(f"\nEmbedding shape: {coords.shape}")
    print(f"Expected shape: ({len(tokens)}, 3)")
    
    # Verify unit sphere normalization
    norms = np.linalg.norm(coords, axis=1)
    print(f"\nNorms (should all be ~1.0): {norms}")
    print(f"All close to 1.0: {np.allclose(norms, 1.0)}")
    
    # Show sample coordinates
    print(f"\nFirst 5 token embeddings:")
    for i in range(min(5, len(tokens))):
        print(f"  Token {tokens[i]}: [{coords[i][0]:+.4f}, {coords[i][1]:+.4f}, {coords[i][2]:+.4f}]")
    
    # Test caching
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\nTesting cache in: {tmpdir}")
        coords_cached = svd_embed(tokens, n_components=3, window=5, cache_dir=tmpdir)
        print(f"Cached embedding matches: {np.allclose(coords, coords_cached)}")
        
        # Load from cache
        coords_loaded = svd_embed(tokens, n_components=3, window=5, cache_dir=tmpdir)
        print(f"Loaded from cache matches: {np.allclose(coords, coords_loaded)}")
    
    print("\n✓ All tests passed!")
