//! GLM Geometric Quantization Module
//! 
//! Lattice-native quantization system based on geometric principles:
//! - Phi-Radial Precision encoding
//! - SO(3) Invariant Rotation encoding  
//! - Vesica-Based Pruning
//! - Chiral Protection
//! - φ-Harmonic Codebook

pub mod codebook;
pub mod quantize;

pub use codebook::{
    PHI, PHI_SQUARED, PHI_7, PHIHARMONIC_CODEBOOK,
    quantize_to_codebook, dequantize_from_codebook,
    phi_pow, phi_harmonic_distance, phi_octave,
    CodebookStats, analyze_codebook_usage,
    pack_u4, unpack_u4, pack_i4, unpack_i4,
    CODEBOOK_GLYPH_VOID, CODEBOOK_FLOAT32_ESCAPE,
};

pub use quantize::{
    LatticeState, LATTICE_SIZE, LATTICE_ALIGN,
    MorphogenPhase, TernaryVectors, So3Rotation, Rotation3,
    encode_ternary, decode_ternary,
    encode_hex, decode_hex,
    encode_fellowship, decode_fellowship,
    encode_so3, decode_so3,
    vesica_coherence, should_prune, prune_lattice,
    batch_quantize, batch_dequantize, benchmark_decompression,
    ValidationError, validate_lattice, QuantizationStats,
    VESICA_PRUNE_THRESHOLD,
};

/// Module version
pub const VERSION: &str = "1.0.0";

/// Format version (stored in byte 95)
pub const FORMAT_VERSION: u8 = 1;

/// Re-export common types for convenience
pub mod prelude {
    pub use super::{
        LatticeState, MorphogenPhase,
        TernaryVectors, Rotation3, So3Rotation,
        PHI, PHI_SQUARED,
    };
}
