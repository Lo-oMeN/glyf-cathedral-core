//! Glyphoform Traversal — Ordered, Non-Communicable, Emergent
//! 
//! Key insight: Line→Line→Circle ≠ Circle→Line→Line
//! The ORDER of primitives creates the topology.

#![cfg_attr(not(feature = "std"), no_std)]

extern crate alloc;
use alloc::vec::Vec;

use crate::primitives::PrimitiveType;

/// A single stroke in a letterform
/// Non-communicable: has specific spacetime coordinates
#[derive(Copy, Clone, Debug)]
pub struct Stroke {
    /// The primitive type (Line, Curve, Vesica, etc.)
    pub primitive: PrimitiveType,
    /// Start coordinate [x, y] — normalized 0-1
    pub from: [f64; 2],
    /// End coordinate [x, y] — normalized 0-1
    pub to: [f64; 2],
    /// Stroke order (1st, 2nd, 3rd...)
    pub order: u8,
    /// Pen state (true = drawing, false = moving)
    pub is_drawn: bool,
}

impl Stroke {
    pub fn new(primitive: PrimitiveType, from: [f64; 2], to: [f64; 2], order: u8) -> Self {
        Self {
            primitive,
            from,
            to,
            order,
            is_drawn: true,
        }
    }
    
    /// Create a "move" stroke (pen up, repositioning)
    pub fn move_to(to: [f64; 2], order: u8) -> Self {
        Self {
            primitive: PrimitiveType::Node, // Move is just a node
            from: to,
            to,
            order,
            is_drawn: false,
        }
    }
    
    /// Vector representation of stroke
    pub fn vector(&self) -> [f64; 2] {
        [self.to[0] - self.from[0], self.to[1] - self.from[1]]
    }
    
    /// Length of stroke
    pub fn length(&self) -> f64 {
        let dx = self.to[0] - self.from[0];
        let dy = self.to[1] - self.from[1];
        (dx*dx + dy*dy).sqrt()
    }
    
    /// Angle of stroke (in radians)
    pub fn angle(&self) -> f64 {
        let dx = self.to[0] - self.from[0];
        let dy = self.to[1] - self.from[1];
        dy.atan2(dx)
    }
}

/// A letterform as ordered traversal
/// The SEQUENCE of strokes creates the topology
#[derive(Clone, Debug)]
pub struct GlyphoformTraversal {
    pub letter: char,
    pub strokes: Vec<Stroke>,
}

impl GlyphoformTraversal {
    /// Get primitive at specific stroke order
    pub fn primitive_at(&self, order: u8) -> Option<PrimitiveType> {
        self.strokes.iter()
            .find(|s| s.order == order)
            .map(|s| s.primitive)
    }
    
    /// Detect emergent Angles at Line→Line transitions
    /// An Angle appears where two consecutive Lines meet at a vertex
    pub fn emergent_angles(&self) -> Vec<AngleInstance> {
        let mut angles = Vec::new();
        
        for i in 0..self.strokes.len().saturating_sub(1) {
            let stroke1 = &self.strokes[i];
            let stroke2 = &self.strokes[i + 1];
            
            // Angle emerges where two Lines meet at a vertex
            if stroke1.primitive == PrimitiveType::Line 
                && stroke2.primitive == PrimitiveType::Line {
                
                // Check if stroke1 ends where stroke2 begins (vertex)
                let dx = (stroke1.to[0] - stroke2.from[0]).abs();
                let dy = (stroke1.to[1] - stroke2.from[1]).abs();
                
                if dx < 0.01 && dy < 0.01 {
                    // Calculate angle between strokes
                    let angle1 = stroke1.angle();
                    let angle2 = stroke2.angle();
                    let vertex_angle = (angle2 - angle1).abs();
                    
                    angles.push(AngleInstance {
                        vertex: stroke1.to,
                        incoming_angle: angle1,
                        outgoing_angle: angle2,
                        vertex_angle,
                        stroke_order: stroke1.order,
                    });
                }
            }
        }
        
        angles
    }
    
    /// Detect emergent Vesicas from Curve closures
    /// A Vesica emerges where a Curve forms a lens shape
    pub fn emergent_vesicas(&self) -> Vec<VesicaInstance> {
        let mut vesicas = Vec::new();
        
        // Find Curve strokes that could form vesicas
        let curves: Vec<&Stroke> = self.strokes.iter()
            .filter(|s| s.primitive == PrimitiveType::Curve)
            .collect();
        
        // Check for overlapping curves (simplified vesica detection)
        for i in 0..curves.len() {
            for j in (i+1)..curves.len() {
                let c1 = curves[i];
                let c2 = curves[j];
                
                // Rough overlap check
                let mid1 = [(c1.from[0] + c1.to[0])/2.0, (c1.from[1] + c1.to[1])/2.0];
                let mid2 = [(c2.from[0] + c2.to[0])/2.0, (c2.from[1] + c2.to[1])/2.0];
                let dist = ((mid1[0]-mid2[0]).powi(2) + (mid1[1]-mid2[1]).powi(2)).sqrt();
                
                if dist < 0.3 { // Threshold for overlap
                    vesicas.push(VesicaInstance {
                        curves: (c1.order, c2.order),
                        center: [(mid1[0] + mid2[0])/2.0, (mid1[1] + mid2[1])/2.0],
                    });
                }
            }
        }
        
        vesicas
    }
    
    /// Get all primitives (explicit + emergent)
    pub fn all_primitives(&self) -> Vec<(PrimitiveType, [f64; 2])> {
        let mut result = Vec::new();
        
        // Explicit primitives (from strokes)
        for stroke in &self.strokes {
            if stroke.is_drawn {
                result.push((stroke.primitive, stroke.from));
            }
        }
        
        // Emergent primitives
        for angle in self.emergent_angles() {
            result.push((PrimitiveType::Angle, angle.vertex));
        }
        
        for vesica in self.emergent_vesicas() {
            result.push((PrimitiveType::Vesica, vesica.center));
        }
        
        result
    }
    
    /// Generate coordinate cloud for this letter
    /// Each stroke contributes points along its path
    pub fn to_coordinate_cloud(&self, x_offset: f64) -> Vec< crate::trajectory::PrimitivePoint > {
        use crate::trajectory::PrimitivePoint;
        
        let mut cloud = Vec::new();
        
        for stroke in &self.strokes {
            if !stroke.is_drawn { continue; }
            
            // Sample points along stroke
            let samples = 3; // Start, middle, end
            for i in 0..samples {
                let t = i as f64 / (samples - 1) as f64;
                let x = stroke.from[0] + (stroke.to[0] - stroke.from[0]) * t + x_offset;
                let y = stroke.from[1] + (stroke.to[1] - stroke.from[1]) * t;
                
                cloud.push(PrimitivePoint::new(
                    stroke.primitive,
                    x,
                    y,
                    0, // letter_index set by caller
                ));
            }
        }
        
        cloud
    }
}

/// An emergent Angle instance
#[derive(Copy, Clone, Debug)]
pub struct AngleInstance {
    pub vertex: [f64; 2],
    pub incoming_angle: f64,
    pub outgoing_angle: f64,
    pub vertex_angle: f64, // The angle at the vertex
    pub stroke_order: u8,
}

/// An emergent Vesica instance
#[derive(Copy, Clone, Debug)]
pub struct VesicaInstance {
    pub curves: (u8, u8), // Stroke orders of overlapping curves
    pub center: [f64; 2],
}

/// Complete A-Z traversal mappings
/// Each letter has its OWN grammar — non-communicable
pub struct TraversalMapping;

impl TraversalMapping {
    /// Get traversal for a letter
    /// Each letter has unique stroke order — this is the STEPPING STONE
    pub fn get(letter: char) -> Option<GlyphoformTraversal> {
        match letter.to_ascii_uppercase() {
            'A' => Some(Self::a_traversal()),
            'B' => Some(Self::b_traversal()),
            'C' => Some(Self::c_traversal()),
            'D' => Some(Self::d_traversal()),
            'E' => Some(Self::e_traversal()),
            'F' => Some(Self::f_traversal()),
            'G' => Some(Self::g_traversal()),
            'H' => Some(Self::h_traversal()),
            'I' => Some(Self::i_traversal()),
            'J' => Some(Self::j_traversal()),
            'K' => Some(Self::k_traversal()),
            'L' => Some(Self::l_traversal()),
            'M' => Some(Self::m_traversal()),
            'N' => Some(Self::n_traversal()),
            'O' => Some(Self::o_traversal()),
            'P' => Some(Self::p_traversal()),
            'Q' => Some(Self::q_traversal()),
            'R' => Some(Self::r_traversal()),
            'S' => Some(Self::s_traversal()),
            'T' => Some(Self::t_traversal()),
            'U' => Some(Self::u_traversal()),
            'V' => Some(Self::v_traversal()),
            'W' => Some(Self::w_traversal()),
            'X' => Some(Self::x_traversal()),
            'Y' => Some(Self::y_traversal()),
            'Z' => Some(Self::z_traversal()),
            _ => None,
        }
    }
    
    // === A-Z TRAVERSALS (ORDER MATTERS) ===
    
    /// A: Left stroke → Right stroke → Crossbar
    /// Traversal: Line → Line → Line (with emergent Angles at apex and base)
    fn a_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'A',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.5, 1.0], 1),  // Left ascending
                Stroke::new(PrimitiveType::Line, [0.5, 1.0], [1.0, 0.0], 2),  // Right descending
                Stroke::new(PrimitiveType::Line, [0.25, 0.5], [0.75, 0.5], 3), // Crossbar
            ],
        }
    }
    
    /// B: Spine → Top bowl → Bottom bowl
    /// Traversal: Line → Vesica → Vesica
    fn b_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'B',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),    // Spine
                Stroke::new(PrimitiveType::Curve, [0.0, 0.6], [0.5, 0.9], 2),   // Top bowl left
                Stroke::new(PrimitiveType::Curve, [0.5, 0.9], [0.0, 0.6], 3),   // Top bowl right
                Stroke::new(PrimitiveType::Curve, [0.0, 0.1], [0.5, 0.4], 4),   // Bottom bowl left
                Stroke::new(PrimitiveType::Curve, [0.5, 0.4], [0.0, 0.1], 5),   // Bottom bowl right
            ],
        }
    }
    
    /// C: Single curve
    /// Traversal: Curve
    fn c_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'C',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [1.0, 0.8], [0.0, 0.5], 1),   // Upper arc
                Stroke::new(PrimitiveType::Curve, [0.0, 0.5], [1.0, 0.2], 2),   // Lower arc
            ],
        }
    }
    
    /// S: Double curve (opposing)
    /// Traversal: Curve → Curve (creates double-flow topology)
    fn s_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'S',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [0.0, 0.9], [0.5, 0.7], 1),   // Top curve left
                Stroke::new(PrimitiveType::Curve, [0.5, 0.7], [1.0, 0.5], 2),   // Top curve right
                Stroke::new(PrimitiveType::Curve, [1.0, 0.5], [0.5, 0.3], 3),   // Bottom curve left
                Stroke::new(PrimitiveType::Curve, [0.5, 0.3], [0.0, 0.1], 4),   // Bottom curve right
            ],
        }
    }
    
    /// R: Spine → Bowl → Leg
    /// Traversal: Line → Vesica → Line → Angle (different from B!)
    fn r_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'R',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),    // Spine
                Stroke::new(PrimitiveType::Curve, [0.0, 0.6], [0.4, 0.9], 2),   // Bowl left
                Stroke::new(PrimitiveType::Curve, [0.4, 0.9], [0.0, 0.6], 3),   // Bowl right
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [0.5, 0.0], 4),    // Leg
            ],
        }
    }
    
    /// E: Spine → Top → Middle → Bottom
    /// Traversal: Line × 4 (extension pattern)
    fn e_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'E',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),    // Spine
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.7, 1.0], 2),    // Top bar
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [0.6, 0.5], 3),    // Middle bar
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.7, 0.0], 4),    // Bottom bar
            ],
        }
    }
    
    /// O: Circle
    /// Traversal: Curve × 4 (closed loop)
    fn o_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'O',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [0.5, 0.0], [1.0, 0.5], 1),   // Right quadrant
                Stroke::new(PrimitiveType::Curve, [1.0, 0.5], [0.5, 1.0], 2),   // Top quadrant
                Stroke::new(PrimitiveType::Curve, [0.5, 1.0], [0.0, 0.5], 3),   // Left quadrant
                Stroke::new(PrimitiveType::Curve, [0.0, 0.5], [0.5, 0.0], 4),   // Bottom quadrant
            ],
        }
    }
    
    // === REMAINING LETTERS (stub implementations) ===
    // Full implementations would follow same pattern:
    // D, F, G, H, I, J, K, L, M, N, P, Q, T, U, V, W, X, Y, Z
    
    fn d_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'D',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Curve, [0.0, 0.1], [0.6, 0.5], 2),
                Stroke::new(PrimitiveType::Curve, [0.6, 0.5], [0.0, 0.9], 3),
            ],
        }
    }
    
    fn f_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'F',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.7, 1.0], 2),
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [0.6, 0.5], 3),
            ],
        }
    }
    
    fn g_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'G',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [1.0, 0.8], [0.0, 0.5], 1),
                Stroke::new(PrimitiveType::Curve, [0.0, 0.5], [1.0, 0.2], 2),
                Stroke::new(PrimitiveType::Line, [0.5, 0.5], [0.8, 0.5], 3),
                Stroke::new(PrimitiveType::Line, [0.8, 0.5], [0.8, 0.2], 4),
            ],
        }
    }
    
    fn h_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'H',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [1.0, 0.0], [1.0, 1.0], 2),
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [1.0, 0.5], 3),
            ],
        }
    }
    
    fn i_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'I',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.5, 0.0], [0.5, 1.0], 1),
            ],
        }
    }
    
    fn j_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'J',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.5, 1.0], [0.5, 0.2], 1),
                Stroke::new(PrimitiveType::Curve, [0.5, 0.2], [0.0, 0.0], 2),
            ],
        }
    }
    
    fn k_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'K',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [0.7, 1.0], 2),
                Stroke::new(PrimitiveType::Line, [0.0, 0.5], [0.7, 0.0], 3),
            ],
        }
    }
    
    fn l_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'L',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.0, 0.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.7, 0.0], 2),
            ],
        }
    }
    
    fn m_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'M',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.5, 0.5], 2),
                Stroke::new(PrimitiveType::Line, [0.5, 0.5], [1.0, 1.0], 3),
                Stroke::new(PrimitiveType::Line, [1.0, 1.0], [1.0, 0.0], 4),
            ],
        }
    }
    
    fn n_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'N',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [1.0, 0.0], 2),
                Stroke::new(PrimitiveType::Line, [1.0, 0.0], [1.0, 1.0], 3),
            ],
        }
    }
    
    fn p_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'P',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [0.0, 1.0], 1),
                Stroke::new(PrimitiveType::Curve, [0.0, 0.6], [0.5, 0.9], 2),
                Stroke::new(PrimitiveType::Curve, [0.5, 0.9], [0.0, 0.6], 3),
            ],
        }
    }
    
    fn q_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'Q',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [0.5, 0.0], [1.0, 0.5], 1),
                Stroke::new(PrimitiveType::Curve, [1.0, 0.5], [0.5, 1.0], 2),
                Stroke::new(PrimitiveType::Curve, [0.5, 1.0], [0.0, 0.5], 3),
                Stroke::new(PrimitiveType::Curve, [0.0, 0.5], [0.5, 0.0], 4),
                Stroke::new(PrimitiveType::Line, [0.6, 0.3], [0.8, 0.0], 5),
            ],
        }
    }
    
    fn t_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'T',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [1.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.5, 1.0], [0.5, 0.0], 2),
            ],
        }
    }
    
    fn u_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'U',
            strokes: vec![
                Stroke::new(PrimitiveType::Curve, [0.0, 1.0], [0.0, 0.2], 1),
                Stroke::new(PrimitiveType::Curve, [0.0, 0.2], [1.0, 0.2], 2),
                Stroke::new(PrimitiveType::Curve, [1.0, 0.2], [1.0, 1.0], 3),
            ],
        }
    }
    
    fn v_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'V',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.5, 0.0], 1),
                Stroke::new(PrimitiveType::Line, [0.5, 0.0], [1.0, 1.0], 2),
            ],
        }
    }
    
    fn w_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'W',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.25, 0.0], 1),
                Stroke::new(PrimitiveType::Line, [0.25, 0.0], [0.5, 0.5], 2),
                Stroke::new(PrimitiveType::Line, [0.5, 0.5], [0.75, 0.0], 3),
                Stroke::new(PrimitiveType::Line, [0.75, 0.0], [1.0, 1.0], 4),
            ],
        }
    }
    
    fn x_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'X',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [1.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [1.0, 0.0], 2),
            ],
        }
    }
    
    fn y_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'Y',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [0.5, 0.5], 1),
                Stroke::new(PrimitiveType::Line, [0.5, 0.5], [1.0, 1.0], 2),
                Stroke::new(PrimitiveType::Line, [0.5, 0.5], [0.5, 0.0], 3),
            ],
        }
    }
    
    fn z_traversal() -> GlyphoformTraversal {
        GlyphoformTraversal {
            letter: 'Z',
            strokes: vec![
                Stroke::new(PrimitiveType::Line, [0.0, 1.0], [1.0, 1.0], 1),
                Stroke::new(PrimitiveType::Line, [1.0, 1.0], [0.0, 0.0], 2),
                Stroke::new(PrimitiveType::Line, [0.0, 0.0], [1.0, 0.0], 3),
            ],
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_a_emergent_angles() {
        let a = TraversalMapping::get('A').unwrap();
        let angles = a.emergent_angles();
        
        // A has 2 emergent angles (at apex and crossbar ends)
        assert!(angles.len() >= 1);
        
        // Check apex angle
        let apex = angles.iter().find(|a| a.vertex[1] > 0.9);
        assert!(apex.is_some());
    }
    
    #[test]
    fn test_order_matters() {
        // B: Line → Vesica → Vesica
        // R: Line → Vesica → Line (different ending!)
        
        let b = TraversalMapping::get('B').unwrap();
        let r = TraversalMapping::get('R').unwrap();
        
        // B ends with Curve
        let b_last = b.strokes.last().unwrap();
        assert_eq!(b_last.primitive, PrimitiveType::Curve);
        
        // R ends with Line (leg)
        let r_last = r.strokes.last().unwrap();
        assert_eq!(r_last.primitive, PrimitiveType::Line);
    }
    
    #[test]
    fn test_all_letters_exist() {
        for c in 'A'..='Z' {
            assert!(TraversalMapping::get(c).is_some(), "Missing: {}", c);
        }
    }
}
