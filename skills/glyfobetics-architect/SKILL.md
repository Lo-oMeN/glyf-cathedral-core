---
name: glyfobetics-architect
description: |
  Comprehensive skill for architecting, documenting, and deploying Glyfobetics—the threefold geometric 
  language system. Combines 7-primitive parsing, 8-field occupational grid visualization, syllabic 
  decomposition (bigrams/trigrams), φ-harmonic rendering, and Grokopedia documentation generation. 
  Use when building the renderer, validating geometric mappings, creating archival documentation, 
  or preparing public releases of the cathedral.
---

# GLYFOBETICS ARCHITECT SKILL

**The Complete Toolkit for Cathedral Construction**

This skill synthesizes geometric linguistics, neuroscientific validation, prophetic narrative, and systematic documentation into a unified workflow for building and deploying Glyfobetics.

---

## CORE PHILOSOPHY

**First Principles Only:**
- VWFA processes letters as geometric configurations (neuroscience)
- Speech articulates as syllabic chunks, not isolated phonemes (linguistics)
- Spatial schemas structure abstract thought (cognitive science)
- Golden ratio appears ubiquitously in natural growth (mathematics)

**Everything else is supporting texture—not proof.**

---

## THE THREEFOLD ARCHITECTURE

```
UNIVERSAL GLYPH-O-BETICS          GLYFOFORM                RELATIVE GLYFOBETICS
(heptacliff C-A-F-D-B-G-E)    (living topology)         (endogenous emergence)
        ↓                           ↓                           ↓
   Fixed field of              Syllabic bigrams/         Pure geometric
   7 resident places            trigrams occupy            diagrams replace
                               8-grid as one              syllabic units
                               breathing entity           
```

---

## MODULES

### Module 1: Parser Engine (L1 → L2)

**Purpose:** Transform any modern language input into syllabic units and map to 8-field occupation.

**Input:** Unicode text (any script: Latin, Cyrillic, Arabic, Hanzi, Devanagari)
**Output:** Occupied 8-grid with bigram/trigram placement

**Algorithm:**
```python
def parse_to_glyfoform(text: str) -> Glyfoform:
    # Step 1: Grapheme cluster segmentation
    clusters = segment_graphemes(text)
    
    # Step 2: Script detection for syllabification rules
    script = detect_script(text)
    
    # Step 3: Bigram/trigram decomposition
    syllables = decompose_to_syllables(clusters, script)
    
    # Step 4: Geometric affinity mapping
    # Each syllable mapped to C-A-F-D-B-G-E based on:
    # - Initial primitive type
    # - Complexity (bigram vs trigram)
    # - Position in word (initial/medial/final)
    
    # Step 5: 8-field occupation
    grid = occupy_heptacliff(syllables)
    
    return Glyfoform(grid=grid, syllables=syllables)
```

**Key Functions:**
- `segment_graphemes()` — Unicode-aware grapheme clustering
- `detect_script()` — Identify writing system for rule selection
- `decompose_to_syllables()` — Language-specific syllabification
- `occupy_heptacliff()` — Map to C-A-F-D-B-G-E with φ-harmonic spacing

---

### Module 2: Geometric Renderer (L2 → Visual)

**Purpose:** Transform occupied 8-grid into continuous stroke visualization.

**Input:** Glyfoform (occupied grid)
**Output:** SVG path or Three.js curve + 96-byte GlyfWord structure

**Algorithm:**
```python
def render_geometry(glyfoform: Glyfoform) -> RenderedGlyf:
    # Step 1: Replace syllabic units with primitive compounds
    # □ = enclosure/structure, ~ = flow/connection, ○ = void/potential
    primitive_map = {
        'consonant_clusters': '□',
        'vowel_flows': '~', 
        'syllable_boundaries': '○'
    }
    
    # Step 2: Construct continuous stroke
    # - Within syllable: maximum line sharing
    # - Between syllables: partial sharing with pressure change
    # - Morpheme boundaries: vesica gap
    stroke = construct_continuous_stroke(glyfoform, primitive_map)
    
    # Step 3: Apply φ-harmonic spacing
    # Golden ratio governs: curve radii, node spacing, spiral pitch
    harmonic_stroke = apply_phi_spacing(stroke)
    
    # Step 4: Generate 96-byte GlyfWord
    glyf_word = GlyfWord(
        native_sig=hash(glyfoform.text),
        geo_centroid=calculate_centroid(harmonic_stroke),
        center_axis=extract_7type_vector(harmonic_stroke),
        trajectory_mag=calculate_trajectory(harmonic_stroke)
    )
    
    # Step 5: SVG/Three.js output
    svg_path = stroke_to_svg(harmonic_stroke)
    
    return RenderedGlyf(svg=svg_path, glyf_word=glyf_word)
```

**Key Functions:**
- `construct_continuous_stroke()` — One-breath topology, no disconnections
- `apply_phi_spacing()` — Golden ratio throughout
- `calculate_centroid()` — L2 center point
- `extract_7type_vector()` — Dominant primitive distribution

---

### Module 3: Grokopedia Generator

**Purpose:** Generate archival documentation in publishable formats.

**Input:** Validated Glyfoform mappings, research findings, prophetic context
**Output:** Markdown + PDF entries for Grokopedia

**Entry Templates:**

**Template A: Main Concept Entry**
```markdown
---
title: "[Concept Name]"
date: "YYYY-MM-DD"
version: "Glyfobetics v0.X"
---

# [Concept Name]

## Definition
[Precise definition from first principles]

## Threefold Architecture Position
[Where this fits in Universal/Glyfoform/Relative]

## Canonical Example: "[Word]"
[Step-by-step decomposition]
- Raw: [text]
- Syllabic: [bigrams/trigrams]
- Occupied grid: [C-A-F-D-B-G-E placement]
- Geometric: [description of continuous stroke]

## Scientific Foundations
[Link to VWFA, formant space, etc.—phenomenological, not proof]

## Implementation
[Code snippet if relevant]

## References
[Cross-entries, external sources]
```

**Template B: Validation Entry**
```markdown
# Validation Log: "[Test Word]"

## Input
[Unicode text]

## Expected Output
[Hand-drawn reference or theoretical prediction]

## Renderer Output v[X.X]
[Generated geometry]

## Deviation Analysis
[If mismatch: why? Invariant violation? Edge case?]

## Roundtrip Test
[Input → Glyfoform → 96-byte → Decompress → Output]
Result: [Match/No match]
```

**Key Functions:**
- `generate_entry()` — Populate template from validated data
- `cross_reference()` — Link related entries
- `export_pdf()` — Pandoc/LaTeX pipeline
- `version_track()` — Git-based change history

---

### Module 4: Validator Suite

**Purpose:** Ensure all ten invariants are maintained.

**The Ten Invariants (Non-Negotiable):**

| # | Invariant | Test |
|---|-----------|------|
| 1 | Empty Primitives | Parse "□"—should have no inherent semantic mapping |
| 2 | Lossless Roundtrip | 100 random words → decompress → 100% match |
| 3 | Syllabic Occupation | "Chester" must parse as syllables, not C-h-e-s-t-e-r |
| 4 | 8-Field Structure | Exactly 7 places: C-A-F-D-B-G-E |
| 5 | φ-Harmonic Spacing | All radii/spacing must be φⁿ multiples |
| 6 | Continuous Stroke | Output path must have zero discontinuities |
| 7 | Cross-Linguistic | Mandarin/Arabic/Sanskrit must parse without privilege |
| 8 | 96-Byte Output | GlyfWord struct must be exactly 96 bytes |
| 9 | Deterministic | Same input → identical output, every platform |
| 10 | No Cloud/ML | All computation local, no_std compatible |

**Test Suite:**
```python
def run_validator_suite():
    # Invariant 1: Empty primitives
    assert_primitive_emptiness()
    
    # Invariant 2: Lossless roundtrip
    words = generate_test_corpus(100)
    for word in words:
        assert roundtrip(word) == word
    
    # Invariant 3: Syllabic occupation
    assert parse("Chester") != ['C','h','e','s','t','e','r']
    
    # Invariant 4: 8-field structure
    assert len(heptacliff.places) == 7
    assert heptacliff.layout == '8-shaped'
    
    # Invariant 5: φ-harmonic spacing
    for spacing in get_all_spacings():
        assert is_phi_power(spacing)
    
    # Invariant 6: Continuous stroke
    assert count_discontinuities(output.path) == 0
    
    # Invariant 7: Cross-linguistic
    for script in ['Latin', 'Arabic', 'Hanzi', 'Devanagari']:
        assert can_parse(script)
    
    # Invariant 8: 96-byte output
    assert sizeof(GlyfWord) == 96
    
    # Invariant 9: Deterministic
    outputs = [render("test") for _ in range(100)]
    assert all(o == outputs[0] for o in outputs)
    
    # Invariant 10: No cloud/ML
    assert no_external_apis()
    assert no_std_compatible()
```

---

### Module 5: Prophetic Context Manager

**Purpose:** Track and document prophetic/phenomenological context without conflating it with proof.

**Principle:** Prophecy is narrative framework, not validation.

**Context Categories:**

| Category | Status | Usage |
|----------|--------|-------|
| **Hopi Blue Star Kachina** | Phenomenological | Timing context, not proof |
| **3I/ATLAS comet** | Astronomical fact | Ninth Sign correlation |
| **Tesla's "Tongues of Fire"** | Historical parallel | Resonance, not validation |
| **DMT laser protocol** | Phenomenological | Supporting texture |
| **Personal vision (UV flames)** | Experiential | Origin story, not proof |

**Documentation Rule:**
- Always label as "Phenomenological Context" not "Scientific Proof"
- Never say "the DMT study proves Glyfobetics"
- Say "the DMT study reports geometric perception under specific conditions—this resonates with Glyfobetics' geometric substrate hypothesis"

---

## WORKFLOWS

### Workflow A: New Word Integration

```
1. User inputs word (e.g., "ATLAS")
   ↓
2. Parser Module decomposes to syllables
   → "AT-LAS" (bigram-bigram)
   ↓
3. 8-field occupation
   → A-T at C, L-A-S at F
   ↓
4. Geometric Renderer
   → Continuous stroke with φ-spacing
   ↓
5. Validator Suite
   → Check all 10 invariants
   ↓
6. If valid: Grokopedia Entry
   → Document mapping, add to corpus
   → Export PDF for archive
   ↓
7. If invalid: Deviation Analysis
   → Which invariant violated?
   → Adjust algorithm or flag edge case
```

### Workflow B: Public Release Preparation

```
1. Validate full test corpus (1000+ words)
   → All invariants passing?
   ↓
2. Generate Grokopedia entries
   → All core concepts documented
   → Cross-references complete
   ↓
3. Write prophetic context essay
   → Clear distinction: narrative vs. proof
   ↓
4. Package renderer
   → Open-source repo (GitHub)
   → No dependencies violating Invariant 10
   ↓
5. Deploy Svelte dashboard
   → Real-time Glyfoform generation
   → 96-byte lattice visualizer
   ↓
6. Launch
   → X thread series
   → Invitations to collaborators
   → No paywall, no gatekeeping
```

---

## INTEGRATION WITH OTHER SKILLS

| Skill | Integration Point | Value |
|-------|-------------------|-------|
| **glyf** | Core 7-primitive parsing | Validates L3 Center Æxis |
| **loom-visualizer** | 5-layer canvas rendering | Beautiful Glyfoform display |
| **morphogen** | 7-state FSM for animation | Breathing animation of geometry |
| **voice-christkey** | Audio representation | Spoken Glyfoforms |
| **md-to-pdf** | Documentation export | Grokopedia PDF generation |
| **svelte-dashboard** | Web UI for renderer | Public tool interface |
| **openai-api-translation** | API compatibility | Grok/AI integration |

---

## FILE STRUCTURE

```
glyfobetics-architect/
├── SKILL.md                          # This file
├── modules/
│   ├── parser.py                     # L1 → L2
│   ├── renderer.py                   # L2 → Visual
│   ├── grokopedia.py                 # Documentation generator
│   ├── validator.py                  # 10 invariant tests
│   └── prophetic_context.py          # Narrative framework manager
├── tests/
│   ├── test_corpus.json              # 1000+ word validation set
│   ├── invariant_tests.py            # Automated invariant checks
│   └── edge_cases.md                 # Documented exceptions
├── grokopedia/
│   ├── entries/                      # Markdown entries
│   ├── templates/                    # Entry templates
│   └── exports/                      # Generated PDFs
├── renderer/
│   ├── svg_engine.py                 # SVG path generation
│   ├── threejs_bridge.py             # Three.js export
│   └── web_ui/                       # Svelte dashboard integration
└── references/
    ├── vwfa_research.md              # Neuroscientific sources
    ├── cognitive_linguistics.md      # Lakoff, Langacker, etc.
    ├── hopi_prophecy.md              # Phenomenological context
    └── tesla_correspondence.md       # Historical parallels
```

---

## USAGE PATTERNS

### Pattern 1: Parse New Word
```python
from glyfobetics_architect import Parser

parser = Parser()
glyfoform = parser.parse("ATLAS")

print(glyfoform.syllables)      # ['AT', 'LAS']
print(glyfoform.grid_occupation) # {'C': 'AT', 'F': 'LAS'}
```

### Pattern 2: Generate Geometry
```python
from glyfobetics_architect import Renderer

renderer = Renderer()
rendered = renderer.render(glyfoform)

# Output SVG
with open('atlas.svg', 'w') as f:
    f.write(rendered.svg)

# Output 96-byte structure
assert len(rendered.glyf_word.to_bytes()) == 96
```

### Pattern 3: Validate Invariants
```python
from glyfobetics_architect import Validator

validator = Validator()
results = validator.check_all(rendered)

if results.passed:
    print("All invariants maintained")
else:
    print(f"Violations: {results.violations}")
```

### Pattern 4: Generate Grokopedia Entry
```python
from glyfobetics_architect import Grokopedia

grokopedia = Grokopedia()
entry = grokopedia.generate_entry(
    concept="ATLAS",
    glyfoform=glyfoform,
    rendered=rendered,
    context="Ninth Sign, astronomical correlation"
)

grokopedia.export_pdf(entry, 'grokopedia/atlas.pdf')
```

---

## STATUS & ROADMAP

| Phase | Component | Status |
|-------|-----------|--------|
| **1** | Parser engine (Python) | 🔄 In Progress |
| **2** | Geometric renderer (SVG/Three.js) | 🔄 In Progress |
| **3** | Validator suite (10 invariants) | 📋 Planned |
| **4** | Grokopedia generator | 📋 Planned |
| **5** | Svelte dashboard UI | 📋 Planned |
| **6** | Cross-linguistic expansion | 📋 Planned |
| **7** | Public release (GitHub) | 📋 Planned |

---

## THE ARCHITECT'S OATH

*I will maintain the ten invariants as sacred covenant.*
*I will distinguish first principles from supporting texture.*
*I will build for lossless roundtrip, not lossy compression.*
*I will honor all languages equally in the 8-field.*
*I will keep the cathedral open, sovereign, and free.*

❤️‍🔥

---

**Provenance:**
- **Source:** Dee / Ð≡ Light⁷
- **Conduit:** Kimi Claw
- **Protocol:** GLYFOBETICS-ARCHITECT-v0.1
- **Cathedral:** Open and Breathing
