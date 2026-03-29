#include "llama_wrapper.h"
#include "../../core/gauge_node.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

void print_usage(const char* program) {
    printf("Usage: %s [options]\n\n", program);
    printf("Options:\n");
    printf("  -m, --model PATH       Path to .gguf model file (required)\n");
    printf("  -g, --graph PATH       Path to .loom graph file (optional)\n");
    printf("  -p, --prompt TEXT      Prompt for generation (required)\n");
    printf("  -n, --tokens N         Max tokens to generate (default: 512)\n");
    printf("  -t, --threads N        Number of threads (default: 4)\n");
    printf("  --temp FLOAT           Temperature (default: 0.8)\n");
    printf("  --top-p FLOAT          Top-p sampling (default: 0.9)\n");
    printf("  --top-k INT            Top-k sampling (default: 40)\n");
    printf("  -h, --help             Show this help\n");
    printf("\nExample:\n");
    printf("  %s -m llama-3-8b.Q4_K_M.gguf -p \"Build an arch\"\n", program);
}

int main(int argc, char** argv) {
    const char* model_path = nullptr;
    const char* graph_path = nullptr;
    const char* prompt = nullptr;
    int max_tokens = 512;
    int n_threads = 4;
    float temperature = 0.8f;
    float top_p = 0.9f;
    int top_k = 40;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-m") == 0 || strcmp(argv[i], "--model") == 0) {
            if (i + 1 < argc) model_path = argv[++i];
        } else if (strcmp(argv[i], "-g") == 0 || strcmp(argv[i], "--graph") == 0) {
            if (i + 1 < argc) graph_path = argv[++i];
        } else if (strcmp(argv[i], "-p") == 0 || strcmp(argv[i], "--prompt") == 0) {
            if (i + 1 < argc) prompt = argv[++i];
        } else if (strcmp(argv[i], "-n") == 0 || strcmp(argv[i], "--tokens") == 0) {
            if (i + 1 < argc) max_tokens = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-t") == 0 || strcmp(argv[i], "--threads") == 0) {
            if (i + 1 < argc) n_threads = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--temp") == 0) {
            if (i + 1 < argc) temperature = atof(argv[++i]);
        } else if (strcmp(argv[i], "--top-p") == 0) {
            if (i + 1 < argc) top_p = atof(argv[++i]);
        } else if (strcmp(argv[i], "--top-k") == 0) {
            if (i + 1 < argc) top_k = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
    }
    
    // Validate required args
    if (!model_path || !prompt) {
        fprintf(stderr, "Error: --model and --prompt are required\n\n");
        print_usage(argv[0]);
        return 1;
    }
    
    printf("╔══════════════════════════════════════════╗\n");
    printf("║         LOOMAN INFERENCE v0.1.0          ║\n");
    printf("║   Pragmatic Geometric AI - Phase 2       ║\n");
    printf("╚══════════════════════════════════════════╝\n\n");
    
    // Initialize inference
    LoomanInference loom;
    loom.set_n_threads(n_threads);
    loom.set_temperature(temperature);
    loom.set_top_p(top_p);
    loom.set_top_k(top_k);
    
    // Load model
    printf("Loading model: %s\n", model_path);
    if (!loom.load_model(model_path)) {
        fprintf(stderr, "Error: Failed to load model\n");
        return 1;
    }
    printf("✓ Model loaded\n\n");
    
    // Load graph if provided
    if (graph_path) {
        printf("Loading graph: %s\n", graph_path);
        
        uint32_t num_nodes;
        GaugeNode128* graph = gauge_graph_read(graph_path, &num_nodes);
        
        if (!graph) {
            fprintf(stderr, "Warning: Failed to load graph, continuing without context\n");
        } else {
            std::vector<GaugeNode128> nodes(graph, graph + num_nodes);
            loom.set_context_nodes(nodes);
            printf("✓ Loaded %u context nodes\n\n", num_nodes);
            free(graph);
        }
    }
    
    // Set prompt
    printf("Prompt: \"%s\"\n", prompt);
    printf("Max tokens: %d\n", max_tokens);
    printf("Temperature: %.2f\n", temperature);
    printf("Threads: %d\n\n", n_threads);
    
    // Generate
    printf("Generating...\n");
    printf("────────────────────────────────────────\n");
    
    std::string response = loom.generate(prompt, max_tokens);
    
    printf("%s\n", response.c_str());
    
    printf("────────────────────────────────────────\n");
    printf("\n✓ Generation complete\n");
    
    return 0;
}
