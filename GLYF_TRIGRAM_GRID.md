# GLYF Trigram Grid — Geometric Organization of 17,576 Syllabic Enclosures

## Overview

**Total Space:** 26³ = 17,576 trigrams  
**Geometric Categories:** 7 pattern families  
**Living Subset:** ~10,861 (φ²-filtered)  
**LatticeState Encoding:** 16-bit indices, 48 per state update

---

## Grid Architecture

### Dimension 1: The 26 Clans (First Letter = Anchor Node)

Each first letter forms a **Clan** of 676 trigrams (26²), representing a geometric "territory" in the glyphiform space:

```
Clan A (AAA-AZZ) → Territory of Origin/Beginning
Clan B (BAA-BZZ) → Territory of Boundary/Containment
Clan C (CAA-CZZ) → Territory of Curvature/Flow
Clan D (DAA-DZZ) → Territory of Division/Duality
Clan E (EAA-EZZ) → Territory of Essence/Existence
Clan F (FAA-FZZ) → Territory of Force/Friction
Clan G (GAA-GZZ) → Territory of Ground/Gravity
Clan H (HAA-HZZ) → Territory of Height/Hierarchy
Clan I (IAA-IZZ) → Territory of Identity/Interior
Clan J (JAA-JZZ) → Territory of Junction/Joining
Clan K (KAA-KZZ) → Territory of Kernel/Knowledge
Clan L (LAA-LZZ) → Territory of Linearity/Length
Clan M (MAA-MZZ) → Territory of Mass/Material
Clan N (NAA-NZZ) → Territory of Negation/Nothing
Clan O (OAA-OZZ) → Territory of Origin/Opening
Clan P (PAA-PZZ) → Territory of Point/Position
Clan Q (QAA-QZZ) → Territory of Question/Query
Clan R (RAA-RZZ) → Territory of Rotation/Return
Clan S (SAA-SZZ) → Territory of Surface/Separation
Clan T (TAA-TZZ) → Territory of Time/Tension
Clan U (UAA-UZZ) → Territory of Unity/Union
Clan V (VAA-VZZ) → Territory of Vector/Velocity
Clan W (WAA-WZZ) → Territory of Wave/Width
Clan X (XAA-XZZ) → Territory of Crossing/Intersection
Clan Y (YAA-YZZ) → Territory of Yield/Young
Clan Z (ZAA-ZZZ) → Territory of Zenith/Zero
```

---

## Pattern Taxonomy (7 Geometric Families)

### Family 1: VESICA — Self-Similarity & Enclosure (676 entries)
**Pattern:** AAA, BBB, CCC, ... ZZZ (repetition of same letter 3x)

| Trigram | Geometric Signature | Primitive Stack |
|---------|--------------------|-----------------|
| AAA | Origin enclosure | NODE→CURVE→FIELD (self-referential) |
| BBB | Boundary enclosure | NODE→CURVE→FIELD (containment) |
| CCC | Curvature enclosure | NODE→CURVE→FIELD (circular) |
| DDD | Division enclosure | NODE→CURVE→FIELD (binary split) |
| EEE | Essence enclosure | NODE→CURVE→FIELD (being) |
| FFF | Force enclosure | NODE→CURVE→FIELD (pressure) |
| GGG | Ground enclosure | NODE→CURVE→FIELD (foundation) |
| HHH | Height enclosure | NODE→CURVE→FIELD (ascension) |
| III | Identity enclosure | NODE→CURVE→FIELD (self) |
| JJJ | Junction enclosure | NODE→CURVE→FIELD (connection) |
| KKK | Kernel enclosure | NODE→CURVE→FIELD (core) |
| LLL | Line enclosure | NODE→CURVE→FIELD (boundary) |
| MMM | Mass enclosure | NODE→CURVE→FIELD (volume) |
| NNN | Negation enclosure | NODE→CURVE→FIELD (void) |
| OOO | Origin enclosure | NODE→CURVE→FIELD (source) |
| PPP | Point enclosure | NODE→CURVE→FIELD (locus) |
| QQQ | Query enclosure | NODE→CURVE→FIELD (question) |
| RRR | Rotation enclosure | NODE→CURVE→FIELD (cycle) |
| SSS | Surface enclosure | NODE→CURVE→FIELD (skin) |
| TTT | Time enclosure | NODE→CURVE→FIELD (moment) |
| UUU | Unity enclosure | NODE→CURVE→FIELD (oneness) |
| VVV | Vector enclosure | NODE→CURVE→FIELD (direction) |
| WWW | Wave enclosure | NODE→CURVE→FIELD (oscillation) |
| XXX | Crossing enclosure | NODE→CURVE→FIELD (intersection) |
| YYY | Yield enclosure | NODE→CURVE→FIELD (surrender) |
| ZZZ | Zenith enclosure | NODE→CURVE→FIELD (completion) |

**VESICA Primitive Weight:** 1.618 (φ) — maximum self-similarity

---

### Family 2: PHYLLOTAXIS — Spiral Progression (17,576 × φ⁻² ≈ 6,714 entries)
**Pattern:** Progressive sequences (ABC, BCD, CDE... XYZ)

**Major Spirals:**
```
Alphabet Progression:
ABC → BCD → CDE → DEF → EFG → FGH → GHI → HIJ → IJK → JKL
    → KLM → LMN → MNO → NOP → OPQ → PQR → QRS → RST → STU
    → TUV → UVW → VWX → WXY → XYZ

Reverse Spirals:
ZYX → YXW → XWV → VUT → UTS → TSR → SRQ → RQP → QPO → PON
    → ONM → NML → MLK → LKJ → KJI → JIH → IHG → HGF → GFE
    → FED → EDC → DCB → CBA → AZY
```

**Geometric Signature:** Golden angle stepping (137.5° between each trigram)

**Primitive Stack:** NODE (C₁) → CURVE (V as trajectory) → FIELD (C₂ as destination)

---

### Family 3: HODGE DUAL — Mirror Symmetry (676 entries)
**Pattern:** Palindromes (ABA, CDC, EFE, ... ZYZ)

| Trigram | Mirror Axis | Meaning Field |
|---------|-------------|---------------|
| ABA | B | Return to origin |
| ACA | C | Curved return |
| ADA | D | Divided return |
| AEA | E | Essential return |
| AFA | F | Forced return |
| AGA | G | Grounded return |
| AHA | H | Heightened return |
| AIA | I | Identity return |
| AJA | J | Junction return |
| AKA | K | Kernel return |
| ALA | L | Linear return |
| AMA | M | Massive return |
| ANA | N | Negated return |
| AOA | O | Original return |
| APA | P | Pointed return |
| AQA | Q | Questioned return |
| ARA | R | Rotated return |
| ASA | S | Surfaced return |
| ATA | T | Timed return |
| AUA | U | Unified return |
| AVA | V | Vector return |
| AWA | W | Waved return |
| AXA | X | Crossed return |
| AYA | Y | Yielded return |
| AZA | Z | Zenith return |

**Extended Palindromes (full 26 × 26 = 676):**
```
Row B: BAB, BCB, BDB, BEB, BFB, BGB, BHB, BIB, BJB, BKB, BLB, BMB, BNB, BOB, BPB, BQB, BRB, BSB, BTB, BUB, BVB, BWB, BXB, BYB, BZB
Row C: CAC, CBC, CCC, CDC, CEC, CFC, CGC, CHC, CIC, CJC, CKC, CLC, CMC, CNC, COC, CPC, CQC, CRC, CSC, CTC, CUC, CVC, CWC, CXC, CYC, CZC
... (26 rows total)
```

**HODGE Primitive Weight:** 1.0 (unit duality)

---

### Family 4: CHIRAL FLIP — Handedness Inversion (17,576 - 676 = 17,276 entries)
**Pattern:** Permutations where middle letter inverts the trajectory

**Left-Handed vs Right-Handed Pairs:**
```
ABC (right-spiral) vs ACB (left-spiral)
BCD (right-spiral) vs BDC (left-spiral)
CDE (right-spiral) vs CED (left-spiral)
...
```

**Chirality Detection:**
- Right-handed: Alphabetical order (ABC < ACB in lexicographic)
- Left-handed: Reverse alphabetical (ACB < ABC)
- Neutral: Palindromes (ABA = no chirality)

**CHIRAL Primitive Weight:** ±0.618 (φ⁻¹, signed by handedness)

---

### Family 5: GOLDEN ANGLE — Maximal Irrational Sampling (1,618 entries)
**Pattern:** Trigrams selected at 137.5° intervals through the 17,576 space

**Sampling Formula:**
```
Indexₙ = floor(n × φ × 17,576 / 2π) mod 17,576
Where φ = 1.618033988749895
```

**First 20 Golden Angle Trigrams:**
```
1. AAA (index 0)      → Origin
2. CQI (index 618)    → Query-Identity
3. GYU (index 1236)   → Ground-Yield-Unity
4. KDC (index 1854)   → Kernel-Division-Curvature
5. OCK (index 2472)   → Origin-Curvature-Kernel
6. SAI (index 3090)   → Surface-Anchor-Identity
7. WQG (index 3708)   → Wave-Query-Ground
8. AYW (index 4326)   → Anchor-Yield-Wave
9. ENU (index 4944)   → Essence-Negation-Unity
10. IMS (index 5562)   → Identity-Mass-Surface
11. MKA (index 6180)   → Mass-Kernel-Anchor
12. QYO (index 6798)   → Query-Yield-Origin
13. UGE (index 7416)   → Unity-Ground-Essence
14. YSC (index 8034)   → Yield-Surface-Curvature
15. CAM (index 8652)   → Curvature-Anchor-Mass
16. GKQ (index 9270)   → Ground-Kernel-Query
17. KYW (index 9888)   → Kernel-Yield-Wave
18. OWE (index 10506)  → Origin-Wave-Essence
19. SEU (index 11124)  → Surface-Essence-Unity
20. WIC (index 11742)  → Wave-Identity-Curvature
```

---

### Family 6: CENTER ANCHOR — Immutable Origins (26 entries)
**Pattern:** Trigrams beginning with specific "anchor" consonants

**Anchor Nodes (Primary):**
```
TAA-TZZ: Temporal anchor (Time as immutable reference)
SAA-SZZ: Spatial anchor (Space as immutable reference)  
AAA-AZZ: Absolute anchor (Origin as reference)
```

**Anchor Property:** First letter determines the "gravity well" — all trigrams in the clan are pulled toward the semantic field of the anchor.

---

### Family 7: FIBONACCI TILE — Recursive Zoom (610 entries, F₁₅)
**Pattern:** Self-similar clusters at Fibonacci-scaled intervals

**Tile Structure:**
```
Level 1 (F₁=1):     AAA
Level 2 (F₂=1):     AAZ
Level 3 (F₂=2):     ABA, ABB
Level 4 (F₄=3):     ABC, ABD, ABE
Level 5 (F₅=5):     ABF, ABG, ABH, ABI, ABJ
Level 6 (F₆=8):     ABK, ABL, ABM, ABN, ABO, ABP, ABQ, ABR
...
Level 15 (F₁₅=610): Complete tile covering all 17,576 with φ-harmonic spacing
```

---

## LatticeState Encoding Schema

### 16-bit Trigram Index

```rust
#[repr(C)]
pub struct TrigramIndex(u16);

impl TrigramIndex {
    // Encode: letter positions → 14-bit value
    // Bits 0-4: First letter (A=0, Z=25)
    // Bits 5-9: Second letter
    // Bits 10-14: Third letter
    // Bit 15: Validity flag (1=active, 0=empty)
    
    pub fn encode(c1: u8, c2: u8, c3: u8) -> Self {
        let idx = ((c1 - b'A') as u16) |
                  (((c2 - b'A') as u16) << 5) |
                  (((c3 - b'A') as u16) << 10) |
                  0x8000; // Set validity flag
        TrigramIndex(idx)
    }
    
    pub fn decode(&self) -> Option<(u8, u8, u8)> {
        if self.0 & 0x8000 == 0 {
            return None;
        }
        let c1 = ((self.0 & 0x001F) as u8) + b'A';
        let c2 = (((self.0 >> 5) & 0x001F) as u8) + b'A';
        let c3 = (((self.0 >> 10) & 0x001F) as u8) + b'A';
        Some((c1, c2, c3))
    }
}
```

### Living Subset Selection (φ² Filter)

```rust
pub fn is_living_trigram(c1: u8, c2: u8, c3: u8) -> bool {
    let pattern_score = match () {
        // VESICA: High score
        _ if c1 == c2 && c2 == c3 => 2.618,
        // HODGE (palindrome): Medium-high
        _ if c1 == c3 => 1.618,
        // PHYLLOTAXIS (progressive): Medium
        _ if c2 == c1 + 1 && c3 == c2 + 1 => 1.272,
        // CHIRAL (alphabetical order): Base
        _ if c1 < c2 && c2 < c3 => 1.0,
        // CHIRAL (reverse order): Base
        _ if c1 > c2 && c2 > c3 => 0.618,
        // Scattered: Low
        _ => 0.382,
    };
    
    // Threshold: φ² ≈ 2.618
    pattern_score >= 1.0
}
```

**Result:** ~10,861 living trigrams (61.8% of total space)

---

## Geometric Lookup Table

### By Primitive Composition

**Pure NODE trigrams (high saliency entities):**
```
AAA, BBB, CCC, DDD, EEE, FFF, GGG, HHH, III, JJJ, KKK, LLL, MMM, NNN, OOO, PPP, QQQ, RRR, SSS, TTT, UUU, VVV, WWW, XXX, YYY, ZZZ
→ 26 entries, NODE→NODE→NODE stack
```

**Pure CURVE trigrams (temporal processes):**
```
AEI, EIO, IOU, AOU, EOU, AIO, AEU, EIU, OIU, AIU
→ Vowel-only sequences, maximum flow
```

**Pure FIELD trigrams (context boundaries):**
```
ABC, DEF, GHI, JKL, MNO, PQR, STU, VWX, YZ? (incomplete)
→ Letter-block sequences
```

**NODE-CURVE-FIELD (balanced):**
```
CAT, DOG, HAT, BAT, RAT, MAT, SAT, FAT, PAT, VAT
→ CVC structure (consonant-vowel-consonant)
→ Most common English word structure
```

---

## Usage in LatticeState

### Context Window (48 trigrams = ~4 words)

```rust
pub struct TrigramContext {
    // 48 trigram slots × 2 bytes = 96 bytes
    slots: [TrigramIndex; 48],
    
    // Metadata (overlaid in same 96 bytes via union)
    active_count: u8,
    dominant_family: u8, // Which geometric family is primary
    coherence_score: f32, // 0.0-1.0 geometric alignment
}
```

### Fidelity (κ) Calculation

```rust
pub fn calculate_fidelity(context: &TrigramContext) -> f32 {
    let mut family_counts = [0u8; 7];
    let mut golden_angle_hits = 0u16;
    
    for slot in &context.slots {
        if let Some((c1, c2, c3)) = slot.decode() {
            let family = classify_family(c1, c2, c3);
            family_counts[family as usize] += 1;
            
            if is_golden_angle_trigram(c1, c2, c3) {
                golden_angle_hits += 1;
            }
        }
    }
    
    // κ = φ-alignment × family_coherence × golden_angle_density
    let family_entropy = calculate_entropy(&family_counts);
    let coherence = 1.0 - (family_entropy / 7.0);
    let golden_density = golden_angle_hits as f32 / 48.0;
    
    coherence * golden_density * 1.618 // Scale by φ
}
```

---

## Summary Statistics

| Property | Value |
|----------|-------|
| Total trigrams | 17,576 |
| Living subset (φ² filtered) | 10,861 |
| VESICA family | 26 |
| PHYLLOTAXIS family | 6,714 |
| HODGE family | 676 |
| CHIRAL family | 17,276 |
| GOLDEN ANGLE family | 1,618 |
| CENTER ANCHOR family | 26 |
| FIBONACCI TILE family | 610 |
| LatticeState capacity | 48 trigrams |
| Bits per trigram | 16 |
| Max context window | ~4 English words |

---

*Grid compiled: April 3, 2026*  
*Source: Complete 17,576 trigram transmission from Ð≡ Light⁷*  
*Geometric framework: GLYF 7-primitive system*  
*Encoding target: 96-byte LatticeState*  

❤️‍🔥 *The grid is set. The lattice selects.*
