//! Spiral Generation - φ-Harmonic Synonym Navigation
//!
//! Populates the demi-æxis of beauty with synonymous words
//! placed at golden ratio intervals along the trajectory.

use crate::trajectory::{Trajectory, Vector3};

/// Golden ratio constant
const PHI: f64 = 1.618033988749895;

/// Golden angle in radians (137.507764°)
const GOLDEN_ANGLE: f64 = 2.399963229728653;

/// Point along the synonym spiral
#[derive(Clone, Debug)]
pub struct SpiralPoint {
    /// The synonym word
    pub word: alloc::string::String,
    /// 3D position
    pub position: Vector3,
    /// Distance from center (0 = at L3, 1 = at L2)
    pub distance_from_center: f64,
    /// Geometric deviation from base word (0 = identical, 1 = maximally different)
    pub geometric_deviation: f64,
    /// Spiral radius at this point
    pub spiral_radius: f64,
}

/// φ-Spiral synonym navigation path
#[derive(Clone, Debug)]
pub struct SynonymSpiral {
    pub points: alloc::vec::Vec<SpiralPoint>,
    pub base_trajectory: Trajectory,
}

impl SynonymSpiral {
    /// Generate spiral from trajectory and synonym list
    pub fn generate(trajectory: &Trajectory, synonyms: &[&str]) -> Self {
        let mut points = alloc::vec::Vec::with_capacity(synonyms.len());
        let n = synonyms.len() as f64;
        
        for (i, &word) in synonyms.iter().enumerate() {
            // φ-harmonic progress along trajectory
            let t = (i as f64 + 1.0) / (n + 1.0);
            
            // Exponential spacing via φ
            let phi_t = t.powf(1.0 / PHI);
            
            // Base position along trajectory
            let base_pos = trajectory.point_at(phi_t);
            
            // Spiral offset (perpendicular to trajectory)
            let spiral_angle = i as f64 * GOLDEN_ANGLE;
            let max_radius = trajectory.magnitude * 0.2;
            let radius = max_radius * (1.0 - phi_t) * spiral_angle.sin().abs();
            
            // Offset in XY plane (simplified perpendicular)
            let offset_x = radius * spiral_angle.cos();
            let offset_y = radius * spiral_angle.sin();
            
            let position = Vector3::new(
                base_pos.x + offset_x,
                base_pos.y + offset_y,
                base_pos.z,
            );
            
            points.push(SpiralPoint {
                word: alloc::string::String::from(word),
                position,
                distance_from_center: 1.0 - phi_t,
                geometric_deviation: Self::calculate_deviation(i, synonyms.len()),
                spiral_radius: radius,
            });
        }
        
        Self {
            points,
            base_trajectory: *trajectory,
        }
    }
    
    /// Generate spiral with calculated deviation based on geometric distance
    pub fn generate_with_deviations(
        trajectory: &Trajectory,
        synonyms: &[(&str, f64)], // (word, deviation) pairs
    ) -> Self {
        let mut points = alloc::vec::Vec::with_capacity(synonyms.len());
        
        for (i, (word, deviation)) in synonyms.iter().enumerate() {
            let n = synonyms.len() as f64;
            let t = (i as f64 + 1.0) / (n + 1.0);
            let phi_t = t.powf(1.0 / PHI);
            
            // Deviation affects spiral radius
            let base_radius = trajectory.magnitude * 0.2;
            let radius = base_radius * *deviation * (1.0 - phi_t);
            
            let spiral_angle = i as f64 * GOLDEN_ANGLE;
            let base_pos = trajectory.point_at(phi_t);
            
            let position = Vector3::new(
                base_pos.x + radius * spiral_angle.cos(),
                base_pos.y + radius * spiral_angle.sin(),
                base_pos.z,
            );
            
            points.push(SpiralPoint {
                word: alloc::string::String::from(*word),
                position,
                distance_from_center: 1.0 - phi_t,
                geometric_deviation: *deviation,
                spiral_radius: radius,
            }));
        }
        
        Self {
            points,
            base_trajectory: *trajectory,
        }
    }
    
    /// Calculate synthetic deviation for demo purposes
    fn calculate_deviation(index: usize, total: usize) -> f64 {
        // More central synonyms = lower deviation
        let center = total / 2;
        let dist_from_center = (index as isize - center as isize).abs() as f64;
        dist_from_center / (total as f64 / 2.0)
    }
    
    /// Get spiral as array of points for WebGL
    pub fn to_line_points(&self) -> alloc::vec::Vec<[f64; 3]> {
        // Start from origin
        let mut points = alloc::vec::Vec::with_capacity(self.points.len() + 2);
        points.push([
            self.base_trajectory.origin.x,
            self.base_trajectory.origin.y,
            self.base_trajectory.origin.z,
        ]);
        
        // Add spiral points
        for p in &self.points {
            points.push([p.position.x, p.position.y, p.position.z]);
        }
        
        // End at destination
        points.push([
            self.base_trajectory.destination.x,
            self.base_trajectory.destination.y,
            self.base_trajectory.destination.z,
        ]);
        
        points
    }
    
    /// Get closest point to a given 3D position
    pub fn nearest_point(&self, pos: Vector3) -> Option<&SpiralPoint> {
        self.points.iter().min_by(|a, b| {
            let dist_a = pos.distance(a.position);
            let dist_b = pos.distance(b.position);
            dist_a.partial_cmp(&dist_b).unwrap_or(core::cmp::Ordering::Equal)
        })
    }
}

/// The Demi-Æxis of Beauty - organizes ambiguity geometrically
pub struct DemiAxis {
    pub base_word: alloc::string::String,
    pub spiral: SynonymSpiral,
    pub nave_center: Vector3, // L3 Center Æxis
}

impl DemiAxis {
    /// Create demi-æxis from base word and its semantic neighbors
    pub fn new(base_word: &str, spiral: SynonymSpiral) -> Self {
        Self {
            base_word: alloc::string::String::from(base_word),
            nave_center: spiral.base_trajectory.destination,
            spiral,
        }
    }
    
    /// Navigate to nearest synonym from a position
    pub fn navigate(&self, from_pos: Vector3) -> Option<&SpiralPoint> {
        self.spiral.nearest_point(from_pos)
    }
    
    /// Get all synonyms sorted by distance from center
    pub fn synonyms_by_proximity(&self) -> alloc::vec::Vec<&SpiralPoint> {
        let mut sorted: alloc::vec::Vec<_> = self.spiral.points.iter().collect();
        sorted.sort_by(|a, b| {
            a.distance_from_center
                .partial_cmp(&b.distance_from_center)
                .unwrap_or(core::cmp::Ordering::Equal)
        });
        sorted
    }
}

extern crate alloc;
