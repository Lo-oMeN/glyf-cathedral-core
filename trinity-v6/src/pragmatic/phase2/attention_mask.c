#include "attention_mask.h"
#include <math.h>
#include <string.h>

/* ============================================================================
 * Geometric Attention Masking Implementation
 * ============================================================================ */

void geometric_attention_mask(
    float* attn_scores,
    const GaugeNode128* nodes,
    int n_nodes,
    int seq_len,
    int n_heads
) {
    // Iterate over all attention heads
    for (int h = 0; h < n_heads; h++) {
        // For each query position (i)
        for (int i = 0; i < seq_len; i++) {
            // Map sequence position to node (with wrap-around if seq > nodes)
            int node_i = (n_nodes > 0) ? (i % n_nodes) : 0;
            const GaugeNode128* ni = &nodes[node_i];
            
            // For each key position (j)
            for (int j = 0; j < seq_len; j++) {
                int node_j = (n_nodes > 0) ? (j % n_nodes) : 0;
                const GaugeNode128* nj = &nodes[node_j];
                
                // Compute geometric mask weight
                float mask = 1.0f;
                
                // Apply glyph-specific rules
                GlyfPrimitive glyph_i = (GlyfPrimitive)ni->glyph_type;
                GlyfPrimitive glyph_j = (GlyfPrimitive)nj->glyph_type;
                
                // GLYPH_VOID: Zero attention (complete suppression)
                if (glyph_i == GLYPH_VOID || glyph_j == GLYPH_VOID) {
                    mask = 0.0f;
                }
                // GLYPH_VESICA: Gaussian distance weighting
                else if (glyph_i == GLYPH_VESICA || glyph_j == GLYPH_VESICA) {
                    float dist = gauge_node_distance(ni, nj);
                    
                    // Use holonomy_phase as variance parameter
                    float sigma = ni->holonomy_phase;
                    if (sigma <= 0.0f || sigma > 10.0f) {
                        sigma = 1.0f; // Default fallback
                    }
                    
                    mask = vesica_gaussian_weight(dist, sigma);
                }
                // GLYPH_DOT: Slight boost for anchor points
                else if (glyph_i == GLYPH_DOT || glyph_j == GLYPH_DOT) {
                    mask = 1.1f;
                }
                
                // Apply chirality penalty
                // XOR of chirality bits = 0.5x penalty
                float chi_penalty = chirality_penalty(ni->chirality, nj->chirality);
                mask *= chi_penalty;
                
                // Apply the mask to attention score
                // Layout: [head, query, key] -> [h * seq_len * seq_len + i * seq_len + j]
                int idx = h * seq_len * seq_len + i * seq_len + j;
                attn_scores[idx] *= mask;
            }
        }
    }
}

float geometric_attention_weight(
    const GaugeNode128* a,
    const GaugeNode128* b
) {
    if (!a || !b) {
        return 0.0f;
    }
    
    float weight = 1.0f;
    
    // Get glyph types
    GlyfPrimitive glyph_a = (GlyfPrimitive)a->glyph_type;
    GlyfPrimitive glyph_b = (GlyfPrimitive)b->glyph_type;
    
    // GLYPH_VOID: No attention
    if (glyph_a == GLYPH_VOID || glyph_b == GLYPH_VOID) {
        return 0.0f;
    }
    
    // Glyph bias
    weight *= glyph_attention_bias(glyph_a);
    weight *= glyph_attention_bias(glyph_b);
    
    // Distance factor (inverse relationship)
    float dist = gauge_node_distance(a, b);
    if (dist > 0.0f) {
        // Soft inverse distance
        weight *= 1.0f / (1.0f + dist * 0.1f);
    }
    
    // Chirality alignment
    weight *= chirality_penalty(a->chirality, b->chirality);
    
    // Bond bonus: directly connected nodes get boost
    bool bonded = false;
    for (int i = 0; i < 4 && i < a->bond_count; i++) {
        // Note: This assumes node_id is the index, which may not always be true
        // In a full implementation, we'd use a hash map or search
        if (a->bonds[i] == b->node_id) {
            bonded = true;
            break;
        }
    }
    if (bonded) {
        weight *= 1.2f;
    }
    
    return weight;
}

float vesica_gaussian_weight(float dist, float sigma) {
    if (sigma <= 0.0f) {
        sigma = 1.0f;
    }
    
    // Gaussian: exp(-dist^2 / (2 * sigma^2))
    float exponent = -(dist * dist) / (2.0f * sigma * sigma);
    
    // Clamp to prevent underflow
    if (exponent < -20.0f) {
        return 0.0f;
    }
    
    return expf(exponent);
}

float chirality_penalty(uint8_t chirality_a, uint8_t chirality_b) {
    // XOR of chirality bits
    // Same chirality: 1.0 (no penalty)
    // Different chirality: 0.5 (penalty)
    return (chirality_a ^ chirality_b) ? 0.5f : 1.0f;
}

float glyph_attention_bias(GlyfPrimitive glyph) {
    switch (glyph) {
        case GLYPH_VOID:
            return 0.0f;  // Complete suppression
        case GLYPH_DOT:
            return 1.1f;  // Anchor point boost
        case GLYPH_CURVE:
            return 1.0f;  // Neutral
        case GLYPH_LINE:
            return 1.0f;  // Neutral
        case GLYPH_ANGLE:
            return 0.95f; // Slight reduction (attention gating)
        case GLYPH_CIRCLE:
            return 1.05f; // Boundary emphasis
        case GLYPH_VESICA:
            return 1.0f;  // Depends on distance (handled separately)
        default:
            return 1.0f;
    }
}

void geometric_logits_mask(
    float* logits,
    int n_vocab,
    const GaugeNode128* nodes,
    int n_nodes,
    const int* token_to_node
) {
    if (!logits || !nodes || n_nodes <= 0) {
        return;
    }
    
    // If no mapping provided, use simple modulo mapping
    if (!token_to_node) {
        // Apply general geometric bias to all tokens
        // based on overall graph statistics
        
        float total_chiral_penalty = 1.0f;
        int chiral_pairs = 0;
        int void_nodes = 0;
        
        // Compute aggregate statistics
        for (int i = 0; i < n_nodes; i++) {
            if (nodes[i].glyph_type == GLYPH_VOID) {
                void_nodes++;
            }
            
            for (int j = i + 1; j < n_nodes && j < i + 4; j++) {
                if (nodes[i].chirality ^ nodes[j].chirality) {
                    chiral_pairs++;
                }
            }
        }
        
        // Aggregate penalty factor
        if (n_nodes > 0) {
            float void_ratio = (float)void_nodes / n_nodes;
            float chiral_ratio = (float)chiral_pairs / (n_nodes * 2);
            
            // More void nodes = more suppression
            // More chiral pairs = more penalty
            float global_penalty = 1.0f - (void_ratio * 0.3f) - (chiral_ratio * 0.2f);
            if (global_penalty < 0.5f) global_penalty = 0.5f;
            
            // Apply to all logits
            for (int i = 0; i < n_vocab; i++) {
                logits[i] *= global_penalty;
            }
        }
        
        return;
    }
    
    // With token-to-node mapping, apply per-token masks
    for (int token = 0; token < n_vocab && token < n_nodes; token++) {
        int node_idx = token_to_node[token];
        if (node_idx < 0 || node_idx >= n_nodes) {
            continue;
        }
        
        const GaugeNode128* node = &nodes[node_idx];
        
        // Apply glyph bias
        float bias = glyph_attention_bias((GlyfPrimitive)node->glyph_type);
        logits[token] *= bias;
        
        // Apply chirality penalty relative to graph majority
        int same_chirality = 0;
        for (int i = 0; i < n_nodes; i++) {
            if (nodes[i].chirality == node->chirality) {
                same_chirality++;
            }
        }
        
        // If node is in minority chirality, penalize
        if (same_chirality < n_nodes / 2) {
            logits[token] *= 0.5f;
        }
    }
}
