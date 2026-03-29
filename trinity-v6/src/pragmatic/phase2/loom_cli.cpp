/**
 * loom_cli.cpp - Looman Inference CLI
 * 
 * Command-line interface for geometrically-constrained inference
 * using llama.cpp as the backend.
 * 
 * Usage: ./looman --model <model.gguf> --graph <knowledge.loom> --prompt "..."
 */

#include "llama_wrapper.h"
#include "../core/gauge_node.h"
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <vector>

// Version info
#define LOOMAN_VERSION "0.2.0"
#define LOOMAN_BUILD "phase2"

void print_usage(const char* program) {
    printf("Looman Inference v%s (%s)\n", LOOMAN_VERSION, LOOMAN_BUILD);
    printf("Geometrically-constrained LLM inference\n\n");
    printf("Usage: %s [options]\n\n", program);
    printf("Required:\n");
    printf("  -m, --model <path>     Path to GGUF model file\n");
    printf("  -g, --graph <path>     Path to .loom graph file\n");
    printf("  -p, --prompt <text>   Input prompt for generation\n\n");
    printf("Optional:\n");
    printf("  -n, --tokens <n>      Max tokens to generate (default: 512)\n");
    printf("  -c, --ctx <n>         Context size (default: 4096)\n");
    printf("  -t, --threads <n>     Number of threads (default: 4)\n");
    printf("  -v, --verbose          Enable verbose output\n");
    printf("  -h, --help             Show this help\n");
    printf("  --version              Show version\n\n");
    printf("Examples:\n");
    printf("  %s -m model.gguf -g graph.loom -p \"Hello world\"\n", program);
    printf("  %s --model tiny.gguf --graph test.loom --prompt \"Build an arch\" -n 256\n", program);
}

void print_version() {
    printf("Looman Inference v%s (%s)\n", LOOMAN_VERSION, LOOMAN_BUILD);
    printf("llama.cpp backend with geometric attention masking\n");
    printf("GaugeNode128: %zu bytes\n", sizeof(GaugeNode128));
    printf("Supported glyphs: VOID DOT CURVE LINE ANGLE CIRCLE VESICA\n");
}

int main(int argc, char** argv) {
    const char* model_path = nullptr;
    const char* graph_path = nullptr;
    const char* prompt = nullptr;
    int max_tokens = 512;
    int n_ctx = 4096;
    int n_threads = 4;
    bool verbose = false;
    
    // Parse arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
        else if (strcmp(argv[i], "--version") == 0) {
            print_version();
            return 0;
        }
        else if ((strcmp(argv[i], "-m") == 0 || strcmp(argv[i], "--model") == 0) && i + 1 < argc) {
            model_path = argv[++i];
        }
        else if ((strcmp(argv[i], "-g") == 0 || strcmp(argv[i], "--graph") == 0) && i + 1 < argc) {
            graph_path = argv[++i];
        }
        else if ((strcmp(argv[i], "-p") == 0 || strcmp(argv[i], "--prompt") == 0) && i + 1 < argc) {
            prompt = argv[++i];
        }
        else if ((strcmp(argv[i], "-n") == 0 || strcmp(argv[i], "--tokens") == 0) && i + 1 < argc) {
            max_tokens = atoi(argv[++i]);
        }
        else if ((strcmp(argv[i], "-c") == 0 || strcmp(argv[i], "--ctx") == 0) && i + 1 < argc) {
            n_ctx = atoi(argv[++i]);
        }
        else if ((strcmp(argv[i], "-t") == 0 || strcmp(argv[i], "--threads") == 0) && i + 1 < argc) {
            n_threads = atoi(argv[++i]);
        }
        else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose = true;
        }
        else {
            fprintf(stderr, "Unknown option: %s\n", argv[i]);
            print_usage(argv[0]);
            return 1;
        }
    }
    
    // Validate required arguments
    if (!model_path) {
        fprintf(stderr, "Error: --model is required\n");
        print_usage(argv[0]);
        return 1;
    }
    
    if (!prompt) {
        fprintf(stderr, "Error: --prompt is required\n");
        print_usage(argv[0]);
        return 1;
    }
    
    if (verbose) {
        printf("Configuration:\n");
        printf("  Model: %s\n", model_path);
        printf("  Graph: %s\n", graph_path ? graph_path : "(none)");
        printf("  Prompt: %.50s%s\n", prompt, strlen(prompt) > 50 ? "..." : "");
        printf("  Max tokens: %d\n", max_tokens);
        printf("  Context: %d\n", n_ctx);
        printf("  Threads: %d\n", n_threads);
        printf("\n");
    }
    
    // Initialize inference engine
    LoomanInference loom;
    
    // Load model
    printf("Loading model: %s\n", model_path);
    if (!loom.load_model(model_path)) {
        fprintf(stderr, "Error: Failed to load model\n");
        fprintf(stderr, "Make sure the model file exists and is a valid GGUF format\n");
        return 1;
    }
    printf("Model loaded successfully\n\n");
    
    // Load graph if provided
    if (graph_path) {
        printf("Loading graph: %s\n", graph_path);
        
        uint32_t n_nodes = 0;
        GaugeNode128* graph = gauge_graph_read(graph_path, &n_nodes);
        
        if (!graph) {
            fprintf(stderr, "Error: Failed to load graph from %s\n", graph_path);
            fprintf(stderr, "Continuing without geometric context...\n");
        } else {
            printf("Loaded %u nodes\n", n_nodes);
            
            // Copy to vector and set context
            std::vector<GaugeNode128> nodes(graph, graph + n_nodes);
            loom.set_context(nodes);
            
            // Free the raw graph (now copied)
            free(graph);
        }
        printf("\n");
    }
    
    // Generate response
    printf("Generating response (max %d tokens)...\n", max_tokens);
    printf("---\n");
    
    // Simple timing
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    std::string response = loom.generate(prompt, max_tokens);
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    
    printf("%s\n", response.c_str());
    printf("---\n");
    
    // Print statistics
    int n_tokens = 0;
    for (char c : response) {
        if (c == ' ' || c == '\n') n_tokens++;
    }
    n_tokens++; // Approximate
    
    printf("\nStatistics:\n");
    printf("  Time: %.2f seconds\n", elapsed);
    printf("  Approx tokens: %d\n", n_tokens);
    if (elapsed > 0) {
        printf("  Speed: %.2f tokens/sec\n", n_tokens / elapsed);
    }
    
    return 0;
}
