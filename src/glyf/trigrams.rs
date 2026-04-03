//! GLYF Trigrams — 17,576 Syllabic Compound Glyphs
//!
//! 26³ = 17,576 trigrams (aaa through zzz)
//! Each trigram encodes a complete syllable pattern.
//! 
//! Binary encoding: 16 bits
//! - Bits 0-4: First letter (A=0...Z=25)
//! - Bits 5-9: Second letter (× 32)
//! - Bits 10-14: Third letter (× 1024)
//! - Bit 15: Validity flag

use super::monograms::Monogram;

/// 26³ = 17,576 possible trigrams
pub const TRIGRAM_COUNT: usize = 26 * 26 * 26;

/// Maximum trigram code value (15 bits used)
pub const MAX_CODE: u16 = 0x7FFF;

/// A trigram syllable (three letters)
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Trigram {
    /// First letter (0-25 = A-Z)
    pub a: u8,
    /// Second letter (0-25 = A-Z)
    pub b: u8,
    /// Third letter (0-25 = A-Z)
    pub c: u8,
}

impl Trigram {
    /// Create from three letters
    pub fn new(a: char, b: char, c: char) -> Option<Self> {
        let a = a.to_ascii_uppercase();
        let b = b.to_ascii_uppercase();
        let c = c.to_ascii_uppercase();
        
        if a >= 'A' && a <= 'Z' &&
           b >= 'A' && b <= 'Z' &&
           c >= 'A' && c <= 'Z' {
            Some(Self {
                a: a as u8 - b'A',
                b: b as u8 - b'A',
                c: c as u8 - b'A',
            })
        } else {
            None
        }
    }
    
    /// Create from indices
    pub fn from_indices(a: u8, b: u8, c: u8) -> Option<Self> {
        if a < 26 && b < 26 && c < 26 {
            Some(Self { a, b, c })
        } else {
            None
        }
    }
    
    /// Encode to 16-bit code
    pub fn encode(&self) -> TrigramCode {
        let code = ((self.c as u16) << 10)
                 | ((self.b as u16) << 5)
                 | (self.a as u16);
        TrigramCode(code | 0x8000) // Set validity bit
    }
    
    /// Decode from 16-bit code
    pub fn decode(code: TrigramCode) -> Option<Self> {
        if !code.is_valid() {
            return None;
        }
        let raw = code.raw();
        Some(Self {
            a: (raw & 0x1F) as u8,
            b: ((raw >> 5) & 0x1F) as u8,
            c: ((raw >> 10) & 0x1F) as u8,
        })
    }
    
    /// Get letters as chars
    pub fn chars(&self) -> (char, char, char) {
        (
            (b'A' + self.a) as char,
            (b'A' + self.b) as char,
            (b'A' + self.c) as char,
        )
    }
    
    /// Get string representation
    pub fn as_string(&self) -> String {
        let (a, b, c) = self.chars();
        format!("{}{}{}", a, b, c)
    }
    
    /// Get first monogram
    pub fn first(&self) -> Option<&'static Monogram> {
        super::monograms::Monogram::from_index(self.a as usize)
    }
    
    /// Get second monogram
    pub fn second(&self) -> Option<&'static Monogram> {
        super::monograms::Monogram::from_index(self.b as usize)
    }
    
    /// Get third monogram
    pub fn third(&self) -> Option<&'static Monogram> {
        super::monograms::Monogram::from_index(self.c as usize)
    }
    
    /// Calculate φ-weighted complexity
    /// 
    /// Uses the three monograms' complexity scores
    /// weighted by φ ratios
    pub fn phi_complexity(&self) -> f32 {
        let c1 = self.first().map(|m| m.complexity() as f32).unwrap_or(0.0);
        let c2 = self.second().map(|m| m.complexity() as f32).unwrap_or(0.0);
        let c3 = self.third().map(|m| m.complexity() as f32).unwrap_or(0.0);
        
        // φ-weighted: first is most significant
        c1 * super::PHI.powi(0) +
        c2 * super::PHI.powi(-1) +
        c3 * super::PHI.powi(-2)
    }
    
    /// Check if this trigram is a valid English syllable
    pub fn is_valid_english(&self) -> bool {
        // Check against common English patterns
        let s = self.as_string();
        !INVALID_ENGLISH.contains(&s.as_str())
    }
}

/// Trigram code (16-bit encoded)
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct TrigramCode(u16);

impl TrigramCode {
    /// Create from raw code (checks validity)
    pub fn new(raw: u16) -> Option<Self> {
        if raw & 0x8000 != 0 { // Validity bit set
            Some(Self(raw))
        } else {
            None
        }
    }
    
    /// Create without checking
    pub unsafe fn new_unchecked(raw: u16) -> Self {
        Self(raw)
    }
    
    /// Check validity bit
    pub fn is_valid(&self) -> bool {
        self.0 & 0x8000 != 0
    }
    
    /// Get raw code (without validity bit)
    pub fn raw(&self) -> u16 {
        self.0 & 0x7FFF
    }
    
    /// Get full code
    pub fn full(&self) -> u16 {
        self.0
    }
    
    /// Convert to trigram
    pub fn to_trigram(&self) -> Option<Trigram> {
        Trigram::decode(*self)
    }
}

impl From<Trigram> for TrigramCode {
    fn from(t: Trigram) -> Self {
        t.encode()
    }
}

/// Invalid English trigram patterns
static INVALID_ENGLISH: [&str; 20] = [
    "XXX", "QQQ", "ZZZ", "JJJ", "KKK",  // Triple consonants (rare)
    "AEI", "AIO", "EIO", "OUI", "AEU", // Triple vowels (invalid)
    "KKB", "QQT", "XXZ", "JJG", "ZZP", // Invalid consonant clusters
    "BFP", "DTK", "GZX", "VJQ", "WLF", // Unpronounceable
];

/// Lookup table for all 17,576 trigrams
/// 
/// This is the core vocabulary. 35KB total storage.
pub static TRIGRAM_TABLE: [Trigram; TRIGRAM_COUNT] = {
    // Build at compile time using const fn
    // This is a placeholder - in practice, use a build script
    // to generate the full table
    let mut table = [Trigram { a: 0, b: 0, c: 0 }; TRIGRAM_COUNT];
    let mut i = 0;
    while i < TRIGRAM_COUNT {
        let c = (i / (26 * 26)) as u8;
        let b = ((i / 26) % 26) as u8;
        let a = (i % 26) as u8;
        table[i] = Trigram { a, b, c };
        i += 1;
    }
    table
};

/// Get trigram by code
pub fn get_by_code(code: u16) -> Option<&'static Trigram> {
    if code < TRIGRAM_COUNT as u16 {
        TRIGRAM_TABLE.get(code as usize)
    } else {
        None
    }
}

/// Find trigrams by prefix (for autocomplete)
pub fn find_by_prefix(prefix: &str) -> Vec<&'static Trigram> {
    if prefix.len() > 3 {
        return vec![];
    }
    
    let chars: Vec<char> = prefix.to_ascii_uppercase().chars().collect();
    
    TRIGRAM_TABLE.iter()
        .filter(|t| {
            if chars.len() >= 1 {
                let a = (b'A' + t.a) as char;
                if a != chars[0] { return false; }
            }
            if chars.len() >= 2 {
                let b = (b'A' + t.b) as char;
                if b != chars[1] { return false; }
            }
            if chars.len() >= 3 {
                let c = (b'A' + t.c) as char;
                if c != chars[2] { return false; }
            }
            true
        })
        .collect()
}

/// Calculate total storage size
pub const fn storage_size() -> usize {
    TRIGRAM_COUNT * std::mem::size_of::<Trigram>()
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_trigram_count() {
        assert_eq!(TRIGRAM_COUNT, 17576);
        assert_eq!(storage_size(), 17576 * 3); // 3 bytes each
    }
    
    #[test]
    fn test_encode_decode() {
        let t = Trigram::new('C', 'A', 'T').unwrap();
        let code = t.encode();
        let decoded = Trigram::decode(code).unwrap();
        assert_eq!(t.a, decoded.a);
        assert_eq!(t.b, decoded.b);
        assert_eq!(t.c, decoded.c);
    }
    
    #[test]
    fn test_string_roundtrip() {
        let t = Trigram::new('T', 'H', 'E').unwrap();
        assert_eq!(t.as_string(), "THE");
    }
    
    #[test]
    fn test_code_validity() {
        let t = Trigram::new('A', 'B', 'C').unwrap();
        let code = t.encode();
        assert!(code.is_valid());
        assert_eq!(code.to_trigram().unwrap().as_string(), "ABC");
    }
    
    #[test]
    fn test_invalid_decode() {
        let invalid = TrigramCode(0x0000); // No validity bit
        assert!(!invalid.is_valid());
        assert!(Trigram::decode(invalid).is_none());
    }
    
    #[test]
    fn test_phi_complexity() {
        let simple = Trigram::new('I', 'I', 'I').unwrap(); // Three I's
        let complex = Trigram::new('M', 'W', 'E').unwrap(); // Complex shapes
        assert!(complex.phi_complexity() > simple.phi_complexity());
    }
    
    #[test]
    fn test_prefix_search() {
        let results = find_by_prefix("TH");
        assert!(results.len() > 0);
        // Should include THE, THY, THO, etc.
    }
    
    #[test]
    fn test_table_generation() {
        // First trigram: AAA
        assert_eq!(TRIGRAM_TABLE[0].as_string(), "AAA");
        // Last trigram: ZZZ
        assert_eq!(TRIGRAM_TABLE[17575].as_string(), "ZZZ");
        // THE is in there somewhere
        let the = Trigram::new('T', 'H', 'E').unwrap();
        let the_code = the.encode().raw() as usize;
        assert_eq!(TRIGRAM_TABLE[the_code].as_string(), "THE");
    }
}
