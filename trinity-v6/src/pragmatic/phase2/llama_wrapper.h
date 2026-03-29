#pragma once

#include <llama.h>
#include <vector>
#include <string>
#include "../../core/gauge_node.h"

// Forward declarations for llama.cpp types
struct llama_model;
struct llama_context;

/**
 * LoomanInference - Geometrically constrained LLM inference
 * 
 * Wraps llama.cpp with GaugeNode128 context for attention masking
 */
class LoomanInference {
private:
    llama_model* model_ = nullptr;
    llama_context* ctx_ = nullptr;
    std::vector<GaugeNode128> context_nodes_;
    bool model_loaded_ = false;
    
    // Default generation parameters
    int n_threads_ = 4;
    int n_batch_ = 512;
    float temperature_ = 0.8f;
    float top_p_ = 0.9f;
    int top_k_ = 40;
    
public:
    LoomanInference();
    ~LoomanInference();
    
    // Prevent copying
    LoomanInference(const LoomanInference&) = delete;
    LoomanInference& operator=(const LoomanInference&) = delete;
    
    /**
     * Load a quantized model from file
     * @param path Path to .gguf model file
     * @return true on success
     */
    bool load_model(const char* path);
    
    /**
     * Set geometric context nodes for attention masking
     * @param nodes Vector of GaugeNode128 providing geometric context
     */
    void set_context_nodes(const std::vector<GaugeNode128>& nodes);
    
    /**
     * Generate text with geometric constraints
     * @param prompt Input prompt text
     * @param max_tokens Maximum tokens to generate
     * @return Generated text
     */
    std::string generate(const char* prompt, int max_tokens = 512);
    
    /**
     * Check if model is loaded
     */
    bool is_loaded() const { return model_loaded_; }
    
    /**
     * Set generation parameters
     */
    void set_temperature(float temp) { temperature_ = temp; }
    void set_top_p(float p) { top_p_ = p; }
    void set_top_k(int k) { top_k_ = k; }
    void set_n_threads(int n) { n_threads_ = n; }
    
private:
    /**
     * Apply geometric mask to logits
     * Modifies logits based on glyph_type and chirality
     */
    void apply_geometric_mask(float* logits, int n_vocab, int pos);
    
    /**
     * Tokenize text to llama tokens
     */
    std::vector<llama_token> tokenize(const char* text, bool add_bos = true);
    
    /**
     * Detokenize llama tokens to text
     */
    std::string detokenize(const std::vector<llama_token>& tokens);
};
