//! Glyphoform Mapping - A-Z Letterform to Geometric Primitives
//!
//! Maps each English letter to its constituent geometric primitives
//! based on the validated GLYF packet specification.

use crate::primitives::{Primitive, PrimitiveType};
use crate::GlyfError;

/// Geometric signature of a single letter
#[derive(Clone, Debug)]
pub struct LetterSignature {
    /// Letter character
    pub letter: char,
    /// Constituent primitives in order
    pub primitives: &'static [PrimitiveType],
    /// Human-readable description
    pub signature: &'static str,
    /// Spatial description
    pub coordinates: &'static str,
}

impl LetterSignature {
    /// Generate coordinate primitives for this letter
    /// x_offset: horizontal position in word
    pub fn to_primitives(&self, x_offset: f64, letter_index: usize
    ) -> impl Iterator<Item = Primitive> + '_ {
        let primitive_count = self.primitives.len();
        
        self.primitives.iter().enumerate().map(move |(i, &ptype)| {
            // Space primitives vertically within letter height
            // and horizontally with letter spacing
            let y = 0.5 + (i as f64 / primitive_count as f64 - 0.5) * 0.8;
            let x = x_offset + (i as f64 / primitive_count as f64) * 0.6;
            
            Primitive::new(ptype, x, y, letter_index)
        })
    }
}

/// Complete A-Z glyphoform mapping
pub struct GlyphoformMapping {
    signatures: [Option<LetterSignature>; 26],
}

impl Default for GlyphoformMapping {
    fn default() -> Self {
        let mut mapping = Self {
            signatures: Default::default(),
        };
        mapping.init();
        mapping
    }
}

impl GlyphoformMapping {
    fn init(&mut self) {
        // A-Z mapping per GLYF packet specification
        self.set('A', &[PrimitiveType::Angle, PrimitiveType::Line, PrimitiveType::Line],
            "Peak/tension", "Two ascending lines meeting at node (apex)");
        
        self.set('B', &[PrimitiveType::Vesica, PrimitiveType::Vesica, PrimitiveType::Line],
            "Double enclosure", "Vertical spine with two right-side bowls");
        
        self.set('C', &[PrimitiveType::Curve],
            "Opening/receptivity", "Single concave curve, open right");
        
        self.set('D', &[PrimitiveType::Vesica, PrimitiveType::Line],
            "Containment", "Vertical spine with right-side bowl");
        
        self.set('E', &[PrimitiveType::Line, PrimitiveType::Line, PrimitiveType::Line, PrimitiveType::Line],
            "Extension/existence", "Vertical spine with three parallel horizontals");
        
        self.set('F', &[PrimitiveType::Line, PrimitiveType::Line, PrimitiveType::Line],
            "Incomplete extension", "Vertical spine with two parallel horizontals (truncated E)");
        
        self.set('G', &[PrimitiveType::Curve, PrimitiveType::Line, PrimitiveType::Angle],
            "Retaining/opening", "C-form with internal horizontal hook");
        
        self.set('H', &[PrimitiveType::Line, PrimitiveType::Line, PrimitiveType::Line],
            "Bridge/connection", "Two verticals joined by central horizontal");
        
        self.set('I', &[PrimitiveType::Line, PrimitiveType::Node],
            "Singular existence", "Vertical line with terminal nodes");
        
        self.set('J', &[PrimitiveType::Curve, PrimitiveType::Node],
            "Descent", "Descending curve with bottom node");
        
        self.set('K', &[PrimitiveType::Line, PrimitiveType::Angle, PrimitiveType::Angle],
            "Bifurcation", "Vertical spine with two angled arms");
        
        self.set('L', &[PrimitiveType::Line, PrimitiveType::Line],
            "Grounding", "Vertical descending to horizontal base");
        
        self.set('M', &[PrimitiveType::Line, PrimitiveType::Angle, PrimitiveType::Angle, PrimitiveType::Line],
            "Peak/duality", "Double ascending/descending angle structure");
        
        self.set('N', &[PrimitiveType::Line, PrimitiveType::Angle, PrimitiveType::Line],
            "Connection across", "Diagonal join between two verticals");
        
        self.set('O', &[PrimitiveType::Vesica],
            "Wholeness/void", "Closed elliptical curve");
        
        self.set('P', &[PrimitiveType::Vesica, PrimitiveType::Line],
            "Partial containment", "Vertical spine with single upper bowl");
        
        self.set('Q', &[PrimitiveType::Vesica, PrimitiveType::Angle],
            "Pierced wholeness", "O-form with penetrating tail");
        
        self.set('R', &[PrimitiveType::Vesica, PrimitiveType::Line, PrimitiveType::Angle],
            "Standing/motion", "P-form with descending leg angle");
        
        self.set('S', &[PrimitiveType::Curve, PrimitiveType::Curve],
            "Double flow", "Two opposing curves, sigmoid form");
        
        self.set('T', &[PrimitiveType::Line, PrimitiveType::Line],
            "Crossing", "Horizontal bisected by vertical center");
        
        self.set('U', &[PrimitiveType::Curve],
            "Container base", "Concave upward curve (open top)");
        
        self.set('V', &[PrimitiveType::Line, PrimitiveType::Angle],
            "Funnel/convergence", "Two lines meeting at bottom node");
        
        self.set('W', &[PrimitiveType::Line, PrimitiveType::Angle, PrimitiveType::Angle, PrimitiveType::Line],
            "Double valley", "Double V-structure, oscillation");
        
        self.set('X', &[PrimitiveType::Angle, PrimitiveType::Angle],
            "Crossing/intersection", "Two diagonal lines crossing at central node");
        
        self.set('Y', &[PrimitiveType::Line, PrimitiveType::Line, PrimitiveType::Angle],
            "Bifurcation with base", "V-form descending to single vertical");
        
        self.set('Z', &[PrimitiveType::Line, PrimitiveType::Angle, PrimitiveType::Line],
            "Lightning/refraction", "Horizontal-diagonal-horizontal zigzag");
    }
    
    fn set(&mut self, letter: char, primitives: &'static [PrimitiveType], 
          signature: &'static str, coordinates: &'static str) {
        let idx = (letter.to_ascii_uppercase() as u8 - b'A') as usize;
        if idx < 26 {
            self.signatures[idx] = Some(LetterSignature {
                letter,
                primitives,
                signature,
                coordinates,
            });
        }
    }
    
    /// Get signature for a letter
    pub fn get(&self, letter: char) -> Option<&LetterSignature> {
        if !letter.is_ascii_alphabetic() {
            return None;
        }
        let idx = (letter.to_ascii_uppercase() as u8 - b'A') as usize;
        self.signatures.get(idx).and_then(|s| s.as_ref())
    }
    
    /// Check if character is valid (A-Z)
    pub fn is_valid(c: char) -> bool {
        c.is_ascii_alphabetic()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_mapping_complete() {
        let mapping = GlyphoformMapping::default();
        
        // Verify all A-Z exist
        for c in 'A'..='Z' {
            assert!(mapping.get(c).is_some(), "Missing mapping for {}", c);
        }
    }
    
    #[test]
    fn test_resilience() {
        let mapping = GlyphoformMapping::default();
        
        // R-E-S-I-L-I-E-N-C-E
        assert_eq!(mapping.get('R').unwrap().primitives.len(), 3);
        assert_eq!(mapping.get('E').unwrap().primitives.len(), 4);
        assert_eq!(mapping.get('S').unwrap().primitives.len(), 2);
    }
}
