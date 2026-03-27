//! 7-Type Glyphobetic Primitive System
//! 
//! Universal morpho-geometric primitives:
//! 1. Curve (∿) - flow, return, cyclical
//! 2. Line (│) - direction, will, extension  
//! 3. Angle (∠) - tension, decision, break
//! 4. Vesica (⧖) - union, intersection, birth
//! 5. Spiral (꩜) - evolution, returning, deepening
//! 6. Node (●) - point, singularity, awareness
//! 7. Field (▥) - container, ground, context

/// The seven universal primitives
pub const SEVEN_TYPES: [PrimitiveType; 7] = [
    PrimitiveType::Curve,
    PrimitiveType::Line,
    PrimitiveType::Angle,
    PrimitiveType::Vesica,
    PrimitiveType::Spiral,
    PrimitiveType::Node,
    PrimitiveType::Field,
];

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
pub enum PrimitiveType {
    Curve = 0,   // ∿ - flow, return, cyclical
    Line = 1,    // │ - direction, will, extension
    Angle = 2,   // ∠ - tension, decision, break
    Vesica = 3,  // ⧖ - union, intersection, birth
    Spiral = 4,  // ꩜ - evolution, returning, deepening
    Node = 5,    // ● - point, singularity, awareness
    Field = 6,   // ▥ - container, ground, context
}

impl PrimitiveType {
    /// Convert to index (0-6)
    pub fn to_index(self) -> usize {
        self as usize
    }
    
    /// Get from index
    pub fn from_index(idx: usize) -> Option<Self> {
        match idx {
            0 => Some(PrimitiveType::Curve),
            1 => Some(PrimitiveType::Line),
            2 => Some(PrimitiveType::Angle),
            3 => Some(PrimitiveType::Vesica),
            4 => Some(PrimitiveType::Spiral),
            5 => Some(PrimitiveType::Node),
            6 => Some(PrimitiveType::Field),
            _ => None,
        }
    }
    
    /// Get symbol representation
    pub fn symbol(self) -> &'static str {
        match self {
            PrimitiveType::Curve => "∿",
            PrimitiveType::Line => "│",
            PrimitiveType::Angle => "∠",
            PrimitiveType::Vesica => "⧖",
            PrimitiveType::Spiral => "꩜",
            PrimitiveType::Node => "●",
            PrimitiveType::Field => "▥",
        }
    }
    
    /// Get semantic field keywords
    pub fn semantic_field(self) -> &'static [&'static str] {
        match self {
            PrimitiveType::Curve => &["flow", "return", "cyclical", "receptivity", "yin"],
            PrimitiveType::Line => &["direction", "will", "extension", "force", "yang"],
            PrimitiveType::Angle => &["tension", "decision", "break", "edge", "crisis"],
            PrimitiveType::Vesica => &["union", "intersection", "birth", "portal", "lens"],
            PrimitiveType::Spiral => &["evolution", "returning", "deepening", "time", "growth"],
            PrimitiveType::Node => &["point", "singularity", "awareness", "focus", "self"],
            PrimitiveType::Field => &["container", "ground", "context", "possibility", "space"],
        }
    }
}

/// A primitive instance with 3D coordinates
#[derive(Copy, Clone, Debug)]
pub struct Primitive {
    pub primitive: PrimitiveType,
    pub x: f64,
    pub y: f64,
    pub z: f64,
    /// Letter index this primitive belongs to
    pub letter_index: usize,
}

impl Primitive {
    pub fn new(primitive: PrimitiveType, x: f64, y: f64, letter_index: usize) -> Self {
        Self {
            primitive,
            x,
            y,
            z: 0.0,
            letter_index,
        }
    }
    
    /// Euclidean distance to another primitive
    pub fn distance(&self, other: &Primitive) -> f64 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        (dx*dx + dy*dy + dz*dz).sqrt()
    }
    
    /// Vector from this primitive to another
    pub fn vector_to(&self, other: &Primitive) -> [f64; 3] {
        [
            other.x - self.x,
            other.y - self.y,
            other.z - self.z,
        ]
    }
}
