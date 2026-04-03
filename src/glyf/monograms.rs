//! GLYF Monograms — 26 Letters as Geometric Traversals
//!
//! Each monogram is a path through the 7-segment field.
//! The Hamiltonian path K2→K5→K1→K4→K7→K3→K6 provides the traversal order.
//!
//! Stroke order defines legibility:
//! - Separated state: All segments visible as distinct strokes
//! - Kissing state: Segments connected by ligature bridges
//! - Overlapped state: Single flowing symbol (instant recognition)

use super::lattice_state::{Segment, LatticeState, HamiltonianPath};

/// 26 English monograms (A-Z)
pub const MONOGRAMS: [Monogram; 26] = [
    // A — Triangle + crossbar (Angle → Void → Line)
    Monogram {
        letter: 'A',
        name: "Angle-Apex",
        strokes: &[
            Stroke { segment: Segment::Angle, intensity: 1.0 },
            Stroke { segment: Segment::Void, intensity: 0.8 },
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Void, intensity: 0.8 },
            Stroke { segment: Segment::Angle, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "∧—",  // Two angles with crossbar
            kissing: "∧̲",     // Connected triangle
            overlapped: "A",  // Standard form
        },
    },
    
    // B — Vertical + two bumps (Line → Curve → Curve)
    Monogram {
        letter: 'B',
        name: "Bifurcate",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 0.9 },
            Stroke { segment: Segment::Curve, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "| ) )",
            kissing: "|))",
            overlapped: "B",
        },
    },
    
    // C — Curve opening right
    Monogram {
        letter: 'C',
        name: "Curve-Open",
        strokes: &[
            Stroke { segment: Segment::Curve, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "(",
            kissing: "⊂",
            overlapped: "C",
        },
    },
    
    // D — Vertical + curve closing
    Monogram {
        letter: 'D',
        name: "Dome",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 0.8 },
        ],
        triadic: TriadicForm {
            separated: "| )",
            kissing: "|)",
            overlapped: "D",
        },
    },
    
    // E — Vertical + three horizontals
    Monogram {
        letter: 'E',
        name: "Edge-Three",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "|— — —",
            kissing: "|≡",
            overlapped: "E",
        },
    },
    
    // F — Vertical + two horizontals (top)
    Monogram {
        letter: 'F',
        name: "Fork-Top",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "|— —",
            kissing: "|=",
            overlapped: "F",
        },
    },
    
    // G — Circle + serif
    Monogram {
        letter: 'G',
        name: "Generate-Serif",
        strokes: &[
            Stroke { segment: Segment::Circle, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.7 },
        ],
        triadic: TriadicForm {
            separated: "O—",
            kissing: "G",
            overlapped: "G",
        },
    },
    
    // H — Two verticals + crossbar
    Monogram {
        letter: 'H',
        name: "Height-Connect",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "|—|",
            kissing: "|-|",
            overlapped: "H",
        },
    },
    
    // I — Single vertical
    Monogram {
        letter: 'I',
        name: "I-Beam",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "|",
            kissing: "|",
            overlapped: "I",
        },
    },
    
    // J — Hook curve
    Monogram {
        letter: 'J',
        name: "J-Hook",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 0.8 },
            Stroke { segment: Segment::Curve, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "| )",
            kissing: "J",
            overlapped: "J",
        },
    },
    
    // K — Vertical + two angles
    Monogram {
        letter: 'K',
        name: "Kite",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "| < >",
            kissing: "|⟨⟩",
            overlapped: "K",
        },
    },
    
    // L — Vertical + horizontal base
    Monogram {
        letter: 'L',
        name: "L-Shape",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "|_",
            kissing: "|_",
            overlapped: "L",
        },
    },
    
    // M — Two verticals + two angles (mountain)
    Monogram {
        letter: 'M',
        name: "Mountain",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "|∧∧|",
            kissing: "|⋀|",
            overlapped: "M",
        },
    },
    
    // N — Vertical + diagonal + vertical
    Monogram {
        letter: 'N',
        name: "N-Connect",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "|/|",
            kissing: "|/|",
            overlapped: "N",
        },
    },
    
    // O — Circle
    Monogram {
        letter: 'O',
        name: "Origin-Circle",
        strokes: &[
            Stroke { segment: Segment::Circle, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "O",
            kissing: "O",
            overlapped: "O",
        },
    },
    
    // P — Vertical + loop
    Monogram {
        letter: 'P',
        name: "P-Loop",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "| )",
            kissing: "|)",
            overlapped: "P",
        },
    },
    
    // Q — Circle + tail
    Monogram {
        letter: 'Q',
        name: "Q-Tail",
        strokes: &[
            Stroke { segment: Segment::Circle, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.7 },
        ],
        triadic: TriadicForm {
            separated: "O/",
            kissing: "O/",
            overlapped: "Q",
        },
    },
    
    // R — Vertical + loop + leg
    Monogram {
        letter: 'R',
        name: "R-Leg",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 0.9 },
            Stroke { segment: Segment::Line, intensity: 0.8 },
        ],
        triadic: TriadicForm {
            separated: "| )/",
            kissing: "|)/",
            overlapped: "R",
        },
    },
    
    // S — Double curve
    Monogram {
        letter: 'S',
        name: "S-Curve",
        strokes: &[
            Stroke { segment: Segment::Curve, intensity: 1.0 },
            Stroke { segment: Segment::Curve, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "~ ~",
            kissing: "~~",
            overlapped: "S",
        },
    },
    
    // T — Cross
    Monogram {
        letter: 'T',
        name: "T-Cross",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "—|—",
            kissing: "†",
            overlapped: "T",
        },
    },
    
    // U — Cup curve
    Monogram {
        letter: 'U',
        name: "U-Cup",
        strokes: &[
            Stroke { segment: Segment::Curve, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "U",
            kissing: "U",
            overlapped: "U",
        },
    },
    
    // V — Two angles meeting
    Monogram {
        letter: 'V',
        name: "V-Point",
        strokes: &[
            Stroke { segment: Segment::Angle, intensity: 1.0 },
            Stroke { segment: Segment::Angle, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "\ /",
            kissing: "\/",
            overlapped: "V",
        },
    },
    
    // W — Double V
    Monogram {
        letter: 'W',
        name: "W-Double",
        strokes: &[
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "\/\/",
            kissing: "⋁⋁",
            overlapped: "W",
        },
    },
    
    // X — Two crossing lines
    Monogram {
        letter: 'X',
        name: "X-Cross",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 1.0 },
        ],
        triadic: TriadicForm {
            separated: "\\/",
            kissing: "X",
            overlapped: "X",
        },
    },
    
    // Y — Branch
    Monogram {
        letter: 'Y',
        name: "Y-Branch",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 0.8 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "| < >",
            kissing: "|⟨⟩",
            overlapped: "Y",
        },
    },
    
    // Z — Horizontal + diagonal + horizontal
    Monogram {
        letter: 'Z',
        name: "Z-Zag",
        strokes: &[
            Stroke { segment: Segment::Line, intensity: 0.9 },
            Stroke { segment: Segment::Angle, intensity: 1.0 },
            Stroke { segment: Segment::Line, intensity: 0.9 },
        ],
        triadic: TriadicForm {
            separated: "— / —",
            kissing: "—/—",
            overlapped: "Z",
        },
    },
];

/// A single monogram definition
#[derive(Clone, Copy, Debug)]
pub struct Monogram {
    /// ASCII letter
    pub letter: char,
    /// Descriptive name
    pub name: &'static str,
    /// Stroke sequence through 7-segment field
    pub strokes: &'static [Stroke],
    /// Triadic form representations
    pub triadic: TriadicForm,
}

/// A single stroke in a monogram
#[derive(Clone, Copy, Debug)]
pub struct Stroke {
    /// Which segment to traverse
    pub segment: Segment,
    /// Stroke intensity (0.0-1.0)
    pub intensity: f32,
}

/// Three representations of the same monogram
#[derive(Clone, Copy, Debug)]
pub struct TriadicForm {
    /// Separated: Individual components visible
    pub separated: &'static str,
    /// Kissing: Components connected by bridges
    pub kissing: &'static str,
    /// Overlapped: Single flowing symbol
    pub overlapped: &'static str,
}

impl Monogram {
    /// Get monogram by letter
    pub fn from_char(c: char) -> Option<&'static Self> {
        let upper = c.to_ascii_uppercase();
        if upper >= 'A' && upper <= 'Z' {
            Some(&MONOGRAMS[(upper as u8 - b'A') as usize])
        } else {
            None
        }
    }
    
    /// Get monogram by index (0-25)
    pub fn from_index(idx: usize) -> Option<&'static Self> {
        MONOGRAMS.get(idx)
    }
    
    /// Generate LatticeState sequence for this monogram
    pub fn to_states(&self) -> Vec<LatticeState> {
        self.strokes.iter().map(|stroke| {
            let mut state = LatticeState::at_segment(stroke.segment);
            // Scale fellowship resonance by intensity
            state.fellowship_resonance *= stroke.intensity;
            state
        }).collect()
    }
    
    /// Get display form based on triadic state
    pub fn display(&self, state: TriadicState) -> &'static str {
        match state {
            TriadicState::Separated => self.triadic.separated,
            TriadicState::Kissing => self.triadic.kissing,
            TriadicState::Overlapped => self.triadic.overlapped,
        }
    }
    
    /// Calculate stroke complexity (number of segments)
    pub fn complexity(&self) -> usize {
        self.strokes.len()
    }
    
    /// Get total traversal intensity
    pub fn total_intensity(&self) -> f32 {
        self.strokes.iter().map(|s| s.intensity).sum()
    }
}

/// Triadic reading states
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum TriadicState {
    /// Separated: Individual components visible (learning)
    Separated,
    /// Kissing: Components connected (transitional)
    Kissing,
    /// Overlapped: Unified symbol (fluency)
    Overlapped,
}

impl TriadicState {
    /// Advance to next state (Separated → Kissing → Overlapped → Separated)
    pub fn advance(self) -> Self {
        match self {
            Self::Separated => Self::Kissing,
            Self::Kissing => Self::Overlapped,
            Self::Overlapped => Self::Separated,
        }
    }
    
    /// Get symbol representation
    pub fn symbol(&self) -> &'static str {
        match self {
            Self::Separated => "●",
            Self::Kissing => "●●",
            Self::Overlapped => "◉",
        }
    }
    
    /// Get description
    pub fn description(&self) -> &'static str {
        match self {
            Self::Separated => "Individuality / Learning",
            Self::Kissing => "Relationship / Transitional",
            Self::Overlapped => "Unity / Fluency",
        }
    }
}

/// Generate all 26 monograms as LatticeState sequences
pub fn generate_all_monograms() -> Vec<(char, Vec<LatticeState>)> {
    MONOGRAMS.iter()
        .map(|m| (m.letter, m.to_states()))
        .collect()
}

/// Get complexity distribution across all monograms
pub fn complexity_distribution() -> [usize; 6] {
    let mut counts = [0usize; 6];
    for m in MONOGRAMS.iter() {
        let c = m.complexity().min(5);
        counts[c] += 1;
    }
    counts
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_all_monograms_defined() {
        assert_eq!(MONOGRAMS.len(), 26);
        for (i, m) in MONOGRAMS.iter().enumerate() {
            assert_eq!(m.letter, (b'A' + i as u8) as char);
        }
    }
    
    #[test]
    fn test_monogram_lookup() {
        assert!(Monogram::from_char('A').is_some());
        assert!(Monogram::from_char('Z').is_some());
        assert!(Monogram::from_char('a').is_some());
        assert!(Monogram::from_char('@').is_none());
    }
    
    #[test]
    fn test_state_generation() {
        let m = Monogram::from_char('A').unwrap();
        let states = m.to_states();
        assert!(!states.is_empty());
    }
    
    #[test]
    fn test_triadic_states() {
        let mut state = TriadicState::Separated;
        state = state.advance();
        assert_eq!(state, TriadicState::Kissing);
        state = state.advance();
        assert_eq!(state, TriadicState::Overlapped);
        state = state.advance();
        assert_eq!(state, TriadicState::Separated);
    }
    
    #[test]
    fn test_complexity_distribution() {
        let dist = complexity_distribution();
        let total: usize = dist.iter().sum();
        assert_eq!(total, 26);
    }
}
