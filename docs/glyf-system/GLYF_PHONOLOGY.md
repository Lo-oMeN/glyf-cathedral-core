# GLYF PHONOLOGY
## Sound→Geometry Mapping Specification v1.0.0

**Date:** 2026-04-01  
**Status:** Production Specification  
**Scope:** IPA phoneme classification, articulatory-to-geometric mapping, prosody encoding  
**Standards:** IPA (International Phonetic Alphabet) 2015 Revision

---

## 1. EXECUTIVE OVERVIEW

Glyf Phonology establishes the **geometric encoding of speech sounds**, mapping the articulatory features of phonemes to the 7-primitive glyfinform system. Unlike traditional phonology that describes sounds by their physical production, Glyf phonology encodes sounds by their **topological function** — how they structure meaning through form.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SOUND → GEOMETRY PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  INPUT: Speech Sound (IPA)                                               │
│     ↓                                                                    │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │  FEATURE EXTRACTION                                              │     │
│  │  • Place of articulation (where in vocal tract)                  │     │
│  │  • Manner of articulation (how airflow is modified)              │     │
│  │  • Voicing (vocal fold vibration)                                │     │
│  │  • Airstream mechanism (pulmonic, glottalic, velaric)            │     │
│  └────────────────────────────────────────────────────────────────┘     │
│     ↓                                                                    │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │  GEOMETRIC TRANSLATION                                           │     │
│  │  • Place → Spatial coordinates in vocal tract space              │     │
│  │  • Manner → Primitive type (Void, Point, Line, Curve, etc.)      │     │
│  │  • Voicing → Presence/absence of resonance (Vesica activation)   │     │
│  │  • Airflow → Directional vectors                                 │     │
│  └────────────────────────────────────────────────────────────────┘     │
│     ↓                                                                    │
│  OUTPUT: Glyfinform Primitive(s)                                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. IPA PHONEME CLASSIFICATION

### 2.1 Consonant Chart → Geometric Matrix

The IPA consonant chart organized by **Place** (columns) and **Manner** (rows):

```
        Labial   Dental  Alveolar  Postalv.  Retrof.  Palatal   Velar   Uvular  Pharyn. Glottal
        ───────────────────────────────────────────────────────────────────────────────────────
Plosive   p b │         t d │           │  ʈ ɖ  │  c ɟ  │  k g  │  q ɢ  │       │  ʔ
          ∧∧ │         ∧∧ │           │  ∧∧   │  ∧∧   │  ∧∧   │  ∧∧   │       │  ∧∧∧
          ────────────────────────────────────────────────────────────────────────────────────
Nasal     m   │         n   │           │  ɳ    │  ɲ    │  ŋ    │  ɴ    │       │
          ◯─  │         ◯∧  │           │  ◯∧   │  ◯∧   │  ◯◯   │  ◯◯   │       │
          ────────────────────────────────────────────────────────────────────────────────────
Trill     B   │         r   │           │       │       │       │  ʀ    │       │
          ~◯◯ │         ~◯◯ │           │       │       │       │  ~◯◯  │       │
          ────────────────────────────────────────────────────────────────────────────────────
Tap/Flap      │         ɾ   │           │  ɽ    │       │       │       │       │
              │         ~·  │           │  ~·   │       │       │       │       │
          ────────────────────────────────────────────────────────────────────────────────────
Fricative ɸ β │ f v │ θ ð │ s z │ ʃ ʒ │ ʂ ʐ │ ç ʝ │ x ɣ │ χ ʁ │ ħ ʕ │ h ɦ
          ─~  │ ─~  │ ──~ │ ≈   │ ≈≈  │ ≈≈  │ ≈~  │ ≈   │ ≈~  │ ──~ │ ~
          ────────────────────────────────────────────────────────────────────────────────────
Lat. fric.    │         ɬ ɮ │           │       │       │       │       │       │
              │         ≈~  │           │       │       │       │       │       │
          ────────────────────────────────────────────────────────────────────────────────────
Approx.  w    │ ʋ   │   ɹ   │           │  ɻ    │  j    │  ɰ    │       │       │
          ~↙  │ ~·  │   ~◯  │           │  ~◯   │  ~↑   │  ~↖   │       │       │
          ────────────────────────────────────────────────────────────────────────────────────
Lat. app.     │         l   │           │  ɭ    │  ʎ    │  ʟ    │       │       │
              │         ~·  │           │  ~·   │  ~·   │  ~·   │       │       │
```

### 2.2 Vowel Chart → Geometric Coordinates

The IPA vowel chart mapped to geometric positions:

```
         Front          Central         Back
         ─────────────────────────────────────
Close    i ·────── y     ɨ ·────── ʉ     ɯ ·────── u
         │~↑      ~↑↗    │~↑      ~↑↗    │~↑      ~↑↑
         │               │               │
         │               │               │
Close-mid│               │               │
         e ·────── ø     ɘ ·────── ɵ     ɤ ·────── o
         │~→      ~→↗    │~→      ~→↘    │~←      ~←↖
         │               │               │
Mid      │               ə ·             │
         │               │~·              │
         │               │               │
Open-mid ɛ ·────── œ     ɜ ·────── ɞ     ʌ ·────── ɔ
         │~↗      ~↗→    │~✻      ~↘←    │~↙      ~←↖
         │               │               │
Near-openæ ·             ɐ ·             │
         │~↘             │~↘             │
         │               │               │
Open     a ·────── ɶ     ä ·             ɑ ·────── ɒ
         │~↓      ~↓↘    │~↓             │~↓      ~↙
         └───────────────────────────────────────

Coordinate System:
  x-axis: Front (-1) ←────→ Back (+1)
  y-axis: Close (+1) ←────→ Open (-1)
```

### 2.3 Articulatory Feature → Primitive Mapping

#### Place of Articulation

| Place | Geometric Zone | Glyph Pattern | Rationale |
|-------|---------------|---------------|-----------|
| **Bilabial** | Anterior boundary | ∧ or ◯─ | Lips as enclosure |
| **Labiodental** | Lower boundary | ─~ | Teeth-lip contact |
| **Dental** | Central point | ·─~ | Tongue-tip precision |
| **Alveolar** | Anterior ridge | ∧ | Hard contact |
| **Postalveolar** | Posterior ridge | ≈ | Grooved channel |
| **Retroflex** | Curved back | ~◯ | Curling motion |
| **Palatal** | High center | ~↑ | Tongue body raise |
| **Velar** | Posterior chamber | ◯◯ | Back cavity |
| **Uvular** | Deep chamber | ◯◯~ | Extended resonance |
| **Pharyngeal** | Throat channel | ──~ | Constricted path |
| **Glottal** | Source point | ∧∧∧ | Glottal stop |

#### Manner of Articulation

| Manner | Geometric Type | Glyph | Dynamics |
|--------|---------------|-------|----------|
| **Plosive** | Angle/Sharp change | ∧ | Abrupt, complete closure |
| **Nasal** | Vesica/Resonance | ◯ | Airflow diversion |
| **Trill** | Oscillation | ~◯◯ | Rapid vibration |
| **Tap/Flap** | Instant | ~· | Brief contact |
| **Fricative** | Line+Curve | ─~ | Turbulent flow |
| **Lateral Fric.** | Angled flow | ≈~ | Side channel |
| **Approximant** | Smooth curve | ~ | Open channel |
| **Lateral App.** | Curve+Point | ~· | Side release |

#### Voicing

| Voicing | Resonance Pattern | Glyph Modification |
|---------|------------------|-------------------|
| **Voiceless** | No vocal fold activity | Base glyph only |
| **Voiced** | Vocal fold vibration | Add Point (·) |
| **Breathy** | Loose fold vibration | Add Curve (~) |
| **Creaky** | Tight fold vibration | Add Angle (∧) |

---

## 3. DETAILED PHONEME MAPPINGS

### 3.1 English Consonants

| Phoneme | Example | Place | Manner | Voicing | Glyfinform |
|---------|---------|-------|--------|---------|------------|
| /p/ | **p**at | Bilabial | Plosive | - | ∧ |
| /b/ | **b**at | Bilabial | Plosive | + | ∧· |
| /t/ | **t**op | Alveolar | Plosive | - | ∧ |
| /d/ | **d**og | Alveolar | Plosive | + | ∧· |
| /k/ | **c**at | Velar | Plosive | - | ∧∧ |
| /g/ | **g**o | Velar | Plosive | + | ∧∧· |
| /ʔ/ | uh-**o**h | Glottal | Plosive | - | ∧∧∧ |
| /m/ | **m**an | Bilabial | Nasal | + | ◯─ |
| /n/ | **n**o | Alveolar | Nasal | + | ◯∧ |
| /ŋ/ | si**ng** | Velar | Nasal | + | ◯◯ |
| /f/ | **f**an | Labiodental | Fricative | - | ─~ |
| /v/ | **v**an | Labiodental | Fricative | + | ─~· |
| /θ/ | **th**in | Dental | Fricative | - | ──~ |
| /ð/ | **th**is | Dental | Fricative | + | ──~· |
| /s/ | **s**it | Alveolar | Fricative | - | ≈ |
| /z/ | **z**oo | Alveolar | Fricative | + | ≈· |
| /ʃ/ | **sh**ip | Postalveolar | Fricative | - | ≈≈ |
| /ʒ/ | mea**s**ure | Postalveolar | Fricative | + | ≈≈· |
| /h/ | **h**at | Glottal | Fricative | - | ~ |
| /tʃ/ | **ch**in | Postalveolar | Affricate | - | ∧≈ |
| /dʒ/ | **j**ump | Postalveolar | Affricate | + | ∧≈· |
| /l/ | **l**eg | Alveolar | Lateral approx. | + | ~· |
| /r/ | **r**ed | Alveolar | Approximant | + | ~◯ |
| /w/ | **w**e | Labiovelar | Approximant | + | ~↙ |
| /j/ | **y**es | Palatal | Approximant | + | ~↑ |

### 3.2 English Vowels

| Phoneme | Example | Height | Backness | Rounding | Glyfinform |
|---------|---------|--------|----------|----------|------------|
| /iː/ | b**ee** | High | Front | - | ~↑ |
| /ɪ/ | b**i**t | Near-high | Front | - | ~↗ |
| /e/ | b**e**t | Mid | Front | - | ~→ |
| /æ/ | b**a**t | Low | Front | - | ~↘ |
| /ɑː/ | f**a**ther | Low | Back | - | ~↓ |
| /ɒ/ | h**o**t | Low | Back | + | ~↙ |
| /ɔː/ | l**aw** | Mid | Back | + | ~← |
| /ʊ/ | p**u**t | Near-high | Back | + | ~↖ |
| /uː/ | f**oo**d | High | Back | + | ~↑↑ |
| /ʌ/ | c**u**t | Mid | Central | - | ~✻ |
| /ə/ | ab**ou**t | Mid | Central | - | ~· |
| /ɜː/ | b**ir**d | Mid | Central | +r | ~○ |
| /eɪ/ | b**ay** | Diphthong | Front-rise | - | ~→~↑ |
| /aɪ/ | b**uy** | Diphthong | Low→High | - | ~↘~↑ |
| /ɔɪ/ | b**oy** | Diphthong | Back→High | + | ~←~↑ |
| /aʊ/ | n**ow** | Diphthong | Low→High+ | - | ~↘~↖ |
| /oʊ/ | g**o** | Diphthong | Back→High+ | + | ~←~↑ |
| /ɪə/ | **ear** | Diphthong | High→Mid | - | ~↗~→ |
| /eə/ | **air** | Diphthong | Mid | - | ~→~→ |
| /ʊə/ | t**our** | Diphthong | High→Mid | + | ~↖~→ |

### 3.3 Spanish Phonemes

| Phoneme | Example | Glyfinform | Notes |
|---------|---------|------------|-------|
| /p/ | **p**adre | ∧ | Same as English |
| /b/ | **b**ien | ∧· | Lenited to [β] intervocalic |
| /t/ | **t**iempo | ∧ | Dental, not alveolar |
| /d/ | **d**ía | ∧· | Lenited to [ð] intervocalic |
| /k/ | **c**asa | ∧∧ | Same as English |
| /g/ | **g**ato | ∧∧· | Lenited to [ɣ] intervocalic |
| /ʝ/ | **y**o, ll**ama** | ~↑ | Varies by dialect |
| /ʧ/ | **ch**ico | ∧≈ | Same as English /tʃ/ |
| /r/ | **r**ato | ~· | Tap (single) |
| /rr/ | pe**rr**o | ~◯◯ | Trill (multiple) |
| /f/ | **f**lor | ─~ | Same as English |
| /θ/ | **z**apato, **c**enar | ──~ | Northern Spain only |
| /s/ | **s**er | ≈ | Apical or dental |
| /x/ | **j**amás | ≈~ | Stronger than English /h/ |
| /m/ | **m**ano | ◯─ | Same as English |
| /n/ | **n**oche | ◯∧ | Same as English |
| /ɲ/ | **ñ**oño | ◯∧ | Palatal nasal |
| /l/ | **l**uz | ~· | Clear [l] |
| /ʎ/ | ca**ll**e | ~· | Merges with /ʝ/ in many dialects |

**Spanish Vowels (5 pure):**
| Phoneme | Example | Glyfinform | Position |
|---------|---------|------------|----------|
| /i/ | s**í** | ~↑ | High front |
| /e/ | s**e** | ~→ | Mid front |
| /a/ | s**a** | ~↓ | Low central |
| /o/ | s**o** | ~← | Mid back |
| /u/ | s**u** | ~↑↑ | High back |

### 3.4 Mandarin Phonemes

**Initials (Consonants):**
| Pinyin | IPA | Glyfinform | Description |
|--------|-----|------------|-------------|
| b | /p/ | ∧ | Voiceless unaspirated |
| p | /pʰ/ | ∧~ | Voiceless aspirated |
| m | /m/ | ◯─ | Bilabial nasal |
| f | /f/ | ─~ | Labiodental fricative |
| d | /t/ | ∧ | Voiceless unaspirated |
| t | /tʰ/ | ∧~ | Voiceless aspirated |
| n | /n/ | ◯∧ | Alveolar nasal |
| l | /l/ | ~· | Alveolar lateral |
| g | /k/ | ∧∧ | Voiceless unaspirated |
| k | /kʰ/ | ∧∧~ | Voiceless aspirated |
| h | /x/ | ≈~ | Velar fricative |
| j | /tɕ/ | ∧~↑ | Voiceless palatal |
| q | /tɕʰ/ | ∧~↑~ | Voiceless aspirated palatal |
| x | /ɕ/ | ≈~↑ | Voiceless palatal fricative |
| zh | /ʈʂ/ | ∧~◯ | Voiceless retroflex |
| ch | /ʈʂʰ/ | ∧~◯~ | Voiceless aspirated retroflex |
| sh | /ʂ/ | ≈~◯ | Voiceless retroflex fricative |
| r | /ɻ/ | ~◯ | Voiced retroflex approximant |
| z | /ts/ | ∧~ | Voiceless alveolar affricate |
| c | /tsʰ/ | ∧~~ | Voiceless aspirated alveolar |
| s | /s/ | ≈ | Voiceless alveolar fricative |

**Finals (Vowels + Codas):**
| Pinyin | IPA | Glyfinform | Composition |
|--------|-----|------------|-------------|
| -i (after z/c/s) | /ɨ/ | ~· | Apical vowel |
| -i (after zh/ch/sh/r) | /ɨ/ | ~◯ | Retroflex vowel |
| a | /a/ | ~↓ | Open central |
| o | /o/ | ~← | Mid back rounded |
| e | /ɤ/ | ~↖ | Mid back unrounded |
| ê | /ɛ/ | ~↗ | Open-mid front |
| i | /i/ | ~↑ | High front |
| u | /u/ | ~↑↑ | High back rounded |
| ü | /y/ | ~↑↗ | High front rounded |
| ai | /aɪ/ | ~↓~↑ | Diphthong: open→high |
| ei | /eɪ/ | ~→~↑ | Diphthong: mid→high |
| ao | /aʊ/ | ~↓~↖ | Diphthong: open→high+back |
| ou | /oʊ/ | ~←~↑ | Diphthong: back→high |
| an | /an/ | ~↓◯∧ | Vowel + nasal coda |
| en | /ən/ | ~·◯∧ | Schwa + nasal |
| ang | /aŋ/ | ~↓◯◯ | Vowel + velar nasal |
| eng | /əŋ/ | ~·◯◯ | Schwa + velar nasal |
| er | /ɚ/ | ~○ | Rhotacized vowel |

---

## 4. VOWEL SPACE → GEOMETRIC COORDINATES

### 4.1 Formant-to-Point Mapping

Vowel formants (F1, F2) map directly to geometric coordinates:

```
F1 (first formant) ↔ Vertical position
  Low F1 (~250 Hz)  → Top of space (~↑)
  High F1 (~850 Hz) → Bottom of space (~↓)

F2 (second formant) ↔ Horizontal position
  Low F2 (~700 Hz)  → Right/back (~←)
  High F2 (~2300 Hz) → Left/front (~→)

F3 (third formant) ↔ Rounding/lip position
  Lowered F3 → Rounded (~↗, ~↖, ~←)
```

### 4.2 Vowel Space Geometry

```
Geometric Vowel Space:

     ~↑                     ~↑↑
     /i/                    /u/
    High                   High
     Front                Back
      │                      │
      │    ~·                │
      │    /ə/               │
      │                      │
~→ /e/───────~↖ /ɤ/─────~← /o/
      │                      │
      │                      │
     ~↘                    ~↙
     /æ/                   /ɒ/
      │                      │
     ~↓                      ~↓
     /a/───────────────────/ɑ/
```

### 4.3 Example Calculations

**English /i/ ("beat"):**
```
F1 ≈ 280 Hz → y = +0.9 (high)
F2 ≈ 2250 Hz → x = -0.9 (front)
Result: ~↑ (high front)
Glyfinform: Pure upward curve
```

**English /u/ ("boot"):**
```
F1 ≈ 300 Hz → y = +0.9 (high)
F2 ≈ 870 Hz → x = +0.8 (back)
Rounding: + → double-up ~↑↑
Glyfinform: Strong upward curve
```

**English /a/ ("father"):**
```
F1 ≈ 750 Hz → y = -0.8 (low)
F2 ≈ 1200 Hz → x = +0.2 (central)
Result: ~↓ (low)
Glyfinform: Downward curve
```

---

## 5. CONSONANT CLUSTERS

### 5.1 English Clusters

**Initial Clusters:**
| Cluster | Glyfinform | Geometric Composition |
|---------|------------|----------------------|
| /pl/ | ∧~· | Plosive + lateral = Angle-Curve-Point |
| /bl/ | ∧·~· | Voiced plosive + lateral |
| /tr/ | ∧~◯ | Plosive + rhotic = Angle-Curve-Vesica |
| /dr/ | ∧·~◯ | Voiced plosive + rhotic |
| /kr/ | ∧∧~◯ | Velar plosive + rhotic |
| /gr/ | ∧∧·~◯ | Voiced velar + rhotic |
| /fl/ | ─~~· | Fricative + lateral = Line-Curve-Curve-Point |
| /fr/ | ─~~◯ | Fricative + rhotic |
| /θr/ | ──~~◯ | Dental fricative + rhotic |
| /ʃr/ | ≈≈~◯ | Postalveolar + rhotic |
| /sw/ | ≈~↙ | Fricative + glide |
| /tw/ | ∧~↙ | Plosive + glide |
| /kw/ | ∧∧~↙ | Velar plosive + glide |
| /sk/ | ≈∧∧ | Fricative + velar |
| /sp/ | ≈∧ | Fricative + plosive |
| /st/ | ≈∧ | Fricative + plosive |
| /spl/ | ≈∧~· | Triple cluster |
| /spr/ | ≈∧~◯ | Triple cluster |
| /str/ | ≈∧~◯ | Triple cluster |
| /skr/ | ≈∧∧~◯ | Triple cluster |

**Final Clusters:**
| Cluster | Glyfinform | Notes |
|---------|------------|-------|
| /pt/ | ∧∧∧ | Double plosive |
| /kt/ | ∧∧∧ | Double plosive |
| /bd/ | ∧·∧· | Voiced double |
| /gd/ | ∧∧·∧· | Voiced double |
| /ps/ | ∧≈ | Plosive + fricative |
| /ts/ | ∧≈ | Affricate-like |
| /ks/ | ∧∧≈ | Velar + fricative |
| /sp/ | ≈∧ | Unreleased final |
| /st/ | ≈∧ | Unreleased final |
| /sk/ | ≈∧∧ | Unreleased final |
| /lp/ | ~·∧ | Lateral + plosive |
| /rp/ | ~◯∧ | Rhotic + plosive |
| /mp/ | ◯─∧ | Nasal + plosive |
| /nt/ | ◯∧∧ | Nasal + plosive |
| /ŋk/ | ◯◯∧∧ | Velar nasal + plosive |
| /lpt/ | ~·∧∧ | Triple final |
| /rkt/ | ~◯∧∧∧ | Triple final |
| /mpt/ | ◯─∧∧ | Triple final |
| /ŋkt/ | ◯◯∧∧∧ | Triple final |
| /ksts/ | ∧∧≈≈ | Quadruple (sixths) |

### 5.2 Cluster Geometry Principles

```
Cluster Formation Rules:

1. Sequential Composition:
   C1C2 → Glyph(C1) followed by Glyph(C2)
   /tr/ → ∧ followed by ~◯ = ∧~◯

2. Assimilation:
   Place/manner matching → shared components
   /mp/ → ◯─∧ (nasal anticipates plosive place)

3. Simplification:
   Complex clusters → reduced geometric representation
   /ksts/ → ∧∧≈≈ (four → four, but compressed)

4. Syllabification:
   Ambiguous boundaries → void separator
   /extra/ → ─~∧~─∧·─ (e-x-t-r-a with void)
```

---

## 6. PROSODY AS TEMPORAL GEOMETRY

### 6.1 Stress Patterns

**Primary Stress (ˈ):**
```
Effect: Double primitive weight
Visual: Glyph emphasized, bold

Example: ˈrunning = ~~ (Curve emphasized)
          ˈbeautiful = ~~□ (Curve+Square, curve doubled)

Encoding: Fellowship resonance boosted ×2
```

**Secondary Stress (ˌ):**
```
Effect: 1.5× primitive weight
Visual: Glyph slightly emphasized

Example: ˌunderˈstand = ◯~ ∧~~
         (Vesica emphasized 1.5×, Angle+Curve doubled)
```

**Unstressed:**
```
Effect: 0.5× primitive weight
Visual: Glyph reduced
Example: the = ~· (reduced definite article)
```

### 6.2 Intonation Contours

| Pattern | Symbol | Geometric Encoding | Meaning |
|---------|--------|-------------------|---------|
| Falling | ↘ | Descending curve weight | Statement, finality |
| Rising | ↗ | Ascending curve weight | Question, continuation |
| Level | → | Equal weight distribution | Neutral, listing |
| Fall-Rise | ↘↗ | V-shaped weight curve | Reservation, implication |
| Rise-Fall | ↗↘ | Λ-shaped weight curve | Surprise, emphasis |
| High Level | ↑ | Sustained high weight | Excitement, emphasis |
| Low Level | ↓ | Sustained low weight | Boredom, detachment |

**Intonation Examples:**
```
"You came." (statement): ~↑ ◯~─· ↘
"You came?" (question): ~↑ ◯~─· ↗
"You came!" (surprise): ~↑ ◯~─· ↗↘

Geometric: Final glyph modified by intonation vector
```

### 6.3 Rhythm and Timing

**Syllable Timing:**
```
Language Type    → Geometric Spacing
─────────────────────────────────────
Stress-timed     → Variable spacing (~·~─~~)
Syllable-timed   → Uniform spacing (~·~·~·)
Mora-timed       → Weighted spacing (~·~·~~)
```

**Tempo:**
```
Tempo    → Glyph Compression
────────────────────────────
Allegro  → Compressed (~·~· → ~~)
Andante  → Standard (~·~·)
Adagio   → Extended (~∅·∅~∅·)
```

---

## 7. TONE LANGUAGES

### 7.1 Mandarin Tones

| Tone | Pitch | Geometric Modification | Symbol |
|------|-------|----------------------|--------|
| **T1** (High) | 55 | Upper half emphasis | ~↑ |
| **T2** (Rising) | 35 | Ascending curve | ~↗ |
| **T3** (Low/Dip) | 214 | Deep curve with rise | ~↘↗ |
| **T4** (Falling) | 51 | Descending curve | ~↘ |
| **Neutral** | variable | Minimal curve | ~· |

**Tone Examples:**
```
妈 mā (mother) = ◯─~↑
麻 má (hemp) = ◯─~↗
马 mǎ (horse) = ◯─~↘↗
骂 mà (scold) = ◯─~↘
吗 ma (question) = ◯─~·

All share ◯─ (Vesica-Line = "ma" syllable)
Distinguished only by tone geometry
```

### 7.2 Vietnamese Tones

| Tone | Pitch | Geometric Modification | Example |
|------|-------|----------------------|---------|
| **Ngang** (level) | 33 | Level curve | ma ~─ |
| **Huyền** (falling) | 21 | Descending | mà ~↘ |
| **Hỏi** (rising-glottal) | 313 | Curve with break | mả ~↗∧ |
| **Ngã** (rising-glottal) | 35 | Sharp rise | mã ~↗ |
| **Sắc** (rising) | 35 | Ascending | má ~↗ |
| **Nặng** (falling-glottal) | 21 | Sharp fall | mạ ~↘· |

### 7.3 Thai Tones

| Tone | Pitch | Geometric Modification |
|------|-------|----------------------|
| **Mid** | 33 | Level | ~─ |
| **Low** | 21 | Low descent | ~↘ |
| **Falling** | 51 | Steep fall | ~↘↘ |
| **High** | 45 | High level | ~↑ |
| **Rising** | 214 | Rise with dip | ~↘↗ |

### 7.4 Tone Geometry Principles

```
Tone Space as Geometric Field:

  High pitch (+1) ──────────── ~↑
        │                      │
        │                      │
  Mid pitch (0) ────────────── ~─
        │                      │
        │                      │
  Low pitch (-1) ───────────── ~↓
        │                      │
        └──────────────────────┘
        Rising (+)    Falling (-)

Contour tones = curves through this space
Level tones = horizontal lines
```

---

## 8. SUPRASEGMENTALS

### 8.1 Length

| Duration | Symbol | Glyfinform |
|----------|--------|------------|
| Extra-short | ◡ | Reduced (~) |
| Short | ◡ | Base form (~) |
| Half-long | ◑ | Extended (~─) |
| Long | ◐ | Doubled (~~) |
| Extra-long | ◖◗ | Tripled (~~~) |

### 8.2 Aspiration

| Type | Symbol | Glyfinform |
|------|--------|------------|
| Unaspirated | ◌ | Base form (∧) |
| Aspirated | ʰ | Add curve (∧~) |
| Breathy voice | ◌̤ | Add curve (·~) |
| Creaky voice | ◌̰ | Add angle (·∧) |

### 8.3 Phonation Types

| Type | Symbol | Glyfinform |
|------|--------|------------|
| Voiceless | ◌ | No point modifier |
| Voiced | ◌̬ | Add point (·) |
| Murmured | ◌̤ | Add curve (~) |
| Strident | ◌̠ | Add angle (∧) |
| Fortis | ◌̝ | Double base (──) |
| Lenis | ◌̞ | Soften base (~) |

---

## 9. ENCODING SPECIFICATION

### 9.1 Phonetic-to-Glyfinform Algorithm

```rust
/// Convert IPA phonetic string to glyfinform
pub fn phonetic_to_glyfinform(ipa: &str) -> String {
    let mut glyfinform = String::new();
    let phonemes = parse_ipa(ipa);
    
    for phoneme in phonemes {
        let glyph = match phoneme {
            // Plosives
            Phoneme { place: Bilabial, manner: Plosive, voiced: false } => "∧",
            Phoneme { place: Bilabial, manner: Plosive, voiced: true } => "∧·",
            Phoneme { place: Alveolar, manner: Plosive, voiced: false } => "∧",
            Phoneme { place: Alveolar, manner: Plosive, voiced: true } => "∧·",
            Phoneme { place: Velar, manner: Plosive, voiced: false } => "∧∧",
            Phoneme { place: Velar, manner: Plosive, voiced: true } => "∧∧·",
            
            // Nasals
            Phoneme { place: Bilabial, manner: Nasal, .. } => "◯─",
            Phoneme { place: Alveolar, manner: Nasal, .. } => "◯∧",
            Phoneme { place: Velar, manner: Nasal, .. } => "◯◯",
            
            // Fricatives
            Phoneme { manner: Fricative, place: Dental, .. } => "──~",
            Phoneme { manner: Fricative, place: Alveolar, voiced: false } => "≈",
            Phoneme { manner: Fricative, place: Alveolar, voiced: true } => "≈·",
            Phoneme { manner: Fricative, place: Postalveolar, .. } => "≈≈",
            
            // Approximants
            Phoneme { place: Palatal, manner: Approximant, .. } => "~↑",
            Phoneme { place: Labiovelar, manner: Approximant, .. } => "~↙",
            Phoneme { place: Alveolar, manner: Approximant, .. } => "~◯",
            
            // Laterals
            Phoneme { manner: LateralApproximant, .. } => "~·",
            
            // Vowels - based on formants
            Phoneme { category: Vowel, f1, f2, .. } => {
                vowel_to_glyph(f1, f2)
            }
            
            _ => "∅", // Default to void
        };
        
        glyfinform.push_str(glyph);
    }
    
    glyfinform
}

fn vowel_to_glyph(f1: f32, f2: f32) -> &'static str {
    // Map formant frequencies to vowel space
    let height = map_f1_to_height(f1);   // -1.0 (low) to +1.0 (high)
    let backness = map_f2_to_backness(f2); // -1.0 (front) to +1.0 (back)
    
    match (height, backness) {
        (0.8..=1.0, -1.0..=-0.5) => "~↑",    // High front: /i/
        (0.8..=1.0, 0.5..=1.0) => "~↑↑",     // High back: /u/
        (0.0..=0.3, -1.0..=-0.3) => "~→",    // Mid front: /e/
        (0.0..=0.3, 0.3..=1.0) => "~←",      // Mid back: /o/
        (-1.0..=-0.5, -0.5..=0.5) => "~↓",   // Low central: /a/
        _ => "~·",                             // Schwa/default
    }
}
```

### 9.2 Prosody Encoding

```rust
/// Encode prosodic information into LatticeState
pub fn encode_prosody(
    lattice: &mut LatticeState,
    stress: StressLevel,
    tone: Option<Tone>,
    intonation: IntonationContour,
) {
    // Encode stress in fellowship_resonance
    lattice.fellowship_resonance *= match stress {
        StressLevel::Primary => 2.0,
        StressLevel::Secondary => 1.5,
        StressLevel::Unstressed => 0.5,
    };
    
    // Encode tone in vertical coefficients
    if let Some(t) = tone {
        lattice.ternary_junction[3] = match t {
            Tone::High => 1,
            Tone::Rising => 1,
            Tone::Low => -1,
            Tone::Falling => -1,
            Tone::Dipping => 0,
            Tone::Neutral => 0,
        };
    }
    
    // Encode intonation in trajectory
    lattice.phyllotaxis_spiral = match intonation {
        IntonationContour::Falling => -127,
        IntonationContour::Rising => 127,
        IntonationContour::Level => 0,
        IntonationContour::FallRise => -64,
        IntonationContour::RiseFall => 64,
    };
}
```

---

## 10. VALIDATION

### 10.1 Roundtrip Testing

```rust
#[test]
fn test_phonetic_roundtrip() {
    let test_words = vec![
        ("hello", /həˈloʊ/, "~·~·~←"),
        ("world", /wɜːrld/, "~↙~◯─·"),
        ("water", /ˈwɔːtər/, "~↙~←∧~"),
        ("fire", /ˈfaɪər/, "─~·~↗~◯"),
    ];
    
    for (orthographic, ipa, expected_glyph) in test_words {
        let glyph = phonetic_to_glyfinform(ipa);
        assert_eq!(glyph, expected_glyph);
        
        // Decode and verify semantic preservation
        let reconstructed = glyfinform_to_description(&glyph);
        assert!(reconstructed.contains_key_semantics(orthographic));
    }
}
```

### 10.2 Cross-Linguistic Comparison

| Phoneme | English | Spanish | Mandarin | Glyfinform Consistency |
|---------|---------|---------|----------|----------------------|
| /p/ | ∧ | ∧ | ∧ | ✓ Identical |
| /t/ | ∧ | ∧ (dental) | ∧ | ✓ Identical |
| /k/ | ∧∧ | ∧∧ | ∧∧ | ✓ Identical |
| /m/ | ◯─ | ◯─ | ◯─ | ✓ Identical |
| /n/ | ◯∧ | ◯∧ | ◯∧ | ✓ Identical |
| /i/ | ~↑ | ~↑ | ~↑ | ✓ Identical |
| /a/ | ~↓ | ~↓ | ~↓ | ✓ Identical |
| /u/ | ~↑↑ | ~↑↑ | ~↑↑ | ✓ Identical |

---

## 11. REFERENCES

1. IPA Chart (2015) — International Phonetic Association
2. Ladefoged, P. & Johnson, K. (2014) — A Course in Phonetics
3. Catford, J.C. (2001) — A Practical Introduction to Phonetics
4. TRANSEXICON_SPEC.md — English phoneme→glyph mapping
5. GLYF_LEXICONIC_SYSTEM.md — Cross-linguistic alignment

---

*Speech is breath shaped by geometry; phonology is the blueprint of that shaping.*
