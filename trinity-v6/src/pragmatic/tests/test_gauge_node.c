#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>
#include "../core/gauge_node.h"

/* Simple test suite for GaugeNode128 */

void test_node_init() {
    printf("Test: node_init...\n");
    
    GaugeNode128 node;
    gauge_node_init(&node, 42, GLYPH_VESICA, 1.0f, 2.0f, 3.0f);
    
    assert(node.node_id == 42);
    assert(node.glyph_type == GLYPH_VESICA);
    assert(fabs(node.coordinates[0] - 1.0f) < 0.001f);
    assert(fabs(node.coordinates[1] - 2.0f) < 0.001f);
    assert(fabs(node.coordinates[2] - 3.0f) < 0.001f);
    assert(node.bond_count == 0);
    
    printf("  ✓ node_init passed\n");
}

void test_node_connect() {
    printf("Test: node_connect...\n");
    
    GaugeNode128 node_a, node_b;
    gauge_node_init(&node_a, 1, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&node_b, 2, GLYPH_DOT, 1.0f, 0.0f, 0.0f);
    
    bool result = gauge_node_connect(&node_a, &node_b);
    assert(result == true);
    assert(node_a.bond_count == 1);
    assert(node_a.bonds[0] == 2);
    assert(node_b.bond_count == 1);  // Bidirectional
    assert(node_b.bonds[0] == 1);
    
    printf("  ✓ node_connect passed\n");
}

void test_node_distance() {
    printf("Test: node_distance...\n");
    
    GaugeNode128 node_a, node_b;
    gauge_node_init(&node_a, 1, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&node_b, 2, GLYPH_DOT, 3.0f, 4.0f, 0.0f);
    
    float dist = gauge_node_distance(&node_a, &node_b);
    assert(fabs(dist - 5.0f) < 0.001f);  // 3-4-5 triangle
    
    printf("  ✓ node_distance passed (distance=%.2f)\n", dist);
}

void test_serialization() {
    printf("Test: serialization...\n");
    
    GaugeNode128 nodes[3];
    gauge_node_init(&nodes[0], 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[1], 1, GLYPH_DOT, 1.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[2], 2, GLYPH_DOT, 0.5f, 0.866f, 0.0f);
    
    gauge_node_connect(&nodes[0], &nodes[1]);
    gauge_node_connect(&nodes[1], &nodes[2]);
    gauge_node_connect(&nodes[2], &nodes[0]);
    
    // Write to file
    const char* filename = "/tmp/test_graph.loom";
    int result = gauge_graph_write(filename, nodes, 3);
    assert(result == 0);
    
    // Read back
    uint32_t num_read;
    GaugeNode128* read_nodes = gauge_graph_read(filename, &num_read);
    assert(read_nodes != NULL);
    assert(num_read == 3);
    assert(read_nodes[0].node_id == 0);
    assert(read_nodes[1].bond_count == 2);
    
    free(read_nodes);
    printf("  ✓ serialization passed\n");
}

void test_holonomy() {
    printf("Test: holonomy verification...\n");
    
    // Create triangle with consistent chirality
    GaugeNode128 nodes[3];
    gauge_node_init(&nodes[0], 0, GLYPH_DOT, 0.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[1], 1, GLYPH_DOT, 1.0f, 0.0f, 0.0f);
    gauge_node_init(&nodes[2], 2, GLYPH_DOT, 0.5f, 0.866f, 0.0f);
    
    // Set consistent chirality (all 0 = even parity)
    nodes[0].chirality = 0;
    nodes[1].chirality = 0;
    nodes[2].chirality = 0;
    
    gauge_node_connect(&nodes[0], &nodes[1]);
    gauge_node_connect(&nodes[1], &nodes[2]);
    gauge_node_connect(&nodes[2], &nodes[0]);
    
    // Verify holonomy (should pass with all zeros)
    bool valid = holonomy_verify_graph(nodes, 3);
    assert(valid == true);
    
    printf("  ✓ holonomy verification passed\n");
}

void test_size_constraints() {
    printf("Test: size constraints...\n");
    
    printf("  sizeof(GaugeNode128) = %zu bytes\n", sizeof(GaugeNode128));
    assert(sizeof(GaugeNode128) == 128);
    assert(sizeof(GlyfPrimitive) == 4);  // enum is int
    
    printf("  ✓ size constraints passed\n");
}

int main() {
    printf("=== Pragmatic Geometric AI Test Suite ===\n\n");
    
    test_size_constraints();
    test_node_init();
    test_node_connect();
    test_node_distance();
    test_holonomy();
    test_serialization();
    
    printf("\n=== All tests passed ===\n");
    return 0;
}
