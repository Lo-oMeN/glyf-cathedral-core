# PHASE 2: Constrained Inference Plan
## llama.cpp Integration + Chirality Attention Masking

**Objective:** Wrap llama.cpp with geometric constraints

---

## Components

### 1. llama_wrapper.cpp
C++ wrapper around llama.cpp:
```cpp
class LoomanInference {
    llama_model* model;
    llama_context* ctx;
    std::vector<GaugeNode128*> context_nodes;
    
public:
    // Load quantized model
    bool load_model(const char* path);
    
    // Set geometric context (called before generation)
    void set_context_nodes(GaugeNode128* nodes, int n_nodes);
    
    // Generate with chirality masking
    std::string generate(const char* prompt, int max_tokens);
    
private:
    // Modify logits based on geometric constraints
    void apply_geometric_mask(float* logits, int n_vocab);
};
```

### 2. attention_mask.c
Custom attention masking:
```c
// Called during llama.cpp forward pass
void geometric_attention_mask(
    float* attn_scores,      // [n_heads, seq_len, seq_len]
    GaugeNode128* nodes,     // Context nodes
    int n_nodes,
    int n_heads
) {
    for (int h = 0; h < n_heads; h++) {
        for (int i = 0; i < n_nodes; i++) {
            for (int j = 0; j < n_nodes; j++) {
                float mask = 1.0f;
                
                // GLYPH_VOID: No attention
                if (nodes[i].glyph_type == 0) {
                    mask = 0.0f;
                }
                // GLYPH_VESICA: Distance-weighted
                else if (nodes[i].glyph_type == 6) {
                    float dist = distance(nodes[i], nodes[j]);
                    mask = exp(-dist*dist / (2 * nodes[i].holonomy_phase));
                }
                // Chirality violation: Penalize
                if (nodes[i].chirality ^ nodes[j].chirality) {
                    mask *= 0.5f;
                }
                
                attn_scores[h * n_nodes * n_nodes + i * n_nodes + j] *= mask;
            }
        }
    }
}
```

### 3. loom_cli.cpp
Command-line interface:
```cpp
int main(int argc, char** argv) {
    LoomanInference loom;
    
    // Load model
    loom.load_model("llama-3-8b.Q4_K_M.gguf");
    
    // Load geometric context
    GaugeNode128* graph = load_graph("knowledge.loom");
    loom.set_context_nodes(graph, n_nodes);
    
    // Generate
    std::string response = loom.generate(
        "Build an arch",
        512  // max_tokens
    );
    
    printf("%s\n", response.c_str());
}
```

### 4. CMakeLists.txt
Build configuration:
```cmake
project(looman)
find_package(llama.cpp REQUIRED)
add_executable(looman 
    loom_cli.cpp
    llama_wrapper.cpp
    attention_mask.c
    ../core/gauge_node.c
)
target_link_libraries(looman llama pthread)
```

---

## Build Steps

```bash
# 1. Build llama.cpp
wget https://github.com/ggerganov/llama.cpp/archive/refs/tags/b3250.zip
unzip b3250.zip
cd llama.cpp-b3250
mkdir build && cd build
cmake .. -DLLAMA_BUILD_EXAMPLES=OFF
make -j4
sudo make install

# 2. Build looman
cd trinity-v6/src/pragmatic/phase2
mkdir build && cd build
cmake ..
make -j4

# 3. Run
./looman --model llama-3-8b.Q4_K_M.gguf \
         --graph knowledge.loom \
         --prompt "Build an arch"
```

---

## Deliverables

| File | Purpose | Size |
|------|---------|------|
| llama_wrapper.cpp | C++ inference wrapper | ~300 lines |
| attention_mask.c | Geometric attention | ~150 lines |
| loom_cli.cpp | Command-line tool | ~200 lines |
| CMakeLists.txt | Build config | ~50 lines |
| test_phase2.cpp | Unit tests | ~200 lines |

---

## Success Criteria

- [ ] Loads llama.cpp quantized model
- [ ] Reads GaugeNode128 graph from .loom file
- [ ] Applies geometric attention masking
- [ ] Respects chirality bits in generation
- [ ] Outputs architecturally-coherent text
- [ ] Runs on CPU (8GB RAM minimum)
- [ ] <500ms token generation time

---

**Dependencies:** llama.cpp, CMake, C++17
**Hardware:** Any x86_64 with 8GB+ RAM
**Output:** Single `looman` binary
