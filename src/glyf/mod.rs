//! GLYF Module — Geometric Linguistic Foundation
//!
//! Core components:
//! - lattice_state: 96-byte semantic encoding
//! - monograms: 26 letter definitions
//! - trigrams: 17,576 syllabic compound glyphs

pub mod lattice_state;
pub mod monograms;
pub mod trigrams;

pub use lattice_state::{LatticeState, Segment, HamiltonianPath, PHI, PHI_7, GOLDEN_ANGLE_RAD};
pub use monograms::{Monogram, MONOGRAMS, TriadicState, TriadicForm};
pub use trigrams::{Trigram, TRIGRAM_TABLE, TrigramCode};
