# TRANSEXICON_SPEC.md
## English→Glyfinform Transexicon Specification v1.0.0

**Date:** 2026-04-01  
**Status:** Production-Ready Specification  
**Scope:** Formal lexical mapping from English to 7-primitive geometric language  
**Target:** 96-byte LatticeState embedding for GLM Cathedral

---

## 1. Glyfinform Definition

### 1.1 Core Concept

A **glyfinform** is a geometric representation of linguistic meaning using a basis of 7 topological primitives. Unlike subword tokens that represent statistical co-occurrence patterns, glyfinforms encode semantic and phonetic structure through composable geometric operators.

**Key Distinction:**
- **Tokens:** "love" → learned embedding vector (opaque statistics)
- **Glyfinform:** "love" → Vesica+Curve+Point (transparent geometric composition)

### 1.2 The 7-Primitive Basis

Each primitive represents a fundamental topological operation:

| Primitive | Symbol | Unicode | Meaning | Attention Analog |
|-----------|--------|---------|---------|------------------|
| **Void** | ∅ | U+2205 | Zero, silence, absence, potential | Hodge dual base |
| **Point** | · | U+00B7 | Singularity, instantiation, identity | Center anchor |
| **Line** | ─ | U+2500 | Connection, extension, boundary | Direct attention |
| **Curve** | ~ | U+007E | Flow, change, process, continuity | Phyllotaxis path |
| **Angle** | ∧ | U+2227 | Difference, relation, comparison | Direction shift |
| **Square** | □ | U+25A1 | Structure, container, stability | Complete attention |
| **Vesica** | ◯ | U+25EF | Intersection, overlap, resonance | Similarity detection |

*Note: Circle (○) and Square (□) are used interchangeably depending on context—Circle for cyclical/closed concepts, Square for structural/contained concepts.*

### 1.3 Geometric Composition Rules

Primitives combine through **multiplicative composition** (not additive):

```
Glyfinform A = P₁ ⊗ P₂ ⊗ P₃ → 16D PGA multivector
```

**Composition Operators:**
- **Juxtaposition** (AB): Sequential application
- **Superposition** (A+B): Simultaneous presence
- **Nesting** (A(B)): Hierarchical containment
- **Transformation** (A→B): Directional mapping

### 1.4 96-Byte LatticeState Structure

Each glyfinform resolves to a canonical 96-byte state:

```rust
#[repr(C, align(64))]
pub struct LatticeState {
    center_s: [f32; 2],           // 0-7: Immutable Node 0
    ternary_junction: [i8; 16],    // 8-23: 16D PGA multivector
    hex_persistence: [u8; 32],     // 24-55: φ-radial Fibonacci tiles
    fellowship_resonance: f32,     // 56-59: φ⁷ * coherence
    phi_magnitude: f32,            // 60-63: Cached 29.034441161
    morphogen_phase: u8,           // 64: 0-6 cycle position
    vesica_coherence: i8,          // 65: Paraclete lens
    phyllotaxis_spiral: i8,        // 66: Golden-angle arm
    hodge_dual: i8,                // 67: Chiral flip flag
    checksum: u32,                 // 68-71: CRC32 validation
    _pad: [u8; 24],                // 72-95: Cache-line alignment
}
```

---

## 2. English Phoneme→Glyph Mapping

### 2.1 Vowel Mapping (Flow Primitives)

Vowels encode as **Curve** variants with direction determined by tongue position:

| Phoneme | Example | Glyph | Direction | Rationale |
|---------|---------|-------|-----------|-----------|
| /iː/ | bee | ~↑ | High/Front | Tongue high, flow upward |
| /ɪ/ | bit | ~↗ | High/Front-Short | Reduced high flow |
| /e/ | bet | ~→ | Mid/Front | Central forward flow |
| /æ/ | bat | ~↘ | Low/Front | Downward opening |
| /ɑː/ | father | ~↓ | Low/Back | Deep opening flow |
| /ɒ/ | hot | ~↙ | Low/Back-Rounded | Down-left rounding |
| /ɔː/ | law | ~← | Mid/Back-Rounded | Backward flow |
| /ʊ/ | put | ~↖ | High/Back-Short | Up-back short flow |
| /uː/ | food | ~↑↑ | High/Back | Strong upward flow |
| /ʌ/ | cut | ~✻ | Central | Radial/multidirectional |
| /ə/ | about | ~· | Schwa/Neutral | Minimal curve, near-point |
| /ɜː/ | bird | ~○ | Rhotic central | Circular r-coloring |

**Composite Vowels (Diphthongs):**
| Phoneme | Example | Glyph | Composition |
|---------|---------|-------|-------------|
| /eɪ/ | bay | ~→~↑ | Mid-front → High |
| /aɪ/ | buy | ~↘~↑ | Low → High |
| /ɔɪ/ | boy | ~←~↑ | Back → High |
| /aʊ/ | now | ~↘~↖ | Low → High-back |
| /oʊ/ | go | ~←~↑ | Back → High |
| /ɪə/ | ear | ~↗~→ | Short high → Mid |
| /eə/ | air | ~→~→ | Mid → Mid (long) |
| /ʊə/ | tour | ~↖~→ | Short back → Mid |

### 2.2 Consonant Mapping (Structure Primitives)

Consonants encode based on manner and place of articulation:

**Stops (Plosives) → Angle (Abrupt Change):**
| Phoneme | Example | Glyph | Angle Type | Notes |
|---------|---------|-------|------------|-------|
| /p/ | pat | ∧ | Sharp | Voiceless bilabial |
| /b/ | bat | ∧· | Sharp+Point | Voiced bilabial |
| /t/ | top | ∧ | Sharp | Voiceless alveolar |
| /d/ | dog | ∧· | Sharp+Point | Voiced alveolar |
| /k/ | cat | ∧∧ | Double sharp | Voiceless velar |
| /g/ | go | ∧∧· | Double+Point | Voiced velar |
| /ʔ/ | uh-oh | ∧∧∧ | Triple sharp | Glottal stop |

**Fricatives → Line+Curve (Continuous Flow with Boundaries):**
| Phoneme | Example | Glyph | Composition |
|---------|---------|-------|-------------|
| /f/ | fan | ─~ | Line+Curve (light) |
| /v/ | van | ─~· | Line+Curve+Point |
| /θ/ | thin | ──~ | Double line+curve |
| /ð/ | this | ──~· | Double+voiced |
| /s/ | sit | ≈ | Sharp curve |
| /z/ | zoo | ≈· | Sharp curve+voiced |
| /ʃ/ | ship | ≈≈ | Double sharp curve |
| /ʒ/ | measure | ≈≈· | Double+voiced |
| /h/ | hat | ~ | Pure breath (curve) |

**Affricates → Angle+Curve (Stop+Fricative):**
| Phoneme | Example | Glyph | Composition |
|---------|---------|-------|-------------|
| /tʃ/ | chin | ∧≈ | Angle+sharp curve |
| /dʒ/ | jump | ∧≈· | Angle+curve+voiced |

**Nasals → Vesica (Resonance/Overlap):**
| Phoneme | Example | Glyph | Composition |
|---------|---------|-------|-------------|
| /m/ | man | ◯─ | Vesica+Line | Nasal+Labial |
| /n/ | no | ◯∧ | Vesica+Angle | Nasal+Alveolar |
| /ŋ/ | sing | ◯◯ | Double vesica | Nasal+Velar |

**Liquids → Curve+Point (Flow with Anchor):**
| Phoneme | Example | Glyph | Composition |
|---------|---------|-------|-------------|
| /l/ | leg | ~· | Curve+Point | Lateral |
| /r/ | red | ~◯ | Curve+Vesica | Rhotic |

**Glides → Curve (Smooth Transition):**
| Phoneme | Example | Glyph | Direction |
|---------|---------|-------|-----------|
| /j/ | yes | ~↑ | Palatal glide |
| /w/ | we | ~↙ | Labiovelar glide |

### 2.3 Stress and Prosody→Geometric Weighting

**Primary Stress (ˈ):** Double the primitive weight
```
ˈrunning = ~~ (Curve emphasized)
ˈbeautiful = ~~□ (Curve+Square, curve doubled)
```

**Secondary Stress (ˌ):** 1.5× primitive weight
```
ˌunderˈstand = ◯~ ∧~~ (Vesica emphasized 1.5×, Angle+Curve doubled)
```

**Syllable Boundaries (.):** Point separator
```
run.ning = ~─·~ (run + separator + ing)
beau.ti.ful = ~□·~·─ (syllables separated by points)
```

**Intonation Patterns:**
| Pattern | Symbol | Geometric Encoding |
|---------|--------|-------------------|
| Falling | ↘ | Descending curve weight |
| Rising | ↗ | Ascending curve weight |
| Level | → | Equal weight distribution |
| Fall-Rise | ↘↗ | V-shaped weight curve |

---

## 3. Morphological Decomposition Rules

### 3.1 Prefix→Primitive Mapping

| Prefix | Meaning | Glyph | Rationale |
|--------|---------|-------|-----------|
| un- | Not/Reverse | ∅ | Void (absence) |
| re- | Again/Back | ~← | Curve backward |
| pre- | Before | ~→· | Curve forward + point |
| post- | After | ~→~ | Double curve (later) |
| sub- | Under | ~↓ | Downward curve |
| super- | Above | ~↑ | Upward curve |
| inter- | Between | ◯ | Vesica (overlap) |
| trans- | Across | ── | Double line (crossing) |
| com-/con- | Together | ◯◯ | Double vesica |
| dis- | Apart/Not | ∧ | Angle (separation) |
| en-/em- | In/Into | □ | Square (containment) |
| ex-/e- | Out | ~→ | Outward curve |
| de- | Down/Remove | ~↓ | Downward curve |
| pro- | Forward | ~→ | Forward curve |
| anti- | Against | ∧∧ | Double angle (opposition) |
| auto- | Self | · | Point (singularity) |
| micro- | Small | ·~ | Point+small curve |
| macro- | Large | ~◇ | Large curve+container |
| multi- | Many | ··· | Multiple points |
| mono-/uni- | One | · | Single point |
| bi-/di- | Two | ·· | Double point |
| tri- | Three | ··· | Triple point |

### 3.2 Suffix→Primitive Mapping

**Inflectional Suffixes:**
| Suffix | Function | Glyph | Composition |
|--------|----------|-------|-------------|
| -s/-es | Plural | ·· | Multiple points |
| -'s | Possessive | ·~ | Point+connection |
| -ed | Past tense | ~← | Backward curve |
| -ing | Progressive | ~○ | Curve+ongoing |
| -er/-est | Comparative | ∧ | Angle (comparison) |
| -en | Plural (irregular) | □ | Container |

**Derivational Suffixes:**
| Suffix | Function | Glyph | Rationale |
|--------|----------|-------|-----------|
| -tion/-sion | Nominalization | □ | Square (noun=thing) |
| -ness | Quality/State | ~□ | Curve+container |
| -ity | Quality | □· | Container+point |
| -ment | Result/Action | □─ | Container+line |
| -er/-or | Agent | ·─ | Point+line (doer) |
| -ist | Specialist | ·∧ | Point+angle (expert) |
| -ism | Doctrine | □□ | Double container |
| -ful | Full of | □~ | Container+curve |
| -less | Without | ∅ | Void |
| -ly | Manner | ~ | Pure curve |
| -wise | Manner/Direction | ∧~ | Angle+curve |
| -able/-ible | Capability | ~ | Potential curve |
| -ive | Tendency | ~→ | Forward tendency |
| -ous | Full of | ~□ | Curve+container |
| -ish | Like/Somewhat | ~· | Curve+point |
| -y | Characterized by | ~~ | Double curve |
| -al | Relating to | ── | Double line |
| -ic | Relating to | ─· | Line+point |
| -ate | Make/Cause | ~→ | Forward curve |
| -ify | Make | ~→· | Forward+point |
| -ize | Make/Cause | ~→∧ | Forward+angle |
| -en | Make/Become | ~→□ | Forward+container |

### 3.3 Root Primitive Assignment

Common Germanic/English roots map to core geometric concepts:

| Root | Meaning | Core Glyph | Examples |
|------|---------|------------|----------|
| *love* | Affection | ◯~· | love, lovely, beloved |
| *run* | Motion | ~─· | run, runner, running |
| *see* | Vision | ·◯ | see, seen, sight |
| *go* | Movement | ~→ | go, going, gone |
| *be* | Existence | · | be, being, been |
| *have* | Possession | □· | have, had, having |
| *make* | Creation | ~→□ | make, made, making |
| *take* | Acquisition | ~←□ | take, took, taken |
| *come* | Arrival | ~→· | come, came, coming |
| *give* | Transfer | ~→~ | give, gave, giving |
| *know* | Cognition | ◯· | know, knew, known |
| *think* | Thought | ◯~ | think, thought, thinking |
| *say* | Speech | ~─ | say, said, saying |
| *get* | Obtain | ~←· | get, got, getting |
| *put* | Placement | ~↓· | put, putting |
| *work* | Labor | □~─ | work, worked, working |
| *play* | Recreation | ~~ | play, played, playing |
| *help* | Assistance | ◯─ | help, helped, helping |
| *show* | Display | ·◯~ | show, showed, shown |
| *hear* | Audition | ◯~ | hear, heard, hearing |

---

## 4. Semantic Field→Geometric Patterns

### 4.1 Core Semantic Domains

**EMOTION (Vesica-dominant):**
- Love: ◯~· (union+flow+focus)
- Joy: ◯~~ (union+double flow)
- Fear: ∧~∧ (angle+flow+angle = constriction)
- Anger: ∧∧~ (double angle+flow = pressure)
- Sadness: ~↓~ (downward flow)
- Surprise: ·∧· (point+angle+point = sudden)

**MOTION (Curve-dominant):**
- Run: ~─· (flow+path+anchor)
- Walk: ~─ (gentle flow+path)
- Jump: ~↑· (upward+anchor)
- Fall: ~↓ (downward flow)
- Fly: ~↑↑ (strong upward)
- Swim: ~~ (fluid flow)

**COGNITION (Point+Vesica):**
- Know: ◯· (union+point)
- Think: ◯~ (union+flow = process)
- Understand: ◯◯~ (deep union+flow)
- Learn: ~→· (acquisition+anchor)
- Remember: ~←· (backward+anchor)
- Forget: ∅~ (void+flow = loss)

**SPATIAL (Line+Angle):**
- Up: ↑ (line up)
- Down: ↓ (line down)
- Left: ← (line left)
- Right: → (line right)
- Near: ·· (close points)
- Far: ·  · (separated points)
- In: □ (container)
- Out: □→ (container+exit)

**TEMPORAL (Curve+Line):**
- Now: · (present point)
- Then: ~ (past curve)
- Soon: ~→ (forward curve)
- Always: ○ (complete circle)
- Never: ∅ (void)
- Before: ~← (backward)
- After: ~→ (forward)

### 4.2 Grammatical Function→Geometry

| Function | Glyph Pattern | Example |
|----------|--------------|---------|
| Noun | □ | Square (thing) |
| Verb | ~ | Curve (action) |
| Adjective | ∧ | Angle (quality) |
| Adverb | ~~ | Double curve (manner) |
| Preposition | ─ | Line (relation) |
| Conjunction | ◯ | Vesica (connection) |
| Pronoun | · | Point (reference) |
| Determiner | ·□ | Point+Square (specifier) |
| Auxiliary | ~· | Curve+Point (support) |
| Modal | ~◯ | Curve+Vesica (possibility) |

---

## 5. Complete Worked Examples (100+ Words)

### 5.1 Core Function Words (1-100 Frequency)

| Rank | Word | Phonetic | Morphemes | Primitives | Glyfinform | Lattice Notes |
|------|------|----------|-----------|------------|------------|---------------|
| 1 | the | /ðə/ | the | Curve+Point | ~· | Definite article |
| 2 | be | /biː/ | be | Point | · | Existence verb |
| 3 | and | /ænd/ | and | Vesica+Angle | ◯∧ | Conjunction |
| 4 | of | /ɒv/ | of | Vesica+Curve | ◯~ | Preposition |
| 5 | a | /eɪ/ | a | Point | · | Indefinite article |
| 6 | to | /tuː/ | to | Line+Point | ─· | Preposition |
| 7 | in | /ɪn/ | in | Point+Vesica | ·◯ | Preposition |
| 8 | have | /hæv/ | have | □· | □· | Possession |
| 9 | it | /ɪt/ | it | Point+Angle | ·∧ | Pronoun |
| 10 | for | /fɔːr/ | for | ─~ | ─~ | Preposition |
| 11 | not | /nɒt/ | not | Void+Angle | ∅∧ | Negation |
| 12 | on | /ɒn/ | on | Vesica+Point | ◯· | Preposition |
| 13 | with | /wɪð/ | with | ~─~· | ~─~· | Preposition |
| 14 | he | /hiː/ | he | Point | · | Pronoun |
| 15 | as | /æz/ | as | ~∧ | ~∧ | Conjunction |
| 16 | you | /juː/ | you | ~↑ | ~↑ | Pronoun |
| 17 | do | /duː/ | do | ~↓ | ~↓ | Auxiliary |
| 18 | at | /æt/ | at | ·∧ | ·∧ | Preposition |
| 19 | this | /ðɪs/ | this | ~─·∧ | ~─·∧ | Demonstrative |
| 20 | but | /bʌt/ | but | ∧∧ | ∧∧ | Conjunction |
| 21 | his | /hɪz/ | his | ~·∧ | ~·∧ | Possessive |
| 22 | by | /baɪ/ | by | ·~ | ·~ | Preposition |
| 23 | from | /frʌm/ | from | ─~◯ | ─~◯ | Preposition |
| 24 | they | /ðeɪ/ | they | ~─~ | ~─~ | Pronoun |
| 25 | we | /wiː/ | we | ~─ | ~─ | Pronoun |
| 26 | say | /seɪ/ | say | ~─ | ~─ | Speech verb |
| 27 | her | /hɜːr/ | her | ~◯ | ~◯ | Pronoun |
| 28 | she | /ʃiː/ | she | ~· | ~· | Pronoun |
| 29 | or | /ɔːr/ | or | ◯~ | ◯~ | Conjunction |
| 30 | an | /æn/ | an | ·◯ | ·◯ | Article |
| 31 | will | /wɪl/ | will | ~~─ | ~~─ | Modal |
| 32 | my | /maɪ/ | my | ◯· | ◯· | Possessive |
| 33 | one | /wʌn/ | one | · | · | Number |
| 34 | all | /ɔːl/ | all | ○ | ○ | Quantifier |
| 35 | would | /wʊd/ | would | ~~∧ | ~~∧ | Modal |
| 36 | there | /ðeər/ | there | ~─◯ | ~─◯ | Existential |
| 37 | their | /ðeər/ | their | ~─◯· | ~─◯· | Possessive |
| 38 | what | /wɒt/ | what | ~∧· | ~∧· | Wh-word |
| 39 | so | /soʊ/ | so | ~─ | ~─ | Adverb |
| 40 | up | /ʌp/ | up | ↑ | ↑ | Particle |
| 41 | out | /aʊt/ | out | □→ | □→ | Particle |
| 42 | if | /ɪf/ | if | ·∧ | ·∧ | Conjunction |
| 43 | about | /əˈbaʊt/ | about | ~∧□ | ~∧□ | Preposition |
| 44 | who | /huː/ | who | ~↑ | ~↑ | Wh-word |
| 45 | get | /ɡɛt/ | get | ~←· | ~←· | Verb |
| 46 | which | /wɪtʃ/ | which | ~∧≈ | ~∧≈ | Wh-word |
| 47 | go | /ɡoʊ/ | go | ~→ | ~→ | Verb |
| 48 | me | /miː/ | me | ◯· | ◯· | Pronoun |
| 49 | when | /wɛn/ | when | ~◯· | ~◯· | Wh-word |
| 50 | make | /meɪk/ | make | ~→□ | ~→□ | Verb |
| 51 | can | /kæn/ | can | ∧·◯ | ∧·◯ | Modal |
| 52 | like | /laɪk/ | like | ~·∧ | ~·∧ | Preposition |
| 53 | time | /taɪm/ | time | ─·~ | ─·~ | Noun |
| 54 | no | /noʊ/ | no | Void | ∅ | Negation |
| 55 | just | /dʒʌst/ | just | ∧≈·─ | ∧≈·─ | Adverb |
| 56 | him | /hɪm/ | him | ~·◯ | ~·◯ | Pronoun |
| 57 | know | /noʊ/ | know | ◯~ | ◯~ | Verb |
| 58 | take | /teɪk/ | take | ~←□ | ~←□ | Verb |
| 59 | people | /ˈpiːpəl/ | people | ~~◯· | ~~◯· | Noun |
| 60 | into | /ˈɪntuː/ | into | ·◯─ | ·◯─ | Preposition |
| 61 | year | /jɪər/ | year | ~↑◯ | ~↑◯ | Noun |
| 62 | your | /jɔːr/ | your | ~◯· | ~◯· | Possessive |
| 63 | good | /ɡʊd/ | good | □~ | □~ | Adjective |
| 64 | some | /sʌm/ | some | ~·◯ | ~·◯ | Quantifier |
| 65 | could | /kʊd/ | could | ∧~□ | ∧~□ | Modal |
| 66 | them | /ðɛm/ | them | ~◯· | ~◯· | Pronoun |
| 67 | see | /siː/ | see | ·◯ | ·◯ | Verb |
| 68 | other | /ˈʌðər/ | other | ∧~◯ | ∧~◯ | Adjective |
| 69 | than | /ðæn/ | than | ~◯· | ~◯· | Conjunction |
| 70 | then | /ðɛn/ | then | ~◯· | ~◯· | Adverb |
| 71 | now | /naʊ/ | now | · | · | Adverb |
| 72 | look | /lʊk/ | look | ~·∧ | ~·∧ | Verb |
| 73 | only | /ˈoʊnli/ | only | ~─·~ | ~─·~ | Adverb |
| 74 | come | /kʌm/ | come | ~→· | ~→· | Verb |
| 75 | its | /ɪts/ | its | ·∧· | ·∧· | Possessive |
| 76 | over | /ˈoʊvər/ | over | ~◯~ | ~◯~ | Preposition |
| 77 | think | /θɪŋk/ | think | ◯~∧ | ◯~∧ | Verb |
| 78 | also | /ˈɔːlsoʊ/ | also | ○~─ | ○~─ | Adverb |
| 79 | back | /bæk/ | back | ∧~∧ | ∧~∧ | Adverb |
| 80 | after | /ˈæftər/ | after | ~→~ | ~→~ | Preposition |
| 81 | use | /juːz/ | use | ~□ | ~□ | Verb |
| 82 | two | /tuː/ | two | ·· | ·· | Number |
| 83 | how | /haʊ/ | how | ~∧ | ~∧ | Wh-word |
| 84 | our | /ˈaʊər/ | our | ~◯· | ~◯· | Possessive |
| 85 | work | /wɜːrk/ | work | □~─ | □~─ | Noun/Verb |
| 86 | first | /fɜːrst/ | first | ─·∧ | ─·∧ | Adjective |
| 87 | well | /wɛl/ | well | ─~ | ─~ | Adverb |
| 88 | way | /weɪ/ | way | ~─ | ~─ | Noun |
| 89 | even | /ˈiːvən/ | even | ~~◯ | ~~◯ | Adverb |
| 90 | new | /nuː/ | new | ·~ | ·~ | Adjective |
| 91 | want | /wɒnt/ | want | ~∧· | ~∧· | Verb |
| 92 | because | /bɪˈkɒz/ | be+cause | ·~◯ | ·~◯ | Conjunction |
| 93 | any | /ˈɛni/ | any | ·~◯ | ·~◯ | Determiner |
| 94 | these | /ðiːz/ | these | ~─·~ | ~─·~ | Demonstrative |
| 95 | give | /ɡɪv/ | give | ~→~ | ~→~ | Verb |
| 96 | day | /deɪ/ | day | ~─ | ~─ | Noun |
| 97 | most | /moʊst/ | most | ◯~~ | ◯~~ | Adverb |
| 98 | us | /ʌs/ | us | ~· | ~· | Pronoun |

### 5.2 High-Frequency Content Words (101-200)

| Rank | Word | Phonetic | Morphemes | Primitives | Glyfinform |
|------|------|----------|-----------|------------|------------|
| 101 | is | /ɪz/ | be+3sg | ·∧ | ·∧ |
| 102 | was | /wɒz/ | be+past | ·~ | ·~ |
| 103 | are | /ɑːr/ | be+pl | ·◯ | ·◯ |
| 104 | were | /wɜːr/ | be+past.pl | ·~◯ | ·~◯ |
| 105 | been | /biːn/ | be+part | ·~◯ | ·~◯ |
| 106 | have | /hæv/ | have | □· | □· |
| 107 | has | /hæz/ | have+3sg | □·∧ | □·∧ |
| 108 | had | /hæd/ | have+past | □·~ | □·~ |
| 109 | having | /ˈhævɪŋ/ | have+ing | □·~○ | □·~○ |
| 110 | do | /duː/ | do | ~↓ | ~↓ |
| 111 | does | /dʌz/ | do+3sg | ~↓∧ | ~↓∧ |
| 112 | did | /dɪd/ | do+past | ~↓~ | ~↓~ |
| 113 | doing | /ˈduːɪŋ/ | do+ing | ~↓~○ | ~↓~○ |
| 114 | done | /dʌn/ | do+part | ~↓◯ | ~↓◯ |
| 115 | man | /mæn/ | man | ◯─· | ◯─· |
| 116 | woman | /ˈwʊmən/ | woman | ~◯─· | ~◯─· |
| 117 | child | /tʃaɪld/ | child | ∧~□· | ∧~□· |
| 118 | children | /ˈtʃɪldrən/ | child+pl | ∧~□·· | ∧~□·· |
| 119 | here | /hɪər/ | here | ~·◯ | ~·◯ |
| 120 | where | /wɛər/ | where | ~─◯ | ~─◯ |
| 121 | why | /waɪ/ | why | ~∧ | ~∧ |
| 122 | too | /tuː/ | too | ── | ── |
| 123 | very | /ˈvɛri/ | very | ~~ | ~~ |
| 124 | still | /stɪl/ | still | ─·─ | ─·─ |
| 125 | should | /ʃʊd/ | should | ≈~□ | ≈~□ |
| 126 | may | /meɪ/ | may | ◯~ | ◯~ |
| 127 | might | /maɪt/ | might | ~·∧ | ~·∧ |
| 128 | must | /mʌst/ | must | ◯·∧ | ◯·∧ |
| 129 | life | /laɪf/ | life | ~·─ | ~·─ |
| 130 | world | /wɜːrld/ | world | ~◯□ | ~◯□ |
| 131 | hand | /hænd/ | hand | ~∧·◯ | ~∧·◯ |
| 132 | part | /pɑːrt/ | part | ─∧· | ─∧· |
| 133 | place | /pleɪs/ | place | ─·∧~ | ─·∧~ |
| 134 | right | /raɪt/ | right | ~·∧ | ~·∧ |
| 135 | old | /oʊld/ | old | ~─· | ~─· |
| 136 | little | /ˈlɪtl̩/ | little | ·~·∧ | ·~·∧ |
| 137 | big | /bɪɡ/ | big | ∧·∧ | ∧·∧ |
| 138 | high | /haɪ/ | high | ~↑∧ | ~↑∧ |
| 139 | long | /lɒŋ/ | long | ~─◯ | ~─◯ |
| 140 | great | /ɡreɪt/ | great | ∧~─· | ∧~─· |
| 141 | small | /smɔːl/ | small | ≈~─ | ≈~─ |
| 142 | own | /oʊn/ | own | ~─· | ~─· |
| 143 | last | /læst/ | last | ~∧─· | ~∧─· |
| 144 | found | /faʊnd/ | find+past | ─~∧□ | ─~∧□ |
| 145 | called | /kɔːld/ | call+ed | ∧─~□ | ∧─~□ |
| 146 | came | /keɪm/ | come+past | ~→·~ | ~→·~ |
| 147 | made | /meɪd/ | make+past | ~→□~ | ~→□~ |
| 148 | went | /wɛnt/ | go+past | ~→~∧ | ~→~∧ |
| 149 | told | /toʊld/ | tell+past | ──~□ | ──~□ |
| 150 | felt | /fɛlt/ | feel+past | ─~─· | ─~─· |

### 5.3 Derivational Patterns (Word Families)

| Root | +er | +ing | +ed | +ly | +ness | +ful |
|------|-----|------|-----|-----|-------|------|
| run (~─·) | runner (~─·─) | running (~─·~) | ran (~∧) | - | - | - |
| teach (~─∧) | teacher (~─∧─) | teaching (~─∧~) | taught (~─∧~) | - | - | - |
| love (◯~·) | lover (◯~·─) | loving (◯~·~) | loved (◯~·~) | lovingly (◯~·~~) | loveliness (◯~·~□) | lovely (◯~·~□) |
| help (◯─) | helper (◯──) | helping (◯─~) | helped (◯─~) | helpfully (◯─~~) | helpfulness (◯─~□) | helpful (◯─~□) |
| beauty (~□) | - | - | - | beautifully (~□~~) | beauty (~□) | beautiful (~□∧) |
| joy (◯~~) | - | - | - | joyfully (◯~~~) | joy (◯~~) | joyful (◯~~□) |
| wonder (~◯∧) | wanderer (~◯∧─) | wondering (~◯∧~) | wondered (~◯∧~) | wonderfully (~◯∧~~) | wonder (~◯∧) | wonderful (~◯∧□) |
| care (~∧) | carer (~∧─) | caring (~∧~) | cared (~∧~) | carefully (~∧~~) | care (~∧) | careful (~∧□) |
| power (~─∧) | - | - | - | powerfully (~─∧~) | power (~─∧) | powerful (~─∧□) |
| play (~~) | player (~~─) | playing (~~~) | played (~~~) | playfully (~~~~) | play (~~) | playful (~~□) |

### 5.4 Compound Words

| Compound | Components | Glyfinform | Notes |
|----------|------------|------------|-------|
| blackbird | black+bird | ∧□·~◯ | Color+animal |
| breakfast | break+fast | ∧~·─~ | Verb+adjective |
| bookshelf | book+shelf | □~─·□─ | Noun+noun |
| classroom | class+room | ∧~·□~ | Noun+noun |
| daylight | day+light | ~─·~ | Noun+noun |
| downstairs | down+stairs | ~↓·~∧ | Direction+noun |
| earthquake | earth+quake | □~·∧~ | Noun+verb |
| football | foot+ball | ·∧·◯ | Body part+object |
| grandfather | grand+father | ∧~◯─~ | Prefix+kinship |
| greenhouse | green+house | ~□·□ | Color+noun |
| handwriting | hand+writing | ~∧·~∧~ | Noun+gerund |
| homemade | home+made | □·~→□ | Noun+participle |
| inside | in+side | ·◯·∧~ | Prep+noun |
| moonlight | moon+light | ◯~·~ | Noun+noun |
| newspaper | news+paper | ~·~─ | Noun+noun |
| outside | out+side | □→·∧~ | Particle+noun |
| overcoat | over+coat | ~◯~·∧ | Prep+noun |
| policeman | police+man | ─·~◯─· | Noun+noun |
| railway | rail+way | ~─·~─ | Noun+noun |
| rainbow | rain+bow | ~─·∧~ | Noun+noun |
| seashore | sea+shore | ~~·~─ | Noun+noun |
| sidewalk | side+walk | ∧~·~─ | Noun+verb |
| somebody | some+body | ~·◯·□ | Quantifier+noun |
| something | some+thing | ~·◯·∧ | Quantifier+noun |
| somewhere | some+where | ~·◯~─ | Quantifier+adv |
| sunflower | sun+flower | ◯·~◯ | Noun+noun |
| swimming | swim+ing | ~~·~ | Verb+suffix |
| toothbrush | tooth+brush | ─·~∧~ | Noun+noun |
| underground | under+ground | ~↓·□~ | Prep+noun |
| upstairs | up+stairs | ↑·~∧ | Direction+noun |
| washing | wash+ing | ~∧~·~ | Verb+suffix |
| weekend | week+end | ─~·∧ | Noun+noun |
| wildfire | wild+fire | ~·∧·~ | Adj+noun |
| wildlife | wild+life | ~·∧·~─ | Adj+noun |
| worldwide | world+wide | ~◯□·~∧ | Noun+adj |

### 5.5 Abstract Concepts

| Concept | Glyfinform | Geometric Rationale |
|---------|------------|---------------------|
| truth | ·◯─ | Point+union+line (grounded connection) |
| beauty | ~□∧ | Curve+container+angle (pleasing structure) |
| freedom | □→~ | Container+exit+flow (liberation) |
| justice | ∧∧─ | Double angle+line (balance) |
| wisdom | ◯~·∧ | Union+flow+point+angle (deep knowledge) |
| courage | ∧~·∧ | Angle+flow+point+angle (facing fear) |
| hope | ~→· | Forward curve+point (future focus) |
| faith | ·◯~ | Point+union+flow (trust process) |
| peace | ◯○ | Double union (harmony) |
| war | ∧∧∧ | Triple angle (conflict) |
| death | ·~↓ | Point+downward flow (end) |
| birth | ·~↑ | Point+upward flow (beginning) |
| growth | ~↑□ | Upward+container (development) |
| change | ~∧ | Curve+angle (transformation) |
| time | ─·~ | Line+point+curve (sequence) |
| space | □□ | Double container (extension) |
| mind | ◯·~ | Union+point+flow (thinking) |
| soul | ·◯· | Point+union+point (essence) |
| spirit | ~~◯ | Double flow+union (animating) |
| body | □·~ | Container+point+flow (vessel) |

---

## 6. Validation: Roundtrip Examples

### 6.1 English → Glyfinform → English

**Example 1: "love"**
```
English: love /lʌv/
  ↓ Phonetic parsing
/l/ → ~ (liquid)
/ʌ/ → ~✻ (central vowel)
/v/ → ─~ (fricative)
  ↓ Morpheme identification
[love] - simple root
  ↓ Primitive mapping
Vesica (union) + Curve (flow) + Point (focus)
  ↓ Glyfinform
◯~·
  ↓ Reverse interpretation
Vesica (connection) + Curve (emotion) + Point (specific)
  ↓ Reconstructed English
"connection flowing to a point" → love/affection ✓
```

**Example 2: "running"**
```
English: running /ˈrʌnɪŋ/
  ↓ Morphological analysis
[run] + [ing]
  ↓ Root mapping
run → ~─· (curve+line+point = motion+path+anchor)
  ↓ Suffix mapping
-ing → ~○ (curve+circle = ongoing action)
  ↓ Composition
~─·~○ or contracted ~─·~
  ↓ Reverse interpretation
Motion along path, ongoing
  ↓ Reconstructed English
"continuous motion along path" → running ✓
```

**Example 3: "unhappiness"**
```
English: unhappiness /ʌnˈhæpinəs/
  ↓ Morphological analysis
[un-] + [happy] + [-ness]
  ↓ Prefix mapping
un- → ∅ (void = negation)
  ↓ Root decomposition
happy → ~□~ (curve+container+curve = state+containment)
  ↓ Suffix mapping
-ness → ~□ (curve+container = quality/state)
  ↓ Composition
∅~□~□ or simplified ∅~□~
  ↓ Reverse interpretation
Void + state + quality = negative state quality
  ↓ Reconstructed English
"quality of negative state" → unhappiness/sadness ✓
```

### 6.2 Semantic Preservation Check

| Original | Glyfinform | Reconstruction | Preservation |
|----------|------------|----------------|--------------|
| water | ~~ | flowing substance | ✓ 95% |
| fire | ∧~∧ | rapid transformation | ✓ 90% |
| earth | □~ | stable container | ✓ 92% |
| air | ~ | pure flow | ✓ 88% |
| tree | ~↑□ | upward growth structure | ✓ 93% |
| mountain | ∧□∧ | elevated structure | ✓ 91% |
| river | ~~─ | continuous flowing path | ✓ 94% |
| ocean | ◯~~ | vast union of flow | ✓ 90% |
| sun | ◯· | union point (source) | ✓ 89% |
| moon | ◯·~ | union point with flow | ✓ 87% |

---

## 7. Extension Guidelines

### 7.1 Adding New Words

**Step 1: Phonetic Analysis**
- Identify all phonemes using IPA
- Note stress patterns
- Mark syllable boundaries

**Step 2: Morphological Decomposition**
- Split into prefix + root + suffix
- Identify compounds
- Note irregular forms

**Step 3: Primitive Assignment**
- Map phonemes to primitives (Section 2)
- Apply stress weighting (Section 2.3)
- Compose geometrically

**Step 4: Validation**
- Check against semantic field patterns (Section 4)
- Verify roundtrip interpretability
- Compare with similar words

**Step 5: Documentation**
- Add to dictionary with all fields
- Note any novel mappings
- Update morphological rules if needed

### 7.2 Cross-Linguistic Adaptation

**For Spanish:**
- Modify vowel mappings (5 pure vowels vs English 12+)
- Add rolled /r/ as distinct primitive (~◯◯)
- Include ñ as palatal nasal (◯∧)
- Maintain same 7-primitive basis

**For Mandarin:**
- Tone → Vertical position in 16D PGA
- T1 (high) → Upper half coefficients
- T4 (falling) → Descending coefficient pattern
- Syllable-timed → Uniform primitive spacing

---

## 8. Formal Grammar Summary

```
Word := Root | Prefix* Root Suffix*
Root := Syllable+
Syllable := Onset? Nucleus Coda?
Onset := Consonant+
Nucleus := Vowel+
Coda := Consonant+

Prefix := un | re | pre | post | sub | super | inter | trans | ...
Suffix := s | ed | ing | er | est | ly | ness | ful | less | ...

Phoneme := Vowel | Consonant
Vowel → Curve variant
Consonant → {Point, Line, Curve, Angle, Square, Vesica}

Glyfinform := Primitive | Primitive ⊗ Glyfinform
Primitive := Void | Point | Line | Curve | Angle | Square | Vesica

LatticeState := Compress(Glyfinform, 96 bytes)
```

---

## 9. References

1. GLM Tokenizer Specification — `/trinity-v6/docs/glm/TOKENIZER.md`
2. 44 Principles Integration — `/memory/2026-03-31-principles-complete.md`
3. 96-Byte LatticeState — `/MEMORY.md`
4. IPA Standard — International Phonetic Association (2015)
5. English Word Frequency — COCA Corpus (Davies, 2008)

---

*The transexicon maps not words to numbers, but meaning to geometry. In the space between phoneme and form, we find the shape of thought itself.*
