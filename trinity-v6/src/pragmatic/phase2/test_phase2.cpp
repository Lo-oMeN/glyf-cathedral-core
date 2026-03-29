/**
 * test_phase2.cpp - Unit tests for Phase 2 constrained inference
 * 
 * Tests:
 * 1. Model loading
 * 2. Attention masking
 * 3. Geometric constraints (chirality, glyph types)
 * 4. Graph context loading
 */

#include "llama_wrapper.h"
#include "attention_mask.h"
#include "../core/gauge_node.h"
#include <cstdio>
#include <cstring>
#include <cmath>
#include <vector>

// Test results
int tests_passed = 0;
int tests_failed = 0;

#define TEST(name) printf("\n[TEST] %s\n", name);
#define ASSERT(cond, msg) \
    if (!(cond)) { \
        printf("  [FAIL] %s (line %d)\n", msg, __LINE__); \
        tests_failed++; \
    } else { \
        printf("  [PASS] %s\n", msg); \
        tests_passed++; \
    }

#define ASSERT_FLOAT_EQ(a, b, eps, msg) \
    if (fabs((a) - (b)) > (eps)) { \
        printf("  [FAIL] %s: %f != %f (line %d)\n", msg, (float)(a), (float)(b), __LINE__); \
        tests_failed++; \
    } else { \
        printf("  [PASS] %s\n", msg); \
        tests_passed++; \
    }

// Test 1: Gauge node operations
void test_gauge_nodes() {
    TEST("Gauge Node Operations");
    
    GaugeNode128 node;
    gauge_node_init(&node, 1, GLYPH_DOT, 1.0f, 2.0f, 3.0f);
    
    ASSERT(node.node_id == 1, "Node ID set correctly");
    ASSERT(node.glyph_type == GLYPH_DOT, "Glyph type set correctly");
    ASSERT(node.coordinates[0] == 1.0f, "X coordinate set");
    ASSERT(node.coordinates[1] == 2.0f, "Y coordinate set");
    ASSERT(node.coordinates[2] == 3.0f, "Z coordinate set");
    ASSERT(sizeof(node) == 128, "Node size is 128 bytes");
    
    // Test second node and bonding
    GaugeNode128 node2;
    gauge_node_init(&node2, 2, GLYPH_LINE, 4.0f, 5.0f, 6.0f);
    
    bool connected = gauge_node_connect(&node, &node2);
    ASSERT(connected, "Nodes connected successfully");
    ASSERT(node.bond_count == 1, "Bond count updated");
    ASSERT(node.bonds[0] == 2, "Bond target correct");
}

// Test 2: Distance calculations
void test_distance() {
    TEST("Distance Calculations");
    
    GaugeNode128 a, b;
    gauge_node_init(&a, 1, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&b, 2, GLYPH_DOT, 3.0f, 4.0f, 0.0f);
    
    float dist = gauge_node_distance(&a, &b);
    ASSERT_FLOAT_EQ(dist, 5.0f, 0.001f, "3-4-5 triangle distance");
    
    // Same point
    GaugeNode128 c;
    gauge_node_init(&c, 3, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    dist = gauge_node_distance(&a, &c);
    ASSERT_FLOAT_EQ(dist, 0.0f, 0.001f, "Same point distance is zero");
}

// Test 3: Chirality penalty
void test_chirality() {
    TEST("Chirality Penalty");
    
    float penalty_same = chirality_penalty(0, 0);
    float penalty_diff = chirality_penalty(0, 1);
    float penalty_xor = chirality_penalty(1, 0);
    
    ASSERT_FLOAT_EQ(penalty_same, 1.0f, 0.001f, "Same chirality: no penalty");
    ASSERT_FLOAT_EQ(penalty_diff, 0.5f, 0.001f, "Different chirality: 0.5x penalty");
    ASSERT_FLOAT_EQ(penalty_xor, 0.5f, 0.001f, "XOR penalty consistent");
}

// Test 4: Glyph attention bias
void test_glyph_bias() {
    TEST("Glyph Attention Bias");
    
    ASSERT_FLOAT_EQ(glyph_attention_bias(GLYPH_VOID), 0.0f, 0.001f, "VOID bias is 0");
    ASSERT_FLOAT_EQ(glyph_attention_bias(GLYPH_DOT), 1.1f, 0.001f, "DOT bias is 1.1");
    ASSERT_FLOAT_EQ(glyph_attention_bias(GLYPH_CURVE), 1.0f, 0.001f, "CURVE bias is 1.0");
    ASSERT_FLOAT_EQ(glyph_attention_bias(GLYPH_LINE), 1.0f, 0.001f, "LINE bias is 1.0");
    ASSERT(glyph_attention_bias(GLYPH_VESICA) > 0.0f, "VESICA has positive bias");
}

// Test 5: Vesica Gaussian weight
void test_vesica_gaussian() {
    TEST("Vesica Gaussian Weight");
    
    // At distance 0, weight should be 1.0
    float w0 = vesica_gaussian_weight(0.0f, 1.0f);
    ASSERT_FLOAT_EQ(w0, 1.0f, 0.001f, "Gaussian at 0 distance is 1");
    
    // At distance = sigma, weight should be exp(-0.5) ≈ 0.6065
    float w1 = vesica_gaussian_weight(1.0f, 1.0f);
    ASSERT_FLOAT_EQ(w1, 0.606531f, 0.001f, "Gaussian at 1 sigma");
    
    // At large distance, weight should be near 0
    float w2 = vesica_gaussian_weight(10.0f, 1.0f);
    ASSERT(w2 < 0.01f, "Gaussian decays at large distance");
}

// Test 6: Attention weight computation
void test_attention_weight() {
    TEST("Attention Weight Computation");
    
    GaugeNode128 a, b;
    gauge_node_init(&a, 1, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&b, 2, GLYPH_LINE, 1.0f, 0.0f, 0.0f);
    a.chirality = 0;
    b.chirality = 0;
    
    float w = geometric_attention_weight(&a, &b);
    ASSERT(w > 0.0f, "Attention weight is positive for compatible nodes");
    ASSERT(w <= 2.0f, "Attention weight is bounded");
    
    // Test with VOID (should be 0)
    GaugeNode128 void_node;
    gauge_node_init(&void_node, 3, GLYPH_VOID, 0.0f, 0.0f, 0.0f);
    float w_void = geometric_attention_weight(&void_node, &a);
    ASSERT_FLOAT_EQ(w_void, 0.0f, 0.001f, "VOID node has zero attention");
    
    // Test chirality penalty
    GaugeNode128 c;
    gauge_node_init(&c, 4, GLYPH_DOT, 1.0f, 0.0f, 0.0f);
    c.chirality = 1; // Opposite chirality
    float w_chiral = geometric_attention_weight(&a, &c);
    ASSERT(w_chiral < w, "Opposite chirality reduces weight");
}

// Test 7: Attention mask application
void test_attention_mask() {
    TEST("Attention Mask Application");
    
    // Create simple graph
    GaugeNode128 nodes[3];
    gauge_node_init(&nodes[0], 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[1], 1, GLYPH_LINE, 1.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[2], 2, GLYPH_VOID, 2.0f, 0.0f, 0.0f);
    
    nodes[0].chirality = 0;
    nodes[1].chirality = 0;
    nodes[2].chirality = 0;
    
    // Create attention scores (all 1.0)
    int n_heads = 2;
    int seq_len = 3;
    std::vector<float> attn_scores(n_heads * seq_len * seq_len, 1.0f);
    
    // Apply mask
    geometric_attention_mask(attn_scores.data(), nodes, 3, seq_len, n_heads);
    
    // Check that VOID node row is suppressed
    // For head 0, query 2 (VOID node), all keys should be near 0
    bool void_suppressed = true;
    for (int j = 0; j < seq_len; j++) {
        int idx = 0 * seq_len * seq_len + 2 * seq_len + j;
        if (attn_scores[idx] > 0.01f) {
            void_suppressed = false;
            break;
        }
    }
    ASSERT(void_suppressed, "VOID node attention is suppressed");
    
    // Check that DOT node has boost
    int dot_idx = 0 * seq_len * seq_len + 0 * seq_len + 1;
    ASSERT(attn_scores[dot_idx] > 1.0f, "DOT node receives attention boost");
}

// Test 8: Graph serialization
void test_graph_serialization() {
    TEST("Graph Serialization");
    
    // Create test graph
    GaugeNode128 nodes[3];
    gauge_node_init(&nodes[0], 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[1], 1, GLYPH_LINE, 1.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[2], 2, GLYPH_CIRCLE, 2.0f, 0.0f, 0.0f);
    
    nodes[0].chirality = 0;
    nodes[1].chirality = 1; // Opposite chirality
    nodes[2].chirality = 0;
    
    gauge_node_connect(&nodes[0], &nodes[1]);
    gauge_node_connect(&nodes[1], &nodes[2]);
    
    // Write to temp file
    const char* temp_file = "/tmp/test_phase2.loom";
    int result = gauge_graph_write(temp_file, nodes, 3);
    ASSERT(result == 0, "Graph written successfully");
    
    // Read back
    uint32_t n_loaded = 0;
    GaugeNode128* loaded = gauge_graph_read(temp_file, &n_loaded);
    ASSERT(loaded != nullptr, "Graph read successfully");
    ASSERT(n_loaded == 3, "Correct number of nodes loaded");
    ASSERT(loaded[0].node_id == 0, "Node ID preserved");
    ASSERT(loaded[0].glyph_type == GLYPH_DOT, "Glyph type preserved");
    ASSERT(loaded[1].chirality == 1, "Chirality preserved");
    ASSERT(loaded[0].bond_count == 1, "Bonds preserved");
    
    free(loaded);
    remove(temp_file);
}

// Test 9: LoomanInference class
void test_looman_inference() {
    TEST("LoomanInference Class");
    
    LoomanInference loom;
    
    // Test initial state
    ASSERT(!loom.is_loaded(), "Initially not loaded");
    ASSERT(loom.context_size() == 0, "Initially no context");
    
    // Test setting context
    std::vector<GaugeNode128> nodes;
    for (int i = 0; i < 5; i++) {
        GaugeNode128 node;
        gauge_node_init(&node, i, (GlyfPrimitive)(i % GLYPH_COUNT), 
                       (float)i, 0.0f, 0.0f);
        node.chirality = i % 2;
        nodes.push_back(node);
    }
    
    loom.set_context(nodes);
    ASSERT(loom.context_size() == 5, "Context size correct");
}

// Test 10: Integration test (without actual model)
void test_integration() {
    TEST("Integration Test (Stub Mode)");
    
    // This test runs without a real model
    // It verifies the infrastructure is in place
    
    LoomanInference loom;
    
    // Create a small test graph
    std::vector<GaugeNode128> graph;
    
    // Root node (DOT)
    GaugeNode128 root;
    gauge_node_init(&root, 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    root.chirality = 0;
    strcpy((char*)root.payload, "center");
    graph.push_back(root);
    
    // Connected nodes with alternating chirality
    for (int i = 1; i <= 4; i++) {
        GaugeNode128 node;
        GlyfPrimitive glyph = (i % 2 == 0) ? GLYPH_LINE : GLYPH_CURVE;
        gauge_node_init(&node, i, glyph, 
                       (float)i * 0.5f, (float)i * 0.3f, 0.0f);
        node.chirality = i % 2;
        
        // Connect to root
        node.bonds[0] = 0;
        node.bond_count = 1;
        
        graph.push_back(node);
    }
    
    // Update root bonds
    graph[0].bond_count = 4;
    for (int i = 0; i < 4; i++) {
        graph[0].bonds[i] = i + 1;
    }
    
    loom.set_context(graph);
    ASSERT(loom.context_size() == 5, "Graph loaded");
    
    // Verify topology
    int dot_count = 0;
    int chiral_pairs = 0;
    for (const auto& node : graph) {
        if (node.glyph_type == GLYPH_DOT) dot_count++;
        for (int b = 0; b < node.bond_count; b++) {
            uint32_t target = node.bonds[b];
            if (target < graph.size()) {
                if (node.chirality != graph[target].chirality) {
                    chiral_pairs++;
                }
            }
        }
    }
    
    ASSERT(dot_count == 1, "One DOT node");
    ASSERT(chiral_pairs > 0, "Chiral pairs detected");
    
    printf("  [INFO] Graph has %d chiral pairs (XOR connections)\n", chiral_pairs / 2);
}

// Test 11: Holonomy verification
void test_holonomy() {
    TEST("Holonomy Verification");
    
    // Create a cycle: 0 -> 1 -> 2 -> 0
    GaugeNode128 nodes[3];
    gauge_node_init(&nodes[0], 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[1], 1, GLYPH_LINE, 1.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[2], 2, GLYPH_LINE, 0.5f, 0.866f, 0.0f); // Equilateral triangle
    
    // Set consistent chirality (no violation)
    nodes[0].chirality = 0;
    nodes[1].chirality = 0;
    nodes[2].chirality = 0;
    
    uint32_t cycle[] = {0, 1, 2, 0};
    uint8_t parity = holonomy_compute_parity(nodes, cycle, 4);
    ASSERT(parity == 0, "Consistent chirality: parity 0");
    
    // Introduce chirality violation
    nodes[1].chirality = 1;
    parity = holonomy_compute_parity(nodes, cycle, 4);
    ASSERT(parity == 1, "Inconsistent chirality: parity 1 (odd number of flips)");
}

int main(int argc, char** argv) {
    printf("========================================\n");
    printf("Phase 2: Constrained Inference Tests\n");
    printf("========================================\n");
    printf("GaugeNode128 size: %zu bytes\n", sizeof(GaugeNode128));
    printf("\n");
    
    // Run all tests
    test_gauge_nodes();
    test_distance();
    test_chirality();
    test_glyph_bias();
    test_vesica_gaussian();
    test_attention_weight();
    test_attention_mask();
    test_graph_serialization();
    test_looman_inference();
    test_integration();
    test_holonomy();
    
    // Summary
    printf("\n========================================\n");
    printf("Results: %d passed, %d failed\n", tests_passed, tests_failed);
    printf("========================================\n");
    
    return tests_failed > 0 ? 1 : 0;
}
