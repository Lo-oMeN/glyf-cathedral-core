#pragma once
#include "../core/gauge_node.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Geometric Attention Masking
 * 
 * Applies constraints based on:
 * - Glyph type (topology)
 * - Chirality (handedness)
 * - Spatial relationships
 * 
 * This creates "architecturally coherent" attention patterns
 * that respect the geometric structure of the knowledge graph.
 */

/**
 * Apply geometric attention mask to attention scores
 * 
 * @param attn_scores Attention score matrix [n_heads, seq_len, seq_len]
 * @param nodes Context nodes (gauge graph)
 * @param n_nodes Number of nodes
 * @param seq_len Sequence length (may differ from n_nodes)
 * @param n_heads Number of attention heads
 * 
 * The masking operates as follows:
 * - GLYPH_VOID (0): Zero attention (complete suppression)
 * - GLYPH_VESICA (6): Gaussian distance weighting
 * - Chirality XOR: 0.5x penalty
 * - GLYPH_DOT (1): 1.1x boost (anchor points)
 */
void geometric_attention_mask(
    float* attn_scores,
    const GaugeNode128* nodes,
    int n_nodes,
    int seq_len,
    int n_heads
);

/**
 * Compute attention weight between two nodes
 * 
 * @param a First node
 * @param b Second node
 * @return Attention weight (0.0 to 1.0+)
 * 
 * Factors:
 * - Distance (closer = higher weight)
 * - Glyph compatibility
 * - Chirality alignment
 */
float geometric_attention_weight(
    const GaugeNode128* a,
    const GaugeNode128* b
);

/**
 * Calculate Gaussian distance-based attention
 * Used primarily for GLYPH_VESICA nodes
 * 
 * @param dist Distance between nodes
 * @param sigma Standard deviation (from holonomy_phase)
 * @return Gaussian weight
 */
float vesica_gaussian_weight(float dist, float sigma);

/**
 * Compute chirality penalty
 * 
 * @param chirality_a First chirality bit
 * @param chirality_b Second chirality bit
 * @return 1.0 if same, 0.5 if different
 */
float chirality_penalty(uint8_t chirality_a, uint8_t chirality_b);

/**
 * Get glyph attention bias
 * 
 * @param glyph Glyph type
 * @return Multiplicative bias factor
 */
float glyph_attention_bias(GlyfPrimitive glyph);

/**
 * Apply full geometric mask to logits during generation
 * This is a higher-level interface for inference-time masking
 * 
 * @param logits Raw model logits [n_vocab]
 * @param n_vocab Vocabulary size
 * @param nodes Context nodes
 * @param n_nodes Number of nodes
 * @param token_to_node Mapping from token IDs to node indices (optional)
 */
void geometric_logits_mask(
    float* logits,
    int n_vocab,
    const GaugeNode128* nodes,
    int n_nodes,
    const int* token_to_node
);

#ifdef __cplusplus
}
#endif
