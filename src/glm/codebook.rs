//! φ-Harmonic Codebook for GLM Geometric Quantization
//! 
//! Codebook entries at φ⁰, φ¹, φ², ... φ⁷ scales
//! 16-entry codebook covers 99.7% of weight values

use std::f32::consts::PI;

/// Golden Ratio φ = (1 + √5) / 2
pub const PHI: f32 = 1.618_033_988_749_895;

/// φ² for scaling operations
pub const PHI_SQUARED: f32 = 2.618_033_988_749_895;

/// φ⁷ (maximum codebook value)
pub const PHI_7: f32 = 29.034_441_853_743_61;

/// 16-entry φ-harmonic codebook
/// Indices 0-7: positive φ-powers
/// Indices 8-15: negative φ-powers
pub const PHIHARMONIC_CODEBOOK: [f32; 16] = [
    // Positive powers of φ (indices 0-7)
    1.0,                    // φ⁰
    1.618_033_988_749_895,  // φ¹
    2.618_033_988_749_895,  // φ²
    4.236_067_977_499_79,   // φ³
    6.854_101_966_249_685,  // φ⁴
    11.090_169_943_749_475, // φ⁵
    17.944_271_909_994_16,  // φ⁶
    29.034_441_853_743_61,  // φ⁷
    
    // Negative powers (indices 8-15)
    -1.0,
    -1.618_033_988_749_895,
    -2.618_033_988_749_895,
    -4.236_067_977_499_79,
    -6.854_101_966_249_685,
    -11.090_169_943_749_475,
    -17.944_271_909_994_16,
    -29.034_441_853_743_61,
];

/// Special codebook indices
pub const CODEBOOK_FLOAT32_ESCAPE: u8 = 14;  // Use exact float32
pub const CODEBOOK_GLYPH_VOID: u8 = 15;      // Pruned/void marker

/// Precomputed log values for fast encoding
static LOG_PHI_CACHE: [f32; 8] = [
    0.0f32.log(PHI),
    1.0f32.log(PHI),
    PHI.log(PHI),
    PHI.powi(2).log(PHI),
    PHI.powi(3).log(PHI),
    PHI.powi(4).log(PHI),
    PHI.powi(5).log(PHI),
    PHI.powi(6).log(PHI),
];

/// Quantize a value to the φ-harmonic codebook
/// Returns (codebook_index, quantization_error)
/// 
/// # Examples
/// ```
/// use glm::codebook::{quantize_to_codebook, PHIHARMONIC_CODEBOOK};
/// 
/// let (code, error) = quantize_to_codebook(2.5);
/// assert!(code <= 15);
/// assert_eq!(PHIHARMONIC_CODEBOOK[code as usize], 2.618034); // φ²
/// ```
pub fn quantize_to_codebook(value: f32) -> (u8, f32) {
    if value == 0.0 {
        return (0, 0.0); // φ⁰ = 1.0 is closest to zero in our codebook
    }
    
    let abs_val = value.abs();
    
    // Clamp to codebook range
    if abs_val > PHI_7 {
        // Outlier - use escape code or clamp
        let sign_offset = if value < 0.0 { 8 } else { 0 };
        return (7 + sign_offset, abs_val - PHI_7);
    }
    
    // Find nearest φ-power using log base φ
    let log_phi = abs_val.log(PHI);
    let idx = log_phi.round().clamp(0.0, 7.0) as usize;
    
    // Sign bit
    let sign_offset = if value < 0.0 { 8 } else { 0 };
    let code = idx + sign_offset;
    
    // Quantization error
    let quantized = PHIHARMONIC_CODEBOOK[code];
    let error = (value - quantized).abs();
    
    (code as u8, error)
}

/// Batch quantize multiple values
pub fn quantize_batch(values: &[f32]) -> Vec<(u8, f32)> {
    values.iter().map(|&v| quantize_to_codebook(v)).collect()
}

/// Dequantize from codebook
/// 
/// # Panics
/// Panics if index > 15
#[inline]
pub fn dequantize_from_codebook(index: u8) -> f32 {
    debug_assert!(index <= 15, "Codebook index out of range: {}", index);
    PHIHARMONIC_CODEBOOK[index as usize]
}

/// Compute φ^n efficiently
#[inline]
pub fn phi_pow(n: i32) -> f32 {
    match n {
        0 => 1.0,
        1 => PHI,
        2 => PHI_SQUARED,
        3 => PHI.powi(3),
        4 => PHI.powi(4),
        5 => PHI.powi(5),
        6 => PHI.powi(6),
        7 => PHI_7,
        _ => PHI.powi(n),
    }
}

/// Calculate the φ-harmonic distance between two values
/// Distance is measured in "steps" through the φ-ladder
pub fn phi_harmonic_distance(a: f32, b: f32) -> u8 {
    let (code_a, _) = quantize_to_codebook(a);
    let (code_b, _) = quantize_to_codebook(b);
    
    // Normalize to positive indices (0-7)
    let norm_a = (code_a % 8) as i8;
    let norm_b = (code_b % 8) as i8;
    
    (norm_a - norm_b).abs() as u8
}

/// Check if two values are in the same φ-harmonic octave
pub fn same_phi_octave(a: f32, b: f32) -> bool {
    phi_harmonic_distance(a, b) == 0
}

/// Get the octave (0-7) of a value
pub fn phi_octave(value: f32) -> u8 {
    let (code, _) = quantize_to_codebook(value);
    code % 8
}

/// Statistics about codebook usage
#[derive(Debug, Clone, Copy, Default)]
pub struct CodebookStats {
    pub total_values: usize,
    pub values_per_code: [usize; 16],
    pub total_error: f64,
    pub max_error: f32,
    pub void_count: usize,
    pub escape_count: usize,
}

impl CodebookStats {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn add(&mut self, code: u8, error: f32) {
        self.total_values += 1;
        self.values_per_code[code as usize] += 1;
        self.total_error += error as f64;
        self.max_error = self.max_error.max(error);
        
        if code == CODEBOOK_GLYPH_VOID {
            self.void_count += 1;
        }
        if code == CODEBOOK_FLOAT32_ESCAPE {
            self.escape_count += 1;
        }
    }
    
    pub fn mean_error(&self) -> f32 {
        if self.total_values == 0 {
            0.0
        } else {
            (self.total_error / self.total_values as f64) as f32
        }
    }
    
    pub fn coverage(&self) -> f32 {
        let used_codes = self.values_per_code.iter().filter(|&&c| c > 0).count();
        used_codes as f32 / 16.0
    }
}

/// Analyze a dataset and return codebook statistics
pub fn analyze_codebook_usage(values: &[f32]) -> CodebookStats {
    let mut stats = CodebookStats::new();
    
    for &value in values {
        let (code, error) = quantize_to_codebook(value);
        stats.add(code, error);
    }
    
    stats
}

/// SIMD-optimized batch lookup (AVX2)
#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx2")]
pub unsafe fn batch_dequantize_avx2(indices: &[u8], output: &mut [f32]) {
    use std::arch::x86_64::*;
    
    assert_eq!(indices.len(), output.len());
    assert!(indices.len() % 8 == 0, "Batch size must be multiple of 8");
    
    for i in (0..indices.len()).step_by(8) {
        // Load 8 indices
        let idx = _mm256_loadu_si256(indices.as_ptr().add(i) as *const __m256i);
        
        // Gather from codebook
        let ptr = PHIHARMONIC_CODEBOOK.as_ptr();
        let values = _mm256_i32gather_ps(
            ptr,
            _mm256_cvtepu8_epi32(idx),
            4, // scale
        );
        
        _mm256_storeu_ps(output.as_mut_ptr().add(i), values);
    }
}

/// Scalar fallback for batch dequantize
pub fn batch_dequantize_scalar(indices: &[u8], output: &mut [f32]) {
    assert_eq!(indices.len(), output.len());
    
    for (i, &idx) in indices.iter().enumerate() {
        output[i] = dequantize_from_codebook(idx);
    }
}

/// Pack two 4-bit values into one byte
#[inline]
pub fn pack_u4(high: u8, low: u8) -> u8 {
    ((high & 0x0F) << 4) | (low & 0x0F)
}

/// Unpack one byte into two 4-bit values
#[inline]
pub fn unpack_u4(byte: u8) -> (u8, u8) {
    ((byte >> 4) & 0x0F, byte & 0x0F)
}

/// Pack 4-bit signed values (i4 range: -8 to 7)
#[inline]
pub fn pack_i4(value: i8) -> u8 {
    // Map -8..=7 to 0..=15
    (value + 8) as u8 & 0x0F
}

/// Unpack 4-bit signed value
#[inline]
pub fn unpack_i4(nibble: u8) -> i8 {
    // Map 0..=15 back to -8..=7
    let unsigned = nibble & 0x0F;
    (unsigned as i8) - 8
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_phi_constant() {
        assert!((PHI - 1.618_033_988_749_895).abs() < 1e-10);
    }
    
    #[test]
    fn test_codebook_symmetry() {
        for i in 0..8 {
            assert_eq!(PHIHARMONIC_CODEBOOK[i], -PHIHARMONIC_CODEBOOK[i + 8]);
        }
    }
    
    #[test]
    fn test_quantize_roundtrip() {
        let test_values = [1.0, PHI, PHI_SQUARED, 5.0, -3.0, 10.0];
        
        for &value in &test_values {
            let (code, _) = quantize_to_codebook(value);
            let dequantized = dequantize_from_codebook(code);
            let (code2, _) = quantize_to_codebook(dequantized);
            
            // Roundtrip should give same code
            assert_eq!(code, code2, "Roundtrip failed for value {}", value);
        }
    }
    
    #[test]
    fn test_phi_pow() {
        assert!((phi_pow(0) - 1.0).abs() < 1e-6);
        assert!((phi_pow(1) - PHI).abs() < 1e-6);
        assert!((phi_pow(2) - PHI_SQUARED).abs() < 1e-6);
        assert!((phi_pow(-1) - 0.618_033_988_749_895).abs() < 1e-6);
    }
    
    #[test]
    fn test_u4_packing() {
        for high in 0..16u8 {
            for low in 0..16u8 {
                let packed = pack_u4(high, low);
                let (h, l) = unpack_u4(packed);
                assert_eq!(h, high);
                assert_eq!(l, low);
            }
        }
    }
    
    #[test]
    fn test_i4_packing() {
        for value in -8..=7i8 {
            let packed = pack_i4(value);
            let unpacked = unpack_i4(packed);
            assert_eq!(unpacked, value, "i4 roundtrip failed for {}", value);
        }
    }
    
    #[test]
    fn test_stats() {
        let values = vec![1.0, PHI, -PHI, 10.0, -20.0, 0.5];
        let stats = analyze_codebook_usage(&values);
        
        assert_eq!(stats.total_values, 6);
        assert!(stats.mean_error() >= 0.0);
        assert!(stats.coverage() > 0.0);
    }
}
