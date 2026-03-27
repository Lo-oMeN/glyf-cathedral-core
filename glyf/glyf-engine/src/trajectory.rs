//! Trajectory Calculation - L2 (Geo-Light) to L3 (Center Æxis)
//!
//! Calculates the deterministic vector from geometric instantiation
//! to semantic essence, generating the pathway for synonym navigation.

use crate::primitives::Primitive;
use crate::glyphoform::GlyphoformMapping;
use crate::GlyfError;

/// 3D Vector for coordinate math
#[derive(Copy, Clone, Debug, Default)]
pub struct Vector3 {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Vector3 {
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self { x, y, z }
    }
    
    pub fn from_array(arr: [f64; 3]) -> Self {
        Self { x: arr[0], y: arr[1], z: arr[2] }
    }
    
    pub fn to_array(self) -> [f64; 3] {
        [self.x, self.y, self.z]
    }
    
    /// Euclidean magnitude
    pub fn magnitude(self) -> f64 {
        (self.x*self.x + self.y*self.y + self.z*self.z).sqrt()
    }
    
    /// Normalize to unit vector
    pub fn normalize(self) -> Self {
        let mag = self.magnitude();
        if mag > 0.0 {
            Self {
                x: self.x / mag,
                y: self.y / mag,
                z: self.z / mag,
            }
        } else {
            self
        }
    }
    
    /// Distance to another vector
    pub fn distance(self, other: Vector3) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        (dx*dx + dy*dy + dz*dz).sqrt()
    }
}

/// Collection of primitives forming a word's geometric cloud
#[derive(Clone, Debug)]
pub struct CoordinateCloud {
    pub points: alloc::vec::Vec<Primitive>,
    pub word_length: usize,
}

impl CoordinateCloud {
    const LETTER_WIDTH: f64 = 1.0;
    const LETTER_HEIGHT: f64 = 1.0;
    
    /// Convert word to L2 (Geo-Light) coordinate cloud
    pub fn from_word(word: &str, mapping: &GlyphoformMapping) 
        -> Result<Self, GlyfError> {
        
        if word.is_empty() {
            return Err(GlyfError::EmptyWord);
        }
        
        let mut points = alloc::vec::Vec::new();
        let chars: alloc::vec::Vec<char> = word.chars().collect();
        
        for (i, c) in chars.iter().enumerate() {
            if !c.is_ascii_alphabetic() {
                return Err(GlyfError::InvalidCharacter(*c));
            }
            
            let signature = mapping.get(*c)
                .ok_or(GlyfError::InvalidCharacter(*c))?;
            
            let x_offset = i as f64 * Self::LETTER_WIDTH;
            
            for primitive in signature.to_primitives(x_offset, i) {
                points.push(primitive);
            }
        }
        
        Ok(Self {
            points,
            word_length: chars.len(),
        })
    }
    
    /// Calculate geometric centroid (L2 center point)
    pub fn centroid(&self) -> [f64; 3] {
        if self.points.is_empty() {
            return [0.0, 0.0, 0.0];
        }
        
        let mut sum_x = 0.0;
        let mut sum_y = 0.0;
        let mut sum_z = 0.0;
        
        for p in &self.points {
            sum_x += p.x;
            sum_y += p.y;
            sum_z += p.z;
        }
        
        let n = self.points.len() as f64;
        [sum_x/n, sum_y/n, sum_z/n]
    }
    
    /// Get bounding box
    pub fn bounds(&self) -> ([f64; 3], [f64; 3]) {
        if self.points.is_empty() {
            return ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]);
        }
        
        let mut min = [f64::INFINITY; 3];
        let mut max = [f64::NEG_INFINITY; 3];
        
        for p in &self.points {
            min[0] = min[0].min(p.x);
            min[1] = min[1].min(p.y);
            min[2] = min[2].min(p.z);
            max[0] = max[0].max(p.x);
            max[1] = max[1].max(p.y);
            max[2] = max[2].max(p.z);
        }
        
        (min, max)
    }
    
    /// Normalize coordinates to unit space (0-1 range)
    pub fn normalize(&mut self) {
        let (min, max) = self.bounds();
        
        let range_x = max[0] - min[0];
        let range_y = max[1] - min[1];
        let range_z = max[2] - min[2];
        
        for p in &mut self.points {
            if range_x > 0.0 { p.x = (p.x - min[0]) / range_x; }
            if range_y > 0.0 { p.y = (p.y - min[1]) / range_y; }
            if range_z > 0.0 { p.z = (p.z - min[2]) / range_z; }
        }
    }
}

/// Trajectory from L2 (Geo-Light) to L3 (Center Æxis)
#[derive(Copy, Clone, Debug)]
pub struct Trajectory {
    /// Starting point (Geo-Light centroid)
    pub origin: Vector3,
    /// Destination (Center Æxis in 3D space)
    pub destination: Vector3,
    /// Vector magnitude (distance)
    pub magnitude: f64,
    /// Unit direction vector
    pub direction: Vector3,
}

impl Default for Trajectory {
    fn default() -> Self {
        Self {
            origin: Vector3::new(0.0, 0.0, 0.0),
            destination: Vector3::new(1.0, 1.0, 1.0),
            magnitude: 1.732,
            direction: Vector3::new(0.577, 0.577, 0.577),
        }
    }
}

impl Trajectory {
    /// Calculate trajectory from cloud to semantic center
    pub fn calculate(cloud: &CoordinateCloud, center_axis: &[f64; 7]) 
        -> Result<Self, GlyfError> {
        
        let origin = Vector3::from_array(cloud.centroid());
        
        // Project 7D semantic vector to 3D for visualization
        // Simple projection: first 3 dimensions map to x,y,z
        // This is deterministic and reversible
        let destination = Self::project_semantic_to_3d(center_axis);
        
        let dx = destination.x - origin.x;
        let dy = destination.y - origin.y;
        let dz = destination.z - origin.z;
        
        let magnitude = (dx*dx + dy*dy + dz*dz).sqrt();
        
        let direction = if magnitude > 0.0 {
            Vector3::new(dx/magnitude, dy/magnitude, dz/magnitude)
        } else {
            Vector3::new(0.0, 0.0, 0.0)
        };
        
        Ok(Self {
            origin,
            destination,
            magnitude,
            direction,
        })
    }
    
    /// Project 7D semantic vector to 3D coordinate space
    fn project_semantic_to_3d(center_axis: &[f64; 7]) -> Vector3 {
        // Use first 3 dimensions as primary axes
        // Remaining 4 contribute through φ-weighted combination
        const PHI: f64 = 1.618033988749895;
        
        let x = center_axis[0] + center_axis[3]/PHI + center_axis[6]/(PHI*PHI);
        let y = center_axis[1] + center_axis[4]/PHI;
        let z = center_axis[2] + center_axis[5]/PHI;
        
        Vector3::new(x, y, z).normalize()
    }
    
    /// Get point at t along trajectory (0.0 = origin, 1.0 = destination)
    pub fn point_at(self, t: f64) -> Vector3 {
        Vector3::new(
            self.origin.x + self.direction.x * self.magnitude * t,
            self.origin.y + self.direction.y * self.magnitude * t,
            self.origin.z + self.direction.z * self.magnitude * t,
        )
    }
}

// Need alloc for Vec
extern crate alloc;
