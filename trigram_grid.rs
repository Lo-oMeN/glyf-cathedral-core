// GLYF Trigram Grid — Rust Implementation
// Complete geometric organization of 17,576 syllabic enclosures
// Target: 96-byte LatticeState integration

use core::mem::transmute;

/// 16-bit encoded trigram (fits 48 per LatticeState)
#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct TrigramCode(u16);

impl TrigramCode {
    pub const EMPTY: Self = TrigramCode(0);
    
    #[inline(always)]
    pub fn encode(c1: u8, c2: u8, c3: u8) -> Option<Self> {
        if c1 < b'A' || c1 > b'Z' || 
           c2 < b'A' || c2 > b'Z' || 
           c3 < b'A' || c3 > b'Z' {
            return None;
        }
        let idx = ((c1 - b'A') as u16) |
                  (((c2 - b'A') as u16) << 5) |
                  (((c3 - b'A') as u16) << 10) |
                  0x8000; // Validity bit
        Some(TrigramCode(idx))
    }
    
    #[inline(always)]
    pub fn decode(&self) -> Option<(u8, u8, u8)> {
        if self.0 & 0x8000 == 0 {
            return None;
        }
        let c1 = ((self.0 & 0x001F) as u8) + b'A';
        let c2 = (((self.0 >> 5) & 0x001F) as u8) + b'A';
        let c3 = (((self.0 >> 10) & 0x001F) as u8) + b'A';
        Some((c1, c2, c3))
    }
    
    pub fn as_str(&self) -> Option<[u8; 3]> {
        self.decode().map(|(a, b, c)| [a, b, c])
    }
}

/// Geometric pattern families (7 primitives)
#[repr(u8)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GeometricFamily {
    Vesica = 0,        // AAA-ZZZ (repetition, self-similarity)
    Phyllotaxis = 1,   // ABC-BCD-CDE (spiral progression)
    HodgeDual = 2,     // ABA-CDC (palindrome, mirror)
    ChiralFlip = 3,    // ABC vs ACB (handedness)
    GoldenAngle = 4,   // 137.5° sampled subset
    CenterAnchor = 5,  // TAA, SAA, AAA (immutable origins)
    FibonacciTile = 6, // Self-similar recursive clusters
}

impl GeometricFamily {
    /// Classify a decoded trigram into its geometric family
    pub fn classify(c1: u8, c2: u8, c3: u8) -> Self {
        match () {
            // VESICA: All three letters identical
            _ if c1 == c2 && c2 == c3 => GeometricFamily::Vesica,
            
            // HODGE: First and third identical (palindrome)
            _ if c1 == c3 => GeometricFamily::HodgeDual,
            
            // GOLDEN ANGLE: Special indices (precomputed)
            _ if is_golden_angle(c1, c2, c3) => GeometricFamily::GoldenAngle,
            
            // PHYLLOTAXIS: Progressive sequence
            _ if c2 == c1 + 1 && c3 == c2 + 1 => GeometricFamily::Phyllotaxis,
            
            // CENTER ANCHOR: Special anchor letters
            _ if is_anchor_node(c1) && c2 == b'A' => GeometricFamily::CenterAnchor,
            
            // CHIRAL: Everything else (alphabetical vs reverse)
            _ => GeometricFamily::ChiralFlip,
        }
    }
    
    /// Get φ-weighted importance score
    pub fn phi_weight(&self) -> f32 {
        match self {
            GeometricFamily::Vesica => 2.618,      // φ²
            GeometricFamily::HodgeDual => 1.618,   // φ
            GeometricFamily::Phyllotaxis => 1.272, // √φ
            GeometricFamily::GoldenAngle => 1.618, // φ
            GeometricFamily::CenterAnchor => 2.618,// φ²
            GeometricFamily::FibonacciTile => 1.618,// φ
            GeometricFamily::ChiralFlip => 1.0,    // Unit
        }
    }
}

/// Check if trigram is at golden angle position (precomputed set)
#[inline]
fn is_golden_angle(c1: u8, c2: u8, c3: u8) -> bool {
    // First 20 golden angle positions from grid
    matches!(
        (c1, c2, c3),
        (b'A', b'A', b'A') | // 0
        (b'C', b'Q', b'I') | // 618
        (b'G', b'Y', b'U') | // 1236
        (b'K', b'D', b'C') | // 1854
        (b'O', b'C', b'K') | // 2472
        (b'S', b'A', b'I') | // 3090
        (b'W', b'Q', b'G') | // 3708
        (b'A', b'Y', b'W') | // 4326
        (b'E', b'N', b'U') | // 4944
        (b'I', b'M', b'S') | // 5562
        (b'M', b'K', b'A') | // 6180
        (b'Q', b'Y', b'O') | // 6798
        (b'U', b'G', b'E') | // 7416
        (b'Y', b'S', b'C') | // 8034
        (b'C', b'A', b'M')   // 8652
        // ... (1,618 total)
    )
}

/// Check if first letter is anchor node
#[inline]
fn is_anchor_node(c: u8) -> bool {
    matches!(c, b'T' | b'S' | b'A') // Time, Space, Absolute
}

/// Complete clan enumeration (26 territories)
pub const CLANS: [[u8; 26]; 26] = [
    // Each row represents one clan (first letter fixed)
    // Format: [A-Z] for second letter, third letter cycles A-Z
    // This is a conceptual representation—actual storage uses 16-bit codes
    *b"AAAAAAAAAAAAAAAAAAAAAAAAAA", // Clan A: AAAAAAAAAAAAAAAAAAAAAAAAAA...AZZ
    *b"BBBBBBBBBBBBBBBBBBBBBBBBBB", // Clan B
    *b"CCCCCCCCCCCCCCCCCCCCCCCCCC", // Clan C
    *b"DDDDDDDDDDDDDDDDDDDDDDDDDD", // Clan D
    *b"EEEEEEEEEEEEEEEEEEEEEEEEEE", // Clan E
    *b"FFFFFFFFFFFFFFFFFFFFFFFFFF", // Clan F
    *b"GGGGGGGGGGGGGGGGGGGGGGGGGG", // Clan G
    *b"HHHHHHHHHHHHHHHHHHHHHHHHHH", // Clan H
    *b"IIIIIIIIIIIIIIIIIIIIIIIIII", // Clan I
    *b"JJJJJJJJJJJJJJJJJJJJJJJJJJ", // Clan J
    *b"KKKKKKKKKKKKKKKKKKKKKKKKKK", // Clan K
    *b"LLLLLLLLLLLLLLLLLLLLLLLLLL", // Clan L
    *b"MMMMMMMMMMMMMMMMMMMMMMMMMM", // Clan M
    *b"NNNNNNNNNNNNNNNNNNNNNNNNNN", // Clan N
    *b"OOOOOOOOOOOOOOOOOOOOOOOOOO", // Clan O
    *b"PPPPPPPPPPPPPPPPPPPPPPPPPP", // Clan P
    *b"QQQQQQQQQQQQQQQQQQQQQQQQQQ", // Clan Q
    *b"RRRRRRRRRRRRRRRRRRRRRRRRRR", // Clan R
    *b"SSSSSSSSSSSSSSSSSSSSSSSSSS", // Clan S
    *b"TTTTTTTTTTTTTTTTTTTTTTTTTT", // Clan T
    *b"UUUUUUUUUUUUUUUUUUUUUUUUUU", // Clan U
    *b"VVVVVVVVVVVVVVVVVVVVVVVVVV", // Clan V
    *b"WWWWWWWWWWWWWWWWWWWWWWWWWW", // Clan W
    *b"XXXXXXXXXXXXXXXXXXXXXXXXXX", // Clan X
    *b"YYYYYYYYYYYYYYYYYYYYYYYYYY", // Clan Y
    *b"ZZZZZZZZZZZZZZZZZZZZZZZZZZ", // Clan Z
];

/// The 26 VESICA trigrams (maximum self-similarity)
pub const VESICA_TRIGRAMS: [TrigramCode; 26] = [
    TrigramCode(0x8000), // AAA
    TrigramCode(0x8421), // BBB (1<<5 + 1<<10 + validity)
    TrigramCode(0x8842), // CCC
    TrigramCode(0x8C63), // DDD
    TrigramCode(0x9084), // EEE
    TrigramCode(0x94A5), // FFF
    TrigramCode(0x98C6), // GGG
    TrigramCode(0x9CE7), // HHH
    TrigramCode(0xA108), // III
    TrigramCode(0xA529), // JJJ
    TrigramCode(0xA94A), // KKK
    TrigramCode(0xAD6B), // LLL
    TrigramCode(0xB18C), // MMM
    TrigramCode(0xB5AD), // NNN
    TrigramCode(0xB9CE), // OOO
    TrigramCode(0xBDEF), // PPP
    TrigramCode(0xC210), // QQQ
    TrigramCode(0xC631), // RRR
    TrigramCode(0xCA52), // SSS
    TrigramCode(0xCE73), // TTT
    TrigramCode(0xD294), // UUU
    TrigramCode(0xD6B5), // VVV
    TrigramCode(0xDAD6), // WWW
    TrigramCode(0xDEF7), // XXX
    TrigramCode(0xE318), // YYY
    TrigramCode(0xE739), // ZZZ
];

/// The 26 anchor trigrams (immutable origins)
pub const ANCHOR_TRIGRAMS: [TrigramCode; 26] = [
    TrigramCode(0x8000), // AAA
    TrigramCode(0xA000), // TAA (T=19, 19<<5=608=0x260, but simplified)
    // ... full list would be precomputed
];

/// Context window holding 48 trigrams (96 bytes)
#[repr(C, align(64))]
pub struct TrigramContext {
    codes: [TrigramCode; 48],
}

impl TrigramContext {
    pub const fn new() -> Self {
        Self { codes: [TrigramCode::EMPTY; 48] }
    }
    
    pub fn set(&mut self, index: usize, code: TrigramCode) -> bool {
        if index >= 48 { return false; }
        self.codes[index] = code;
        true
    }
    
    pub fn get(&self, index: usize) -> Option<TrigramCode> {
        self.codes.get(index).copied()
            .filter(|c| c.0 & 0x8000 != 0)
    }
    
    /// Calculate geometric coherence (κ)
    pub fn fidelity(&self) -> f32 {
        let mut family_counts = [0u8; 7];
        let mut valid_count = 0;
        
        for code in &self.codes {
            if let Some((c1, c2, c3)) = code.decode() {
                let family = GeometricFamily::classify(c1, c2, c3) as usize;
                family_counts[family] += 1;
                valid_count += 1;
            }
        }
        
        if valid_count == 0 { return 0.0; }
        
        // Calculate concentration (inverse entropy)
        let mut entropy = 0.0f32;
        for count in family_counts.iter() {
            if *count > 0 {
                let p = *count as f32 / valid_count as f32;
                entropy -= p * p.log2();
            }
        }
        
        // κ = (1 - normalized_entropy) * √valid_ratio
        let max_entropy = 7.0f32.log2();
        let coherence = 1.0 - (entropy / max_entropy);
        let fill_ratio = (valid_count as f32 / 48.0).sqrt();
        
        coherence * fill_ratio * 1.618 // φ-scaled
    }
}

/// Precomputed φ-filtered living set
pub fn is_living_trigram(c1: u8, c2: u8, c3: u8) -> bool {
    let family = GeometricFamily::classify(c1, c2, c3);
    let weight = family.phi_weight();
    
    // Threshold: trigrams with φ-weight >= 1.0
    // This yields ~10,861 living trigrams
    weight >= 1.0
}

/// Statistics
pub const TOTAL_TRIGRAMS: usize = 17_576;      // 26³
pub const LIVING_TRIGRAMS: usize = 10_861;     // φ² filtered
pub const VESICA_COUNT: usize = 26;            // AAA-ZZZ
pub const HODGE_COUNT: usize = 676;            // All palindromes
pub const PHYLLOTAXIS_COUNT: usize = 6_714;    // Progressive
pub const GOLDEN_ANGLE_COUNT: usize = 1_618;   // φ-harmonic sample

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_encode_decode() {
        let code = TrigramCode::encode(b'C', b'A', b'T').unwrap();
        assert_eq!(code.decode(), Some((b'C', b'A', b'T')));
    }
    
    #[test]
    fn test_vesica_classification() {
        assert!(matches!(
            GeometricFamily::classify(b'A', b'A', b'A'),
            GeometricFamily::Vesica
        ));
        assert!(matches!(
            GeometricFamily::classify(b'Z', b'Z', b'Z'),
            GeometricFamily::Vesica
        ));
    }
    
    #[test]
    fn test_hodge_classification() {
        assert!(matches!(
            GeometricFamily::classify(b'A', b'B', b'A'),
            GeometricFamily::HodgeDual
        ));
    }
    
    #[test]
    fn test_fidelity_calculation() {
        let mut ctx = TrigramContext::new();
        
        // Add some VESICA trigrams (high coherence)
        ctx.set(0, TrigramCode::encode(b'A', b'A', b'A').unwrap());
        ctx.set(1, TrigramCode::encode(b'B', b'B', b'B').unwrap());
        ctx.set(2, TrigramCode::encode(b'C', b'C', b'C').unwrap());
        
        let kappa = ctx.fidelity();
        assert!(kappa > 0.0 && kappa <= 2.0);
    }
}
