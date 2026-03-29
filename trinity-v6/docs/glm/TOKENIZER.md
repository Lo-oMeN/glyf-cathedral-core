# GLM Tokenizer Specification
## Quadraline-to-Glyph Mapping v0.1.0

**Date:** 2026-03-29  
**Status:** Draft — Core Decomposition Pipeline  
**Reference:** glyf/core/quadraline.rs patterns

---

## 1. Core Principle

Traditional tokenizers map:
```
Text → Subword tokens (50k vocab) → Embedding vectors (768 dims)
```

GLM tokenizer maps:
```
Text → 7-Primitive Glyphs → Geometric vectors (16D PGA)
```

No learned embeddings. No vocabulary. Just geometry.

---

## 2. The 7-Primitive Decomposition

Every semantic unit reduces to combinations of:

| Primitive | Symbol | Meaning | Attention Use |
|-----------|--------|---------|---------------|
| Void | ∅ | Null, absence, potential | Hodge dual base |
| Dot | · | Singularity, instantiation | Center anchor |
| Curve | ~ | Flow, continuity | Phyllotaxis path |
| Line | — | Connection, causality | Direct attention |
| Angle | ∧ | Change, inflection | Direction shift |
| Circle | ○ | Cycle, closure | Complete attention |
| Vesica | ⧖ | Overlap, intersection | Similarity detection |

---

## 3. Decomposition Algorithm

### Step 1: Morphological Analysis
```rust
pub fn decompose_word(word: &str) -> Vec<Glyph> {
    match word {
        // Core concepts
        "love" | "heart" | "connect" => vec![
            Glyph::Vesica { strength: 0.9 },    // Union
            Glyph::Curve { direction: Flow },   // Flow
            Glyph::Dot { position: Center },    // Singular focus
        ],
        
        "time" | "sequence" | "then" => vec![
            Glyph::Line { orientation: Forward },
            Glyph::Angle { turn: Right },
            Glyph::Spiral { growth: Phyllotaxis },
        ],
        
        "no" | "not" | "absence" => vec![
            Glyph::Void,
            Glyph::HodgeStar { target: All },
        ],
        
        "begin" | "start" | "seed" => vec![
            Glyph::Dot { position: Origin },
            Glyph::Spiral { phase: 0 },
        ],
        
        "end" | "finish" | "complete" => vec![
            Glyph::Circle,
            Glyph::CenterAnchor,
        ],
        
        // Default: analyze phonemes
        _ => phonetic_decomposition(word),
    }
}
```

### Step 2: Phonetic-to-Geometric Mapping
```rust
pub fn phonetic_decomposition(word: &str) -> Vec<Glyph> {
    word.chars().map(|c| {
        match c.to_lowercase().next().unwrap() {
            // Vowels = curves (flow)
            'a' | 'e' | 'i' | 'o' | 'u' => Glyph::Curve { 
                direction: vowel_direction(c) 
            },
            
            // Hard consonants = angles (abrupt change)
            'k' | 't' | 'p' | 'd' | 'b' | 'g' => Glyph::Angle { 
                turn: ConsonantHard 
            },
            
            // Soft consonants = lines (smooth connection)
            'l' | 'm' | 'n' | 'r' | 's' | 'f' => Glyph::Line { 
                orientation: ConsonantSoft 
            },
            
            // Sibilants = spirals (hissing continuity)
            'h' | 'z' | 'x' => Glyph::Spiral { 
                phase: Sibilance 
            },
            
            _ => Glyph::Dot { position: Transient },
        }
    }).collect()
}
```

### Step 3: Syntactic Structure Mapping
```rust
pub fn decompose_sentence(sentence: &str) -> GlyphSequence {
    let tokens = tokenize(sentence);
    let mut sequence = GlyphSequence::new();
    
    for (i, token) in tokens.iter().enumerate() {
        let mut glyphs = decompose_word(token.word);
        
        // Apply syntactic transforms
        match token.role {
            Role::Subject => {
                // Subjects get CenterAnchor
                glyphs.push(Glyph::CenterAnchor);
            }
            Role::Verb => {
                // Verbs get Vesica (action = intersection)
                glyphs.insert(0, Glyph::Vesica { 
                    strength: 0.7 
                });
            }
            Role::Object => {
                // Objects get Circle (completion)
                glyphs.push(Glyph::Circle);
            }
            Role::Modifier => {
                // Modifiers get Angle (change direction)
                glyphs.insert(0, Glyph::Angle { 
                    turn: Modifier 
                });
            }
        }
        
        sequence.add(token.position, glyphs);
    }
    
    sequence
}
```

---

## 4. Geometric Embedding

Each glyph maps to a 16D PGA multivector:

```rust
pub fn glyph_to_multivector(glyph: &Glyph) -> [i8; 16] {
    match glyph {
        Glyph::Void => [0; 16],
        
        Glyph::Dot { position } => {
            let mut m = [0i8; 16];
            m[0] = 127; // Scalar = presence
            m[1] = match position {
                Center => 127,
                Origin => 64,
                Transient => 32,
            };
            m
        }
        
        Glyph::Line { orientation } => {
            let mut m = [0i8; 16];
            // e1 coefficient for x-direction
            m[1] = match orientation {
                Forward => 127,
                Backward => -127,
                Bidirectional => 0, // Both e1 and e2
            };
            m
        }
        
        Glyph::Curve { direction } => {
            let mut m = [0i8; 16];
            // e12 bivector for rotation
            let angle = match direction {
                Flow => 45,
                Eddy => -45,
                Cascade => 90,
            };
            m[4] = (angle as f32 * 127.0 / 180.0) as i8;
            m
        }
        
        Glyph::Angle { turn } => {
            let mut m = [0i8; 16];
            // Angle = change in direction
            m[4] = match turn {
                Right => 90,
                Left => -90,
                Sharp => 127,
                Gentle => 32,
                ConsonantHard => 60,
                Modifier => 45,
            };
            m
        }
        
        Glyph::Circle => {
            let mut m = [0i8; 16];
            // Circle = e12 + e23 + e31 (closed loop)
            m[4] = 64;  // e12
            m[5] = 64;  // e13
            m[6] = 64;  // e23
            m
        }
        
        Glyph::Vesica { strength } => {
            let mut m = [0i8; 16];
            // Vesica = two overlapping circles
            let s = (strength * 127.0) as i8;
            m[0] = s;      // Presence
            m[4] = s / 2;  // Overlap curvature
            m[8] = s / 2;  // Intersection volume
            m
        }
        
        Glyph::Spiral { phase, growth } => {
            let mut m = [0i8; 16];
            // Spiral = rotation + dilation
            let p = phase.unwrap_or(0) as i8;
            m[4] = p;  // Rotation
            m[0] = match growth {
                Phyllotaxis => 82,  // φ-related
                Archimedes => 64,
                Logarithmic => 100,
            };
            m
        }
        
        Glyph::HodgeStar { target } => {
            let mut m = [0i8; 16];
            // Hodge dual = complement
            m[15] = 127;  // Pseudoscalar activation
            m
        }
        
        Glyph::CenterAnchor => {
            let mut m = [0i8; 16];
            m[0] = 127;  // Scalar = fundamental
            m[1] = 127;  // e1 = x-axis anchor
            m[2] = 127;  // e2 = y-axis anchor
            m
        }
    }
}
```

---

## 5. Compression Ratio

**Example:** "The quick brown fox"

| Stage | Representation | Size |
|-------|---------------|------|
| Raw text | 19 characters | 152 bits |
| Standard tokens | 5 tokens × 2 bytes | 80 bits |
| Standard embeddings | 5 × 768 dims × 32 bits | 122,880 bits |
| **Glyph decomposition** | 23 glyphs × 16 dims × 8 bits | 2,944 bits |
| **GLM context** | 1 LatticeState | **768 bits** |

**Compression:** 160× vs standard embeddings  
**Semantic density:** Higher (glyphs are meaning, not statistics)

---

## 6. Decompression Pipeline

```rust
pub fn multivector_to_glyph(m: [i8; 16]) -> Glyph {
    // Detect dominant component
    let max_idx = m.iter()
        .enumerate()
        .max_by_key(|(_, v)| v.abs())
        .map(|(i, _)| i)
        .unwrap_or(0);
    
    match max_idx {
        0 if m[4] == 0 && m[5] == 0 => Glyph::Dot { 
            position: if m[0] > 100 { Center } else { Transient } 
        },
        
        1 | 2 | 3 => Glyph::Line { 
            orientation: if m[1] > 0 { Forward } else { Backward } 
        },
        
        4 | 5 | 6 if m[0] == 0 => Glyph::Curve { 
            direction: if m[4] > 0 { Flow } else { Eddy } 
        },
        
        4 | 5 | 6 if m[0] != 0 => Glyph::Circle,
        
        8 => Glyph::Vesica { 
            strength: m[0] as f32 / 127.0 
        },
        
        15 => Glyph::HodgeStar { target: All },
        
        _ => Glyph::Void,
    }
}

pub fn glyphs_to_text(glyphs: &[Glyph]) -> String {
    glyphs.iter()
        .map(|g| glyph_description(g))
        .collect::<Vec<_>>()
        .join(" → ")
}
```

**Note:** Exact reconstruction of original text is not guaranteed.  
**Semantic reconstruction** (meaning, not wording) is the goal.

---

## 7. Examples

### Example 1: "Love"
```rust
Input: "love"
Decomposition: [
    Vesica(0.9),    // Union/connection
    Curve(Flow),    // Emotional flow
    Dot(Center),    // Singular focus
    CenterAnchor,   // Immutable core
]
Embedding: [[0, 0, 0, 0, 0, 0, 0, 114, 57, 0, ...], ...]
Context: 96-byte LatticeState
```

### Example 2: "Time flows"
```rust
Input: "time flows"
Decomposition: [
    Line(Forward),      // Direction
    Angle(Right),       // Change
    Spiral(Phyllotaxis), // Growth
    Curve(Flow),        // Continuity
]
Context: Sequential → temporal attention mode
```

### Example 3: "Not true"
```rust
Input: "not true"
Decomposition: [
    Void,               // Absence
    HodgeStar(All),     // Complement
    Line(Forward),      // Truth direction
    CenterAnchor,       // Core reality
]
Context: Hodge attention → negate direction
```

---

## 8. Implementation

```rust
// trinity-v6/src/glm/tokenizer.rs

pub struct GlyphTokenizer;

impl GlyphTokenizer {
    pub fn encode(text: &str) -> GlyphSequence {
        decompose_sentence(text)
    }
    
    pub fn decode(sequence: &GlyphSequence) -> String {
        glyphs_to_text(&sequence.glyphs)
    }
    
    pub fn to_context(sequence: &GlyphSequence) -> GLMContext {
        sequence.to_lattice_state()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_love_decomposition() {
        let glyphs = decompose_word("love");
        assert!(glyphs.contains(&Glyph::Vesica { strength: 0.9 }));
    }
    
    #[test]
    fn test_roundtrip_approximate() {
        let original = "time flows forward";
        let glyphs = GlyphTokenizer::encode(original);
        let reconstructed = GlyphTokenizer::decode(&glyphs);
        
        // Semantic, not lexical match
        assert!(reconstructed.contains("flow"));
        assert!(reconstructed.contains("forward"));
    }
}
```

---

## 9. Next Steps

1. [ ] Implement glyph decomposition rules
2. [ ] Build phonetic mapping table
3. [ ] Syntactic role classifier
4. [ ] Embedding validation tests
5. [ ] Compression ratio benchmarks
6. [ ] Semantic similarity evaluation

---

*The GLM does not read words. It reads the geometry of meaning.*
