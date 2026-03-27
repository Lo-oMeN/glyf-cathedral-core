//! GLYF Lexicon Eyes - Core Parser Engine
//! 
//! 3-Layer Semantic Decompression:
//! L1: Native Glyff (alphabetic) → L2: Geo-Light (geometric) → L3: Center Æxis (semantic)

#![cfg_attr(not(feature = "std"), no_std)]

extern crate alloc;

pub mod primitives;
pub mod glyphoform;
pub mod trajectory;
pub mod spiral;
pub mod audio_transformer;

use primitives::{PrimitiveType, SEVEN_TYPES};
use glyphoform::GlyphoformMapping;
use trajectory::{CoordinateCloud, Trajectory};
use spiral::SynonymSpiral;

/// 96-byte sacred structure for each word
/// Matches the packet specification exactly
#[repr(C, align(64))]
#[derive(Copy, Clone, Debug)]
pub struct GlyfWord {
    /// Native signature (8 bytes) - word hash/index
    pub native_sig: u64,
    
    /// Geo-coordinate centroid (24 bytes) - 3×f64
    pub geo_centroid: [f64; 3],
    
    /// Center Æxis - 7-dimensional semantic vector (56 bytes) - 7×f64
    /// Each dimension corresponds to one of the 7 primitives
    pub center_axis: [f64; 7],
    
    /// Trajectory magnitude (8 bytes)
    pub trajectory_mag: f64,
}

impl GlyfWord {
    pub const SIZE: usize = 96;
    
    /// Parse L1 (Native Glyff) → L2 (Geo-Light)
    pub fn from_native(word: &str) -> Result<Self, GlyfError> {
        let mapping = GlyphoformMapping::default();
        let cloud = CoordinateCloud::from_word(word, &mapping)?;
        let centroid = cloud.centroid();
        
        // Derive center axis from geometry
        let center_axis = Self::derive_semantic_vector(&cloud);
        
        let trajectory = Trajectory::calculate(&cloud, &center_axis)?;
        
        Ok(Self {
            native_sig: Self::hash_word(word),
            geo_centroid: centroid,
            center_axis,
            trajectory_mag: trajectory.magnitude,
        })
    }
    
    /// Hash word to native signature
    fn hash_word(word: &str) -> u64 {
        // Simple FNV-1a hash
        let mut hash: u64 = 0xcbf29ce484222325;
        for byte in word.bytes() {
            hash ^= byte as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        hash
    }
    
    /// Derive 7-dimensional semantic vector from geometric cloud
    fn derive_semantic_vector(cloud: &CoordinateCloud) -> [f64; 7] {
        let mut vector = [0.0; 7];
        let total = cloud.points.len() as f64;
        
        if total == 0.0 {
            return vector;
        }
        
        // Count primitive occurrences
        for point in &cloud.points {
            let idx = point.primitive.to_index();
            vector[idx] += 1.0;
        }
        
        // Normalize to unit vector
        let sum: f64 = vector.iter().sum();
        if sum > 0.0 {
            for v in &mut vector {
                *v /= sum;
            }
        }
        
        vector
    }
    
    /// Get dominant primitive (highest dimension in Center Æxis)
    pub fn dominant_primitive(&self) -> PrimitiveType {
        let mut max_idx = 0;
        let mut max_val = 0.0;
        
        for (i, &val) in self.center_axis.iter().enumerate() {
            if val > max_val {
                max_val = val;
                max_idx = i;
            }
        }
        
        SEVEN_TYPES[max_idx]
    }
    
    /// Generate synonym spiral for this word
    pub fn generate_spiral(&self, synonyms: &[&str]) -> SynonymSpiral {
        // This is a simplified version - in production would recalculate trajectory
        // For now, create a default trajectory
        let default_traj = Trajectory::default();
        SynonymSpiral::generate(&default_traj, synonyms)
    }
}

impl Default for GlyfWord {
    fn default() -> Self {
        Self {
            native_sig: 0,
            geo_centroid: [0.0, 0.0, 0.0],
            center_axis: [0.0; 7],
            trajectory_mag: 0.0,
        }
    }
}

#[derive(Debug, Clone)]
pub enum GlyfError {
    InvalidCharacter(char),
    EmptyWord,
}

impl core::fmt::Display for GlyfError {
    fn fmt(&self, f: &mut core::fmt::Formatter) -> core::fmt::Result {
        match self {
            GlyfError::InvalidCharacter(c) => write!(f, "Invalid character: {}", c),
            GlyfError::EmptyWord => write!(f, "Empty word"),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for GlyfError {}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_word_parsing() {
        let word = GlyfWord::from_native("RESILIENCE").unwrap();
        assert!(word.trajectory_mag >= 0.0);
        assert_eq!(word.native_sig, GlyfWord::hash_word("RESILIENCE"));
    }
    
    #[test]
    fn test_size() {
        assert_eq!(core::mem::size_of::<GlyfWord>(), 96);
    }
    
    #[test]
    fn test_hash_consistency() {
        let h1 = GlyfWord::hash_word("TEST");
        let h2 = GlyfWord::hash_word("TEST");
        assert_eq!(h1, h2);
    }
    
    #[test]
    fn test_dominant_primitive() {
        let mut word = GlyfWord::default();
        word.center_axis[2] = 0.8; // Angle dominant
        word.center_axis[0] = 0.2;
        
        assert_eq!(word.dominant_primitive(), PrimitiveType::Angle);
    }
}
