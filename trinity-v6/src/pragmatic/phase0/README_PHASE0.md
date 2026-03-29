# PHASE 0: Proof of Concept - GaugeNode128 Implementation

**Pragmatic Geometric AI - Core Data Structure Verification**

## Overview

Phase 0 establishes the foundational data structure (`GaugeNode128`) and Python bindings for the Pragmatic Geometric AI system. This proof of concept validates:

- 128-byte cache-line aligned node structure
- Sevenfold primitive taxonomy
- Bidirectional graph connectivity
- Holonomy invariants and chirality verification
- Binary serialization format

## Build Instructions

### Prerequisites

```bash
# System dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip build-essential

# Python dependencies
pip install pybind11 numpy networkx
```

### Building the Module

```bash
cd trinity-v6/src/pragmatic/phase0/

# Build the pybind11 extension module
python3 setup.py build_ext --inplace

# Or with verbose output
python3 setup.py build_ext --inplace -v
```

This will compile:
- `py_gauge.cpp` - Pybind11 wrapper
- `../core/gauge_node.c` - Core C implementation

And produce `py_gauge*.so` (Linux) or `py_gauge*.pyd` (Windows).

### Clean Build

```bash
rm -rf build/ *.so *.egg-info
python3 setup.py build_ext --inplace
```

## API Reference

### GaugeNode128 Class

```python
from py_gauge import GaugeNode128, GlyfPrimitive

# Create node
node = GaugeNode128(node_id=0, glyph_type=GlyfPrimitive.DOT.value, 
                    x=1.0, y=2.0, z=3.0)

# Or initialize later
node = GaugeNode128()
node.init(id=0, glyph_type=1, x=1.0, y=2.0, z=3.0)
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `node_id` | int | Unique node identifier (uint32) |
| `glyph_type` | int | Sevenfold primitive type (0-6) |
| `chirality` | int | Handedness flag (0 or 1) |
| `bond_count` | int | Number of connected bonds (read-only) |
| `holonomy_phase` | float | Accumulated rotation phase |
| `x`, `y`, `z` | float | Spatial coordinates (read-only) |

#### Methods

```python
# Set coordinates
node.set_coordinates(x, y, z)

# Get connected node IDs
bonds = node.get_bonds()  # Returns list[int]

# Payload access (72 bytes)
node.set_payload([0x00, 0x01, ...])  # List of 0-72 bytes
payload = node.get_payload()          # Returns numpy array
```

### GlyfPrimitive Enum

| Value | Name | Description |
|-------|------|-------------|
| 0 | VOID | NULL pointer, zero tensor |
| 1 | DOT | Scalar vertex |
| 2 | CURVE | Bézier control points |
| 3 | LINE | Vector edge |
| 4 | ANGLE | Cosine similarity threshold |
| 5 | CIRCLE | L2 norm boundary |
| 6 | VESICA | Intersection volume |

### Core Functions

```python
from py_gauge import (
    gauge_node_connect,      # Connect two nodes bidirectionally
    gauge_node_distance,     # Calculate L2 distance
    gauge_node_vesica_overlap,  # Calculate intersection volume
    gauge_graph_write,       # Serialize to file
    gauge_graph_read,        # Deserialize from file
    holonomy_verify_graph,   # Verify all cycle parities
    holonomy_compute_parity  # Compute XOR parity for a cycle
)

# Connect nodes
success = gauge_node_connect(node_a, node_b)  # Returns bool

# Distance calculation
dist = gauge_node_distance(node_a, node_b)  # Returns float

# Vesica overlap (spherical intersection volume)
overlap = gauge_node_vesica_overlap(node_a, node_b)

# Serialization
result = gauge_graph_write("/tmp/graph.loom", nodes)  # Returns 0 on success
nodes = gauge_graph_read("/tmp/graph.loom")  # Returns list[GaugeNode128]

# Holonomy verification
is_valid = holonomy_verify_graph(nodes)  # Returns bool
```

### Constants

```python
from py_gauge import (
    GAUGE_NODE_SIZE,    # 128 (bytes)
    GLYPH_COUNT,        # 7
    GAUGE_NODE_MAGIC,   # 0x474C5946 ("GLYF")
    GAUGE_NODE_VERSION, # 1
    PHI,                # 1.618033988749895
    PHI_INV,            # 0.618033988749895
    PHI_SQUARED,        # 2.618033988749895
    GOLDEN_ANGLE        # 2.399963229728653 radians
)
```

## Running Tests

```bash
python3 test_phase0.py
```

This will:
1. Verify 128-byte structure alignment
2. Generate 10,000 random nodes
3. Connect nearby nodes
4. Build NetworkX graph
5. Run chirality checker (XOR parity on all cycles)
6. Run holonomy verification
7. Serialize and verify read-back integrity

## Test Results

### Typical Output

```
======================================================================
PHASE 0: GaugeNode128 Implementation Test Suite
======================================================================

[1/7] Verifying GaugeNode128 structure size...
  ✓ Size check passed: 128 bytes (128-byte aligned)
  Constants: MAGIC=0x474C5946, VERSION=1
  PHI=1.618034, GOLDEN_ANGLE=2.399963

[2/7] Generating 10000 random GaugeNode128 instances...
  ✓ Generated 10000 nodes in 0.XXXs (XXXXX nodes/sec)

[3/7] Connecting nearby nodes...
  ✓ Created XXXX connections in 0.XXXs
  Total bonds: XXXX, avg bonds/node: X.XX

[4/7] Building NetworkX graph...
  ✓ Built graph with 10000 nodes, XXXX edges
  Graph construction time: 0.XXXs
  Average degree: X.XX
  Connected components: XX

[5/7] Running chirality checker (XOR parity on cycles)...
  ✓ All cycles have valid chirality parity
  Verification time: 0.XXXs

[6/7] Running holonomy graph verification...
  Holonomy verification: PASSED
  Verification time: 0.XXXs

[7/7] Testing serialization to /tmp/test_phase0.loom...
  ✓ Serialization verified (read-back integrity confirmed)
  File size: 1.22 MB
  Serialization time: 0.XXXs

======================================================================
TEST RESULTS SUMMARY
======================================================================
  Structure size:     PASS
  Node generation:    10000 nodes @ XXXXX/s
  Graph construction: XXXX edges @ XXXX/s
  Chirality check:    X violations found
  Holonomy verify:    PASS
  Serialization:      PASS

  Total runtime:      X.XXXs

✓ ALL TESTS PASSED - Ready for Phase 1
```

### Expected Performance (Reference)

On a modern x86-64 system:

| Metric | Expected Value |
|--------|---------------|
| Node generation | 50,000-500,000 nodes/sec |
| Graph construction | 10,000-100,000 edges/sec |
| Serialization | 50-200 MB/s |
| Memory per node | 128 bytes |

## File Format

The `.loom` file format (used for serialization):

```
Offset  Size  Description
------  ----  -----------
0       4     Magic: "GLYF" (0x474C5946)
4       4     Version: 1
8       4     Number of nodes
12      4     Reserved (padding to 16 bytes)
16      N     Node array (N = num_nodes * 128 bytes)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        GaugeNode128                         │
├─────────────────────────────────────────────────────────────┤
│ node_id       │ uint32_t │  4 bytes │ Unique identifier     │
├─────────────────────────────────────────────────────────────┤
│ coordinates   │ float[3] │ 12 bytes │ (x, y, z) position    │
│ momentum      │ float[3] │ 12 bytes │ Gradient flow         │
├─────────────────────────────────────────────────────────────┤
│ glyph_type    │ uint8_t  │  1 byte  │ Sevenfold primitive   │
│ chirality     │ uint8_t  │  1 byte  │ Handedness flag       │
│ bond_count    │ uint16_t │  2 bytes │ Graph degree          │
├─────────────────────────────────────────────────────────────┤
│ bonds         │ uint32[4]│ 16 bytes │ Neighbor IDs          │
│ holonomy_phase│ float    │  4 bytes │ Accumulated rotation  │
├─────────────────────────────────────────────────────────────┤
│ payload       │ uint8[72]│ 72 bytes │ Data embedding        │
├─────────────────────────────────────────────────────────────┤
│ TOTAL         │          │128 bytes │ Cache-line aligned    │
└─────────────────────────────────────────────────────────────┘
```

## Next Steps

Upon successful completion of Phase 0:

1. **Phase 1**: Add attention gating mechanisms
2. **Phase 2**: Implement gradient flow through the graph
3. **Phase 3**: Add transformer-style attention layers
4. **Phase 4**: Optimize for GPU/TPU execution

## License

Part of the Trinity v6 Pragmatic Geometric AI system.
