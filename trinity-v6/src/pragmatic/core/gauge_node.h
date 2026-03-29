#pragma once

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ============================================================================
 * PRAGMATIC GEOMETRIC AI - Core Types
 * Buildable on Raspberry Pi 4 or RTX 4090 today
 * ============================================================================ */

/* The Sevenfold Primitive - 1 byte per symbol */
typedef enum {
    GLYPH_VOID   = 0,  /* NULL pointer, zero tensor, attention mask 0 */
    GLYPH_DOT    = 1,  /* Scalar vertex, 1D embedding anchor */
    GLYPH_CURVE  = 2,  /* Bézier control points (quadratic, 3 floats) */
    GLYPH_LINE   = 3,  /* Vector edge, difference of dot coordinates */
    GLYPH_ANGLE  = 4,  /* Cosine similarity threshold, attention gating */
    GLYPH_CIRCLE = 5,  /* L2 norm boundary, clustering radius */
    GLYPH_VESICA = 6   /* Intersection volume, attention overlap region */
} GlyfPrimitive;

#define GLYPH_COUNT 7

/* Gauge Node - 128 bytes exactly, cache-line aligned */
typedef struct __attribute__((packed, aligned(128))) {
    /* Identity (4 bytes) */
    uint32_t node_id;
    
    /* Spatial embedding (12 bytes) */
    float coordinates[3];
    
    /* Gradient flow (12 bytes) */
    float momentum[3];
    
    /* Sevenfold taxonomy (1 byte) */
    uint8_t glyph_type;
    
    /* Handedness flag (1 byte) */
    uint8_t chirality;
    
    /* Graph degree (2 bytes) */
    uint16_t bond_count;
    
    /* Edges to neighbors (16 bytes) */
    uint32_t bonds[4];
    
    /* Accumulated rotation (4 bytes) */
    float holonomy_phase;
    
    /* Data payload (72 bytes) */
    /* Stores text embedding snippet or arbitrary data */
    uint8_t payload[72];
    
} GaugeNode128;

/* Compile-time size check */
#if defined(__cplusplus) || (defined(__STDC_VERSION__) && __STDC_VERSION__ >= 201112L)
    #if defined(__cplusplus)
        static_assert(sizeof(GaugeNode128) == 128, "GaugeNode128 must be exactly 128 bytes");
    #else
        _Static_assert(sizeof(GaugeNode128) == 128, "GaugeNode128 must be exactly 128 bytes");
    #endif
#endif

/* ============================================================================
 * Core Operations
 * ============================================================================ */

/* Initialize a node with given glyph type and coordinates */
void gauge_node_init(GaugeNode128* node, uint32_t id, GlyfPrimitive type,
                     float x, float y, float z);

/* Connect two nodes (bidirectional bond) */
bool gauge_node_connect(GaugeNode128* a, GaugeNode128* b);

/* Calculate L2 distance between nodes */
float gauge_node_distance(const GaugeNode128* a, const GaugeNode128* b);

/* Calculate Vesica intersection volume */
float gauge_node_vesica_overlap(const GaugeNode128* a, const GaugeNode128* b);

/* ============================================================================
 * Holonomy Invariants (Graph Theory)
 * ============================================================================ */

/* Verify chiral parity along a path */
bool holonomy_verify_path(GaugeNode128* nodes, uint32_t* path, uint32_t path_len);

/* Find all cycles in graph and verify holonomy */
bool holonomy_verify_graph(GaugeNode128* nodes, uint32_t num_nodes);

/* Compute XOR of chirality bits along cycle */
uint8_t holonomy_compute_parity(GaugeNode128* nodes, uint32_t* cycle, uint32_t cycle_len);

/* ============================================================================
 * Serialization (Flat Binary Format)
 * ============================================================================ */

/* Write graph to file (mmap-friendly) */
int gauge_graph_write(const char* filename, GaugeNode128* nodes, uint32_t num_nodes);

/* Read graph from file */
GaugeNode128* gauge_graph_read(const char* filename, uint32_t* num_nodes);

/* Memory-map graph for zero-copy access */
GaugeNode128* gauge_graph_mmap(const char* filename, uint32_t* num_nodes);

/* ============================================================================
 * Constants
 * ============================================================================ */

#define GAUGE_NODE_MAGIC 0x474C5946  /* "GLYF" */
#define GAUGE_NODE_VERSION 1

/* Phi - golden ratio */
#define PHI 1.618033988749895f
#define PHI_INV 0.618033988749895f
#define PHI_SQUARED 2.618033988749895f

/* Golden angle in radians (137.507 degrees) */
#define GOLDEN_ANGLE 2.399963229728653f

#ifdef __cplusplus
}
#endif
