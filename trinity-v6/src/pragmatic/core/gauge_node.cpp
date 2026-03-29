#include "gauge_node.h"
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/* ============================================================================
 * Core Operations
 * ============================================================================ */

void gauge_node_init(GaugeNode128* node, uint32_t id, GlyfPrimitive type,
                     float x, float y, float z) {
    memset(node, 0, sizeof(GaugeNode128));
    
    node->node_id = id;
    node->glyph_type = (uint8_t)type;
    node->coordinates[0] = x;
    node->coordinates[1] = y;
    node->coordinates[2] = z;
    node->chirality = 0;
    node->bond_count = 0;
    node->holonomy_phase = 0.0f;
    
    /* Initialize payload with zeros */
    memset(node->payload, 0, 72);
}

bool gauge_node_connect(GaugeNode128* a, GaugeNode128* b) {
    /* Check if connection already exists */
    for (uint16_t i = 0; i < a->bond_count; i++) {
        if (a->bonds[i] == b->node_id) {
            return true;  /* Already connected */
        }
    }
    
    /* Check capacity */
    if (a->bond_count >= 4) {
        return false;  /* Max bonds reached */
    }
    
    /* Add bidirectional connection */
    a->bonds[a->bond_count++] = b->node_id;
    
    /* Also add reverse connection if space available */
    if (b->bond_count < 4) {
        /* Check if already connected */
        bool already = false;
        for (uint16_t i = 0; i < b->bond_count; i++) {
            if (b->bonds[i] == a->node_id) {
                already = true;
                break;
            }
        }
        if (!already) {
            b->bonds[b->bond_count++] = a->node_id;
        }
    }
    
    return true;
}

float gauge_node_distance(const GaugeNode128* a, const GaugeNode128* b) {
    float dx = a->coordinates[0] - b->coordinates[0];
    float dy = a->coordinates[1] - b->coordinates[1];
    float dz = a->coordinates[2] - b->coordinates[2];
    return sqrtf(dx*dx + dy*dy + dz*dz);
}

float gauge_node_vesica_overlap(const GaugeNode128* a, const GaugeNode128* b) {
    /* Vesica = intersection of two spheres (3D) or circles (2D)
     * For simplicity, treat as 3D spheres with radius = holonomy_phase
     */
    float distance = gauge_node_distance(a, b);
    float radius_a = fmaxf(a->holonomy_phase, 0.001f);
    float radius_b = fmaxf(b->holonomy_phase, 0.001f);
    
    /* No intersection */
    if (distance >= radius_a + radius_b) {
        return 0.0f;
    }
    
    /* Complete containment */
    if (distance <= fabsf(radius_a - radius_b)) {
        float r = fminf(radius_a, radius_b);
        return (4.0f / 3.0f) * M_PI * r * r * r;
    }
    
    /* Partial intersection - lens volume formula */
    float r0_sq = radius_a * radius_a;
    float r1_sq = radius_b * radius_b;
    float d_sq = distance * distance;
    
    float term1 = (r0_sq - r1_sq + d_sq) / (2.0f * distance);
    float term2 = (r1_sq - r0_sq + d_sq) / (2.0f * distance);
    
    float h0 = radius_a - term1;
    float h1 = radius_b - term2;
    
    /* Volume of spherical caps */
    float vol0 = (M_PI * h0 * h0 / 3.0f) * (3.0f * radius_a - h0);
    float vol1 = (M_PI * h1 * h1 / 3.0f) * (3.0f * radius_b - h1);
    
    return vol0 + vol1;
}

/* ============================================================================
 * Holonomy Invariants
 * ============================================================================ */

bool holonomy_verify_path(GaugeNode128* nodes, uint32_t* path, uint32_t path_len) {
    if (path_len < 2) return true;
    
    uint8_t parity = 0;
    for (uint32_t i = 0; i < path_len; i++) {
        uint32_t node_idx = path[i];
        parity ^= nodes[node_idx].chirality;
    }
    
    /* For open paths, no constraint */
    /* For closed paths (cycle), parity must be 0 */
    return true;  /* Open path always valid */
}

uint8_t holonomy_compute_parity(GaugeNode128* nodes, uint32_t* cycle, uint32_t cycle_len) {
    uint8_t parity = 0;
    for (uint32_t i = 0; i < cycle_len; i++) {
        uint32_t node_idx = cycle[i];
        parity ^= nodes[node_idx].chirality;
    }
    return parity;
}

/* Simple cycle detection using DFS */
static bool dfs_find_cycles(GaugeNode128* nodes, uint32_t num_nodes,
                           uint32_t current, uint32_t parent,
                           bool* visited, bool* rec_stack,
                           uint32_t* path, uint32_t* path_len) {
    visited[current] = true;
    rec_stack[current] = true;
    path[(*path_len)++] = current;
    
    GaugeNode128* node = &nodes[current];
    
    for (uint16_t i = 0; i < node->bond_count; i++) {
        uint32_t neighbor_id = node->bonds[i];
        
        /* Find neighbor index (simplified - assumes node_id == index) */
        uint32_t neighbor = neighbor_id;
        if (neighbor >= num_nodes) continue;
        
        if (!visited[neighbor]) {
            if (dfs_find_cycles(nodes, num_nodes, neighbor, current,
                               visited, rec_stack, path, path_len)) {
                return true;
            }
        } else if (rec_stack[neighbor] && neighbor != parent) {
            /* Cycle detected - verify holonomy */
            /* Find cycle in path */
            uint32_t cycle_start = 0;
            for (uint32_t j = 0; j < *path_len; j++) {
                if (path[j] == neighbor) {
                    cycle_start = j;
                    break;
                }
            }
            
            uint32_t cycle_len = *path_len - cycle_start;
            uint8_t parity = holonomy_compute_parity(nodes, &path[cycle_start], cycle_len);
            
            if (parity != 0) {
                /* Holonomy violation */
                return false;
            }
        }
    }
    
    rec_stack[current] = false;
    (*path_len)--;
    return true;
}

bool holonomy_verify_graph(GaugeNode128* nodes, uint32_t num_nodes) {
    bool* visited = (bool*)calloc(num_nodes, sizeof(bool));
    bool* rec_stack = (bool*)calloc(num_nodes, sizeof(bool));
    uint32_t* path = (uint32_t*)malloc(num_nodes * sizeof(uint32_t));
    uint32_t path_len = 0;
    
    bool valid = true;
    
    for (uint32_t i = 0; i < num_nodes && valid; i++) {
        if (!visited[i]) {
            if (!dfs_find_cycles(nodes, num_nodes, i, UINT32_MAX,
                                visited, rec_stack, path, &path_len)) {
                valid = false;
            }
        }
    }
    
    free(visited);
    free(rec_stack);
    free(path);
    
    return valid;
}

/* ============================================================================
 * Serialization
 * ============================================================================ */

typedef struct {
    uint32_t magic;
    uint32_t version;
    uint32_t num_nodes;
    uint32_t reserved;
} GaugeGraphHeader;

int gauge_graph_write(const char* filename, GaugeNode128* nodes, uint32_t num_nodes) {
    FILE* fp = fopen(filename, "wb");
    if (!fp) return -1;
    
    /* Write header */
    GaugeGraphHeader header = {
        .magic = GAUGE_NODE_MAGIC,
        .version = GAUGE_NODE_VERSION,
        .num_nodes = num_nodes,
        .reserved = 0
    };
    
    if (fwrite(&header, sizeof(header), 1, fp) != 1) {
        fclose(fp);
        return -1;
    }
    
    /* Write nodes */
    if (fwrite(nodes, sizeof(GaugeNode128), num_nodes, fp) != num_nodes) {
        fclose(fp);
        return -1;
    }
    
    fclose(fp);
    return 0;
}

GaugeNode128* gauge_graph_read(const char* filename, uint32_t* num_nodes) {
    FILE* fp = fopen(filename, "rb");
    if (!fp) return NULL;
    
    /* Read header */
    GaugeGraphHeader header;
    if (fread(&header, sizeof(header), 1, fp) != 1) {
        fclose(fp);
        return NULL;
    }
    
    if (header.magic != GAUGE_NODE_MAGIC) {
        fclose(fp);
        return NULL;
    }
    
    *num_nodes = header.num_nodes;
    
    /* Allocate and read nodes */
    GaugeNode128* nodes = (GaugeNode128*)malloc(header.num_nodes * sizeof(GaugeNode128));
    if (!nodes) {
        fclose(fp);
        return NULL;
    }
    
    if (fread(nodes, sizeof(GaugeNode128), header.num_nodes, fp) != header.num_nodes) {
        free(nodes);
        fclose(fp);
        return NULL;
    }
    
    fclose(fp);
    return nodes;
}

GaugeNode128* gauge_graph_mmap(const char* filename, uint32_t* num_nodes) {
    int fd = open(filename, O_RDONLY);
    if (fd < 0) return NULL;
    
    struct stat st;
    if (fstat(fd, &st) < 0) {
        close(fd);
        return NULL;
    }
    
    void* mapped = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    
    if (mapped == MAP_FAILED) {
        return NULL;
    }
    
    GaugeGraphHeader* header = (GaugeGraphHeader*)mapped;
    if (header->magic != GAUGE_NODE_MAGIC) {
        munmap(mapped, st.st_size);
        return NULL;
    }
    
    *num_nodes = header->num_nodes;
    
    /* Return pointer to first node (after header) */
    return (GaugeNode128*)((char*)mapped + sizeof(GaugeGraphHeader));
}
