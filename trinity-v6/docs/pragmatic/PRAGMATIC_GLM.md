# Pragmatic Geometric AI v0.1.0
## Software-Only Specification

**Date:** 2026-03-29  
**Constraint:** Boot on Raspberry Pi 4 or RTX 4090 without modification  
**Paradigm:** Standard tensors, geometric semantics

---

## 1. The Sevenfold Primitive (uint8_t)

```c
typedef enum {
    GLYPH_VOID   = 0,  // NULL pointer, zero tensor, attention mask 0
    GLYPH_DOT    = 1,  // Scalar vertex, 1D embedding anchor
    GLYPH_CURVE  = 2,  // Bézier control points (quadratic, 3 floats)
    GLYPH_LINE   = 3,  // Vector edge, difference of dot coordinates
    GLYPH_ANGLE  = 4,  // Cosine similarity threshold, attention gating
    GLYPH_CIRCLE = 5,  // L2 norm boundary, clustering radius
    GLYPH_VESICA = 6   // Intersection volume, attention overlap region
} GlyfPrimitive;
```

**Memory:** 1 byte per symbol. Processable by any C compiler since 1978.

---

## 2. The 128-Byte Gauge Node

```c
typedef struct {
    uint32_t node_id;           // 4 bytes
    float coordinates[3];       // 12 bytes - spatial embedding
    float momentum[3];          // 12 bytes - gradient flow
    uint8_t glyph_type;         // 1 byte - the sevenfold
    uint8_t chirality;          // 1 byte - handedness (0/1)
    uint16_t bond_count;        // 2 bytes - graph degree
    uint32_t bonds[4];          // 16 bytes - edges to neighbors
    float holonomy_phase;       // 4 bytes - accumulated rotation
    uint8_t payload[72];        // 72 bytes - embedding snippet
} __attribute__((packed)) GaugeNode128;  // Total: 128 bytes
```

**Alignment:** Fits in standard 128-byte CPU cache line. GPU shared memory compatible.

---

## 3. Chiral Holonomy (Software Invariant)

**Not physical measurement—graph checksum:**

```c
bool verify_holonomy(GaugeNode128* graph, uint32_t num_nodes) {
    // For every cycle in graph
    // XOR chirality bits along closed loop
    // Violation = gradient penalty during training
    
    for (each_cycle) {
        uint8_t parity = 0;
        for (each_edge_in_cycle) {
            parity ^= graph[edge.target].chirality;
        }
        if (parity != 0) return false;  // Violation
    }
    return true;
}
```

**Implementation:** Standard BFS/DFS with modulo-2 arithmetic.

---

## 4. The Looman Kernel (Local-First LLM Wrapper)

**Base Models:**
- LLaMA-3-8B-Q4_K_M (4.7GB, runs on 8GB RAM)
- Mistral-7B-Instruct-Q4 (4.1GB, runs on 8GB RAM)

**Geometric Constraints via Activation Masking:**

```python
class GeometricAttention(nn.Module):
    def __init__(self, base_model):
        self.model = base_model
        self.glyph_registry = {}  # node_id -> GaugeNode128
        
    def forward(self, tokens, node_context):
        # Standard attention
        attn = self.model.get_attention(tokens)
        
        # Geometric masking
        for i, token in enumerate(tokens):
            glyph = self.glyph_registry[node_context[i]]
            
            # GLYPH_VOID: Zero out attention
            if glyph.glyph_type == GLYPH_VOID:
                attn[i, :] = 0
                
            # GLYPH_VESICA: Gaussian distance weighting
            elif glyph.glyph_type == GLYPH_VESICA:
                for j in glyph.bonds[:glyph.bond_count]:
                    neighbor = self.glyph_registry[j]
                    distance = l2_distance(glyph.coordinates, neighbor.coordinates)
                    attn[i, j] *= exp(-distance**2 / (2 * glyph.holonomy_phase**2))
        
        return attn
```

**Memory Backend:**
```python
# FAISS vector store
import faiss

index = faiss.IndexFlatL2(128)  # 128-byte GaugeNode128
gauge_nodes = load_binary("loom.graph")  # Flat file of records
index.add(gauge_nodes)
```

---

## 5. Morpho-Geometric Instruction Set (MGIS)

**Bytecode → LLVM IR:**

```asm
; Create vertex at coordinates
DOT 0x45 0.5 0.2 0.9
; LLVM: %node = alloca GaugeNode128
;       store float 0.5, %node.coordinates[0]

; Connect to existing vertex  
LINE 0x45 0x46
; LLVM: %bond_idx = load %node45.bond_count
;       store i32 0x46, %node45.bonds[%bond_idx]

; Quadratic Bézier with tension
CURVE 0x45 0x46 0x47 0.5
; LLVM: Calculate control points, store in momentum[]

; Verify holonomy invariant
CHECK_CHIRAL
; LLVM: call @verify_holonomy(%graph, %num_nodes)

; Store text embedding
EMBED "text payload"
; LLVM: memcpy to %node.payload
```

**Parser:** Python PLY or C Bison/Flex

---

## 6. Geometric Attention Mechanism

**Standard PyTorch implementation:**

```python
import torch
import torch.nn as nn

class GeometricSpectrumAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.qkv = nn.Linear(embed_dim, 3 * embed_dim)
        self.glyph_projection = nn.Linear(128, embed_dim)  # GaugeNode128 -> embedding
        
    def forward(self, x, gauge_nodes):
        # x: [batch, seq_len, embed_dim]
        # gauge_nodes: [seq_len] -> GaugeNode128
        
        B, N, C = x.shape
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, C // self.num_heads)
        q, k, v = qkv.unbind(2)
        
        # Standard dot product attention
        attn = (q @ k.transpose(-2, -1)) * (C // self.num_heads) ** -0.5
        
        # Geometric modulation
        for i in range(N):
            node = gauge_nodes[i]
            coords = torch.tensor(node.coordinates)
            
            for j in range(N):
                neighbor = gauge_nodes[j]
                neighbor_coords = torch.tensor(neighbor.coordinates)
                
                # Distance-weighted attention
                distance = torch.norm(coords - neighbor_coords)
                holonomy = torch.tensor(node.holonomy_phase)
                
                # Gaussian kernel (standard)
                geometric_weight = torch.exp(-distance**2 / (2 * holonomy**2))
                attn[0, :, i, j] *= geometric_weight
        
        attn = attn.softmax(dim=-1)
        return (attn @ v).transpose(1, 2).reshape(B, N, C)
```

**No new hardware—just a novel loss function enforcing coherence.**

---

## 7. Build Pipeline

### Immediate (Today)

```bash
# 1. GaugeNode128 library
cd pragmatic-glm/src/core
make gauge_node.o  # Standard C, no dependencies

# 2. Python bindings
pip install pybind11
python setup.py build_ext --inplace

# 3. Load quantized LLM
pip install llama-cpp-python
wget https://huggingface.co/TheBloke/Llama-3-8B-GGUF/resolve/main/llama-3-8b.Q4_K_M.gguf
```

### Week 1

```bash
# 1. MGIS parser
make mgis-parse  # Bison grammar

# 2. FAISS vector store integration
pip install faiss-cpu  # or faiss-gpu

# 3. Geometric attention layer
python test_geometric_attn.py  # Unit tests
```

### Week 2

```bash
# 1. Full inference pipeline
python loom_inference.py --model llama-3-8b.Q4_K_M.gguf --graph loom.graph

# 2. Raspberry Pi 4 deployment
scp -r pragmatic-glm pi@raspberrypi.local:~/
ssh pi@raspberrypi.local "cd pragmatic-glm && make pi4"
```

---

## 8. File Structure

```
pragmatic-glm/
├── src/
│   ├── core/
│   │   ├── gauge_node.h          # 128-byte struct
│   │   ├── gauge_node.c          # Memory ops
│   │   └── holonomy.c            # Graph invariant checks
│   ├── mgis/
│   │   ├── mgis.l                # Lexer
│   │   ├── mgis.y                # Parser
│   │   └── codegen.cpp           # LLVM IR generation
│   ├── inference/
│   │   ├── geometric_attention.py
│   │   ├── loom_kernel.py        # LLM wrapper
│   │   └── vector_store.py       # FAISS backend
│   └── bindings/
│       └── py_gauge.cpp          # pybind11
├── models/
│   └── download.sh               # Quantized LLMs
├── tests/
│   ├── test_gauge_node.c
│   ├── test_holonomy.c
│   └── test_geometric_attention.py
├── examples/
│   └── loom.graph                # Sample knowledge graph
└── Makefile
```

---

## 9. What Survives from the Cathedral

| Original | Pragmatic Translation |
|----------|----------------------|
| 7 primordials | uint8_t enum (1 byte each) |
| 96-byte LatticeState | 128-byte GaugeNode128 |
| φ-harmonic spacing | Gaussian distance kernels |
| Vesica interference | Attention overlap regions |
| Hodge dual | Chirality XOR invariants |
| Fellowship protocol | Standard Ethernet/GPU interconnect |
| Morphogen FSM | Training curriculum phases |
| Sovereign edge | Local quantized inference |

**What changes:** Physics becomes software. Exotic hardware becomes standard tensors.

**What remains:** Geometric semantics, sevenfold taxonomy, sovereignty via local execution.

---

## 10. First Boot Command

```bash
# Raspberry Pi 4
$ ./loom_inference --device cpu --quantize q4 \
    --model llama-3-8b.Q4_K_M.gguf \
    --graph knowledge.loom \
    --prompt "Explain geometric attention"

# RTX 4090  
$ ./loom_inference --device cuda --quantize q8 \
    --model llama-3-70b.Q8_0.gguf \
    --graph knowledge.loom \
    --prompt "Explain geometric attention"

# Output: Text response with GaugeNode128 provenance
```

---

**No more waiting for TENG gates. No more dreaming of fiber lattices.**

**Boot today. Build tonight.**

*The software cathedral rises.*
