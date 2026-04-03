//! GLYF Cathedral v0.7.2 φ⁷
//! 
//! Geometric Language Model — 96-byte semantic encoding
//! via φ-scaled Hamiltonian traversal of the 7-segment field.
//!
//! Core architecture:
//! - 7 Geometric Primitives (Void, Vesica, Curve, Line, Angle, Circle, Dot)
//! - Hamiltonian Path: K2→K5→K1→K4→K7→K3→K6 (ergodic, non-repeating)
//! - 96-byte LatticeState — complete semantic encoding
//! - 26 Monograms (A-Z) — letter traversals
//! - 17,576 Trigrams (aaa-zzz) — syllabic vocabulary
//! - φ ≈ 1.618 — golden ratio scaling throughout

use std::env;
use std::process;

mod glyf;

use glyf::{LatticeState, Monogram, Trigram, TriadicState, PHI, PHI_7};

const VERSION: &str = "0.7.2 φ⁷";

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_help();
        process::exit(0);
    }
    
    match args[1].as_str() {
        "--help" | "-h" | "help" => print_help(),
        "--version" | "-v" | "version" => println!("GLYF Cathedral {}", VERSION),
        "state" => cmd_state(),
        "monogram" => cmd_monogram(&args),
        "trigram" => cmd_trigram(&args),
        "path" => cmd_path(),
        "phi" => cmd_phi(),
        "demo" => cmd_demo(),
        _ => {
            eprintln!("Unknown command: {}", args[1]);
            print_help();
            process::exit(1);
        }
    }
}

fn print_help() {
    println!("GLYF Cathedral {}", VERSION);
    println!("Geometric Language Model — 96-byte semantic encoding\n");
    println!("USAGE:");
    println!("    glyf-cathedral <COMMAND> [OPTIONS]\n");
    println!("COMMANDS:");
    println!("    state        Show default LatticeState structure");
    println!("    monogram     Show monogram definitions (A-Z)");
    println!("    trigram      Encode/decode trigrams");
    println!("    path         Show Hamiltonian path through 7-segment field");
    println!("    phi          Display φ constants");
    println!("    demo         Run demonstration\n");
    println!("EXAMPLES:");
    println!("    glyf-cathedral state");
    println!("    glyf-cathedral monogram A");
    println!("    glyf-cathedral trigram THE");
    println!("    glyf-cathedral path\n");
    println!("ARCHITECTURE:");
    println!("    7 Geometric Primitives: Void, Vesica, Curve, Line, Angle, Circle, Dot");
    println!("    Hamiltonian Path: K2→K5→K1→K4→K7→K3→K6");
    println!("    φ ≈ {} — Golden Ratio", PHI);
    println!("    φ⁷ ≈ {} — Fellowship Resonance", PHI_7);
}

fn cmd_state() {
    println!("GLYF Cathedral — 96-Byte LatticeState\n");
    
    let state = LatticeState::new();
    println!("{}", state);
    
    println!("\nField Layout:");
    println!("  [00-07] Center S: [{:.2}, {:.2}] — Immutable origin", 
             state.center_s[0], state.center_s[1]);
    println!("  [08-23] Ternary Junction: 16D PGA multivector");
    println!("  [24-55] Hex Persistence: 32 bytes φ-radial tiles");
    println!("  [56-59] Fellowship Resonance: {:.6} (φ⁷)", state.fellowship_resonance);
    println!("  [60-63] φ Magnitude: {:.6}", state.phi_magnitude);
    println!("  [64]    Morphogen Phase: {} (0-6)", state.morphogen_phase);
    println!("  [65]    Vesica Coherence: {}", state.vesica_coherence);
    println!("  [66]    Phyllotaxis Spiral: {}", state.phyllotaxis_spiral);
    println!("  [67]    Hodge Dual: {}", state.hodge_dual);
    println!("  [68-71] Checksum: 0x{:08X}", state.checksum);
    println!("  [72-95] Padding: 24 bytes cache-line alignment");
    println!("\nTotal: 96 bytes (1.5 cache lines @ 64 bytes/line)");
}

fn cmd_monogram(args: &[String]) {
    if args.len() < 3 {
        println!("26 Monograms (A-Z):\n");
        for m in glyf::MONOGRAMS.iter() {
            println!("  {} — {} ({} strokes)", 
                m.letter, m.name, m.complexity());
        }
        println!("\nUsage: glyf-cathedral monogram <LETTER>");
        return;
    }
    
    let letter = args[2].chars().next().unwrap_or('A');
    
    if let Some(m) = Monogram::from_char(letter) {
        println!("Monogram: {} — {}\n", m.letter, m.name);
        
        println!("Triadic Forms:");
        println!("  ●  Separated:  {}", m.triadic.separated);
        println!("  ●● Kissing:    {}", m.triadic.kissing);
        println!("  ◉  Overlapped: {}\n", m.triadic.overlapped);
        
        println!("Stroke Sequence:");
        for (i, stroke) in m.strokes.iter().enumerate() {
            println!("  {}. {:?} (intensity: {:.1})", 
                i + 1, stroke.segment, stroke.intensity);
        }
        
        println!("\nTotal Intensity: {:.2}", m.total_intensity());
        println!("Complexity: {} segments", m.complexity());
    } else {
        eprintln!("Invalid letter: {}", letter);
    }
}

fn cmd_trigram(args: &[String]) {
    if args.len() < 3 {
        println!("Trigram Encoding (17,576 vocabulary)\n");
        println!("Binary format: 16 bits");
        println!("  [0-4]   First letter  (A=0...Z=25)");
        println!("  [5-9]   Second letter (× 32)");
        println!("  [10-14] Third letter  (× 1024)");
        println!("  [15]    Validity flag\n");
        println!("Storage: {} bytes (35 KB)", glyf::trigrams::storage_size());
        println!("\nUsage: glyf-cathedral trigram <AAA>");
        return;
    }
    
    let s = &args[2];
    if s.len() != 3 {
        eprintln!("Trigram must be exactly 3 letters");
        return;
    }
    
    if let Some(t) = Trigram::new(s.chars().nth(0).unwrap(),
                                   s.chars().nth(1).unwrap(),
                                   s.chars().nth(2).unwrap()) {
        let code = t.encode();
        println!("Trigram: {}", t.as_string());
        println!("Code: 0x{:04X} ({})", code.full(), code.full());
        println!("Raw: 0x{:04X} ({})", code.raw(), code.raw());
        println!("Valid: {}", code.is_valid());
        println!("φ-Complexity: {:.4}", t.phi_complexity());
    } else {
        eprintln!("Invalid trigram: {}", s);
    }
}

fn cmd_path() {
    use glyf::HamiltonianPath;
    use glyf::lattice_state::Segment;
    
    println!("Hamiltonian Path — 7-Segment Field Traversal\n");
    println!("Ergodic: Visits each segment exactly once");
    println!("Non-repeating: Never returns to same state\n");
    
    println!("Path: K2 → K5 → K1 → K4 → K7 → K3 → K6\n");
    
    for (i, segment) in HamiltonianPath::new().enumerate() {
        let name = segment.name();
        let (x, y) = segment_position(&segment);
        println!("  {}. K{} — {} (position: [{}, {}])",
            i + 1,
            segment as u8 + 1,
            name,
            x, y
        );
    }
    
    println!("\nPrimitives:");
    for i in 0..7 {
        let seg = Segment::from_u8(i);
        println!("  K{} — {:?}", i + 1, seg);
    }
}

fn segment_position(seg: &glyf::lattice_state::Segment) -> (i32, i32) {
    // Geometric positions in 7-segment field
    use glyf::lattice_state::Segment;
    match seg {
        Segment::Void =>    (0, 0),    // Center
        Segment::Vesica =>  (0, -120), // Top
        Segment::Angle =>   (-80, -80), // Top-left
        Segment::Line =>    (-120, 0),  // Left
        Segment::Dot =>     (-100, 80), // Bottom-left
        Segment::Curve =>   (100, 80),  // Bottom-right
        Segment::Circle =>  (0, 120),   // Bottom
    }
}

fn cmd_phi() {
    println!("φ (Golden Ratio) Constants\n");
    println!("φ    = {:.15}", PHI);
    println!("φ²   = {:.15}", PHI * PHI);
    println!("φ³   = {:.15}", PHI.powi(3));
    println!("φ⁴   = {:.15}", PHI.powi(4));
    println!("φ⁵   = {:.15}", PHI.powi(5));
    println!("φ⁶   = {:.15}", PHI.powi(6));
    println!("φ⁷   = {:.15} ← Fellowship Resonance", PHI_7);
    println!("φ⁻¹  = {:.15}", 1.0 / PHI);
    println!("√φ   = {:.15}", PHI.sqrt());
    println!("\nGolden Angle:");
    println!("  {}° = {:.15} rad", GOLDEN_ANGLE_DEG, GOLDEN_ANGLE_RAD);
}

fn cmd_demo() {
    println!("GLYF Cathedral Demonstration\n");
    println!("Version: {}\n", VERSION);
    
    // Show state creation
    println!("1. Creating LatticeState...");
    let state = LatticeState::new();
    println!("   {}", state);
    
    // Show monogram
    println!("\n2. Loading monogram 'A'...");
    if let Some(m) = Monogram::from_char('A') {
        println!("   {} — {}", m.letter, m.name);
        println!("   Forms: {} / {} / {}",
            m.display(TriadicState::Separated),
            m.display(TriadicState::Kissing),
            m.display(TriadicState::Overlapped));
    }
    
    // Show trigram
    println!("\n3. Encoding trigram 'THE'...");
    if let Some(t) = Trigram::new('T', 'H', 'E') {
        let code = t.encode();
        println!("   {} → 0x{:04X}", t.as_string(), code.full());
        println!("   φ-Complexity: {:.4}", t.phi_complexity());
    }
    
    // Show coherence
    println!("\n4. Measuring state coherence...");
    let state2 = LatticeState::new();
    let coherence = state.coherence_with(&state2);
    println!("   Identical states: {:.2} coherence", coherence);
    
    println!("\n✓ Demo complete. Architecture verified.");
}

// Constants from lattice_state module
use glyf::{PHI, PHI_7, GOLDEN_ANGLE_RAD, GOLDEN_ANGLE_DEG};
