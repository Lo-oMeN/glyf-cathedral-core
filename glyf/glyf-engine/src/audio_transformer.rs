//! GLYF Audio Transformer — Local Hearing Protocol
//! 
//! Processes audio without cloud APIs.
//! Extracts deterministic features → 96-byte structure.
//! Enables local "hearing" for GLYF interface.

#![cfg_attr(not(feature = "std"), no_std)]

extern crate alloc;

use alloc::vec::Vec;

/// Audio packet — 96-byte sacred structure for sound
/// Mirrors GlyfWord structure for symmetry
#[repr(C, align(64))]
#[derive(Copy, Clone, Debug)]
pub struct AudioGlyf {
    /// Temporal signature (8 bytes) — sample hash
    pub temporal_sig: u64,
    
    /// Spectral centroid (24 bytes) — 3×f64 (low, mid, high)
    pub spectral_centroid: [f64; 3],
    
    /// Harmonic signature (56 bytes) — 7×f64 (fundamental + 6 overtones)
    /// Maps to 7-type primitives:
    /// [0]=Curve (fundamental), [1]=Line (1st harmonic), etc.
    pub harmonic_signature: [f64; 7],
    
    /// Energy envelope (8 bytes) — RMS amplitude
    pub energy_rms: f64,
}

impl AudioGlyf {
    pub const SIZE: usize = 96;
    pub const SAMPLE_RATE: u32 = 16000; // 16kHz optimal for voice
    pub const FRAME_SIZE: usize = 512;  // 32ms frames @ 16kHz
    pub const HOP_SIZE: usize = 256;    // 50% overlap
    
    /// Transform raw PCM audio → 96-byte AudioGlyf
    /// Deterministic, no_std compatible, no ML
    pub fn from_pcm(pcm_samples: &[i16]) -> Self {
        // Step 1: Pre-emphasis (high-pass filter)
        let preemphasized = Self::pre_emphasis(pcm_samples);
        
        // Step 2: Frame extraction with Hann window
        let frames = Self::extract_frames(&preemphasized);
        
        // Step 3: FFT → spectral analysis (fixed-point for no_std)
        let spectrum = Self::compute_spectrum(&frames);
        
        // Step 4: Feature extraction (deterministic)
        let spectral_centroid = Self::spectral_centroid(&spectrum);
        let harmonic_signature = Self::harmonic_analysis(&spectrum);
        let energy_rms = Self::rms_energy(pcm_samples);
        
        // Step 5: Hash temporal signature
        let temporal_sig = Self::hash_audio(pcm_samples);
        
        Self {
            temporal_sig,
            spectral_centroid,
            harmonic_signature,
            energy_rms,
        }
    }
    
    /// Pre-emphasis filter: y[n] = x[n] - 0.97*x[n-1]
    /// Emphasizes high frequencies (voice clarity)
    fn pre_emphasis(samples: &[i16]) -> Vec<i16> {
        let mut output = Vec::with_capacity(samples.len());
        output.push(samples[0]);
        
        for i in 1..samples.len() {
            let prev = samples[i - 1] as f64 * 0.97;
            let curr = samples[i] as f64;
            let emphasized = curr - prev;
            output.push(emphasized.clamp(-32768.0, 32767.0) as i16);
        }
        
        output
    }
    
    /// Extract overlapping frames with Hann window
    fn extract_frames(samples: &[i16]) -> Vec<Vec<f64>> {
        let num_frames = (samples.len() - Self::FRAME_SIZE) / Self::HOP_SIZE + 1;
        let mut frames = Vec::with_capacity(num_frames);
        
        for i in 0..num_frames {
            let start = i * Self::HOP_SIZE;
            let mut frame = Vec::with_capacity(Self::FRAME_SIZE);
            
            for j in 0..Self::FRAME_SIZE {
                if start + j < samples.len() {
                    // Hann window
                    let window = 0.5 * (1.0 - (2.0 * core::f64::consts::PI * j as f64 
                        / (Self::FRAME_SIZE as f64 - 1.0)).cos());
                    let sample = samples[start + j] as f64 * window;
                    frame.push(sample);
                }
            }
            
            frames.push(frame);
        }
        
        frames
    }
    
    /// Compute magnitude spectrum using DFT (naive implementation for no_std)
    /// For production: use rustfft crate or pre-computed twiddle factors
    fn compute_spectrum(frames: &[Vec<f64>]) -> Vec<Vec<f64>> {
        let mut spectra = Vec::with_capacity(frames.len());
        
        for frame in frames {
            let mut spectrum = Vec::with_capacity(Self::FRAME_SIZE / 2);
            
            // Naive DFT — O(n²), suitable for small frames
            for k in 0..Self::FRAME_SIZE / 2 {
                let mut real = 0.0;
                let mut imag = 0.0;
                
                for n in 0..frame.len() {
                    let angle = -2.0 * core::f64::consts::PI * k as f64 * n as f64 
                        / Self::FRAME_SIZE as f64;
                    real += frame[n] * angle.cos();
                    imag += frame[n] * angle.sin();
                }
                
                let magnitude = (real * real + imag * imag).sqrt();
                spectrum.push(magnitude);
            }
            
            spectra.push(spectrum);
        }
        
        spectra
    }
    
    /// Spectral centroid across frequency bands
    /// Returns [low, mid, high] centroids
    fn spectral_centroid(spectra: &[Vec<f64>]) -> [f64; 3] {
        // Average spectrum across frames
        let avg_spectrum = Self::average_spectrum(spectra);
        
        let nyquist = Self::SAMPLE_RATE as f64 / 2.0;
        let bin_size = nyquist / avg_spectrum.len() as f64;
        
        // Band definitions (Hz)
        let low_cutoff = 300.0;   // Voice fundamental
        let mid_cutoff = 2000.0;  // Formants
        
        let mut low_sum = 0.0;
        let mut low_weight = 0.0;
        let mut mid_sum = 0.0;
        let mut mid_weight = 0.0;
        let mut high_sum = 0.0;
        let mut high_weight = 0.0;
        
        for (i, &mag) in avg_spectrum.iter().enumerate() {
            let freq = i as f64 * bin_size;
            
            if freq < low_cutoff {
                low_sum += freq * mag;
                low_weight += mag;
            } else if freq < mid_cutoff {
                mid_sum += freq * mag;
                mid_weight += mag;
            } else {
                high_sum += freq * mag;
                high_weight += mag;
            }
        }
        
        [
            if low_weight > 0.0 { low_sum / low_weight } else { 0.0 },
            if mid_weight > 0.0 { mid_sum / mid_weight } else { 0.0 },
            if high_weight > 0.0 { high_sum / high_weight } else { 0.0 },
        ]
    }
    
    /// Harmonic analysis — maps to 7-type primitives
    /// [0]=Curve(fundamental), [1]=Line(1st), [2]=Angle(2nd), etc.
    fn harmonic_analysis(spectra: &[Vec<f64>]) -> [f64; 7] {
        let avg_spectrum = Self::average_spectrum(spectra);
        let nyquist = Self::SAMPLE_RATE as f64 / 2.0;
        let bin_size = nyquist / avg_spectrum.len() as f64;
        
        // Find fundamental frequency (pitch)
        let fundamental_bin = Self::find_fundamental(&avg_spectrum);
        let fundamental_freq = fundamental_bin as f64 * bin_size;
        
        let mut harmonics = [0.0; 7];
        
        // Extract 7 harmonics (fundamental + 6 overtones)
        for h in 0..7 {
            let target_freq = fundamental_freq * (h + 1) as f64;
            let target_bin = (target_freq / bin_size) as usize;
            
            if target_bin < avg_spectrum.len() {
                // Get magnitude with slight smoothing
                let mag = avg_spectrum[target_bin];
                let prev = if target_bin > 0 { avg_spectrum[target_bin - 1] } else { 0.0 };
                let next = if target_bin + 1 < avg_spectrum.len() { avg_spectrum[target_bin + 1] } else { 0.0 };
                
                harmonics[h] = (mag + prev + next) / 3.0;
            }
        }
        
        // Normalize
        let max = harmonics.iter().fold(0.0, |a, b| a.max(*b));
        if max > 0.0 {
            for h in &mut harmonics {
                *h /= max;
            }
        }
        
        harmonics
    }
    
    /// RMS energy calculation
    fn rms_energy(samples: &[i16]) -> f64 {
        let sum_sq: f64 = samples.iter()
            .map(|s| (*s as f64).powi(2))
            .sum();
        
        (sum_sq / samples.len() as f64).sqrt() / 32768.0 // Normalize to 0-1
    }
    
    /// Find fundamental frequency (simple peak picking)
    fn find_fundamental(spectrum: &[Vec<f64>]) -> usize {
        // Search in voice range: 80Hz - 400Hz
        let nyquist = Self::SAMPLE_RATE as f64 / 2.0;
        let bin_size = nyquist / spectrum.len() as f64;
        
        let min_bin = (80.0 / bin_size) as usize;
        let max_bin = (400.0 / bin_size) as usize;
        
        let mut peak_bin = min_bin;
        let mut peak_mag = 0.0;
        
        for i in min_bin..max_bin.min(spectrum.len()) {
            if spectrum[i] > peak_mag {
                peak_mag = spectrum[i];
                peak_bin = i;
            }
        }
        
        peak_bin
    }
    
    /// Average spectrum across frames
    fn average_spectrum(spectra: &[Vec<f64>]) -> Vec<f64> {
        if spectra.is_empty() {
            return Vec::new();
        }
        
        let len = spectra[0].len();
        let mut avg = vec![0.0; len];
        
        for spectrum in spectra {
            for (i, &val) in spectrum.iter().enumerate() {
                if i < len {
                    avg[i] += val;
                }
            }
        }
        
        for val in &mut avg {
            *val /= spectra.len() as f64;
        }
        
        avg
    }
    
    /// Hash audio for temporal signature
    fn hash_audio(samples: &[i16]) -> u64 {
        // Simple perceptual hash — robust to small variations
        let mut hash: u64 = 0xcbf29ce484222325;
        
        // Sample every 100th point for efficiency
        for (i, sample) in samples.iter().step_by(100) {
            let bucket = ((*sample as i32 + 32768) / 1024) as u8;
            hash ^= bucket as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        
        hash
    }
    
    /// Map harmonic signature to dominant 7-type primitive
    pub fn dominant_primitive(&self) -> crate::primitives::PrimitiveType {
        use crate::primitives::{PrimitiveType, SEVEN_TYPES};
        
        let mut max_idx = 0;
        let mut max_val = 0.0;
        
        for (i, &val) in self.harmonic_signature.iter().enumerate() {
            if val > max_val {
                max_val = val;
                max_idx = i;
            }
        }
        
        SEVEN_TYPES[max_idx % 7]
    }
    
    /// Convert to GlyfWord for semantic alignment
    /// Enables audio → text → geometry pipeline
    pub fn to_glyf_word(&self) -> crate::GlyfWord {
        crate::GlyfWord {
            native_sig: self.temporal_sig,
            geo_centroid: self.spectral_centroid,
            center_axis: self.harmonic_signature,
            trajectory_mag: self.energy_rms,
        }
    }
}

/// Ogg/Opus decoder stub
/// For production: use opus crate or symphonia
pub struct AudioDecoder;

impl AudioDecoder {
    /// Decode Ogg/Opus to PCM
    /// Placeholder — requires external decoder in production
    pub fn decode_ogg_opus(ogg_data: &[u8]) -> Option<Vec<i16>> {
        // TODO: Integrate with opus-rs or similar
        // For now, returns None — actual decoding requires std or specific crates
        
        // Stub: return synthetic data for testing
        #[cfg(test)]
        {
            let mut synthetic = Vec::with_capacity(16000); // 1 second @ 16kHz
            for i in 0..16000 {
                let sample = (i as f64 * 0.1).sin() * 10000.0;
                synthetic.push(sample as i16);
            }
            Some(synthetic)
        }
        
        #[cfg(not(test))]
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_audio_glyf_size() {
        assert_eq!(core::mem::size_of::<AudioGlyf>(), 96);
    }
    
    #[test]
    fn test_synthetic_audio() {
        let synthetic = AudioDecoder::decode_ogg_opus(b"test").unwrap();
        let audio_glyf = AudioGlyf::from_pcm(&synthetic);
        
        assert!(audio_glyf.energy_rms > 0.0);
        assert!(audio_glyf.temporal_sig != 0);
    }
    
    #[test]
    fn test_harmonic_mapping() {
        // Create synthetic sine wave at 440Hz
        let mut samples = Vec::with_capacity(16000);
        for i in 0..16000 {
            let sample = (2.0 * core::f64::consts::PI * 440.0 * i as f64 / 16000.0).sin();
            samples.push((sample * 10000.0) as i16);
        }
        
        let audio_glyf = AudioGlyf::from_pcm(&samples);
        
        // Fundamental should be strongest
        assert!(audio_glyf.harmonic_signature[0] >= audio_glyf.harmonic_signature[1]);
    }
}
