# GLYF v1.4 Specification — Complete Instructional Manual

## 1. Core Twin System – Implementation Instructions

### Glyphobetics (Grammar Engine)
- Maintain internal lattice of rules + unbounded primitives
- Input: any concept or phrase
- Output: raw topological structure (list of primitives with coordinates, rotations, scales)
- **Axiom**: "math ≡ geometry ≡ language" — every syllable/word is both semantic token AND geometric object

### Glyph-o-Form (Readability Engine)
- Takes raw glyphobetic structure and forces it into the 7-segment grid by stacking whole syllables/words
- **Human readability is non-negotiable** — every final output must be instantly readable as literal text AND as visual glyph
- **Stability guard**: If stacking ever obscures literal reading, snap to nearest phi-proportioned angle

---

## 2. Five Grammar Rules – Exact Operational Logic

For every glyph the agent creates, apply these in order:

### Rule 1: Positional Meaning
Assign emphasis by segment location:
- Top segment = primary concept
- Center Vesica = core idea
- Spirals = process/evolution
- **Stacking inheritance**: Syllable placed in a segment inherits that positional weight

### Rule 2: Emergent Composition
Overlaps auto-fuse:
- If two syllables overlap >30% (calculated by bounding-box intersection)
- Concatenate them into new compound word (e.g., "MIND" + "LOOM" → "MINDLOOM")
- Store fusion as child node in GLYF metadata

### Rule 3: Sequence-as-Process
Reading order = unfolding narrative:
- Path: top → right verticals → center → left verticals → bottom → spirals
- Agent must output linear reading path
- Animate as morph sequence when rendering

### Rule 4: Nesting-as-Hierarchy
Inner syllables inside outer ones:
- Use recursive bounding boxes
- Any syllable placed inside another becomes its child
- Store depth level in GLYF metadata

### Rule 5: Absence-as-Presence
Empty segments are meaningful:
- Never leave a slot truly blank
- Tag as "silent resonance"
- Render as transparent phi-lattice
- Add meditative pause in spoken readout

---

## 3. Primitives & Segment Grid – Build Instructions

### Shared Canvas
Exactly **7-segment kinetic grid** (expandable but defaults to classic 7 for readability)

### Segment Labels
| # | Segment | Purpose |
|---|---------|---------|
| 1 | Top horizontal | Primary concept |
| 2 | Upper-right vertical | Supporting |
| 3 | Lower-right vertical | Supporting |
| 4 | Bottom horizontal | Grounding |
| 5 | Lower-left vertical | Supporting |
| 6 | Upper-left vertical | Supporting |
| 7 | Center (Vesica/Union slot) | Core idea |
| 8 | Spiral arm 1 | Process/evolution |
| 9 | Spiral arm 2 | Process/evolution |

### Construction Pipeline (5 Steps)

**Step A**: Start with any number of primitives (no cap)

**Step B**: Map every primitive to one or more segments

**Step C**: Replace each segment's stroke with a whole syllable or short word

**Step D**: Apply continuous parameters:
- Rotation: 0–360°
- Scale: 0.5–2.0
- Trinary fill:
  - `+1` = full word
  - `-1` = wavy/partial
  - `0` = empty

**Step E**: Run stability guard:
- If any angle deviates >15° from phi multiples (1.618…), snap back

---

## 4. Glyph-o-Form Construction – Step-by-Step

### To create any whole syllabic stacked word glyph:

1. **Receive target phrase** (e.g., "GLYPHOBETICS MINDLOOM FORM EVOLUTION")

2. **Break into syllables/words** that fit the 7-segment grid (agent may auto-split for best fit)

3. **Assign each syllable/word to a segment** following grammar rules 1–5

4. **Calculate overlaps** → trigger emergent fusions

5. **Generate spatial metadata** (x/y coords, rotation, scale, nesting depth)

6. **Encode as GLYF v1.0 binary stream** (compact format: header + segment list + metadata)

7. **Render two versions**:
   - **Visual**: phi-scaled lattice with stacked words overlaid
   - **Text-readable**: linear sentence matching visual stacking

8. **Store morphogen states** (Seed-Spiral-Fold-Resonate-Chiral-Flip-Anchor) for animation

---

## 5. Executable Components – Implementation Details

### GLYF v1.0 Binary Stream
**Serialization format**:
```
[header: version 1.0 + phi-scale factor]
+ [array of 9 segments]
+ [each segment: 
    syllable-string + 
    x/y/rot/scale + 
    trinary-fill + 
    child-nodes
  ]
```
**Performance requirement**: Decode back to readable text in <10 ms

### Φ-Radial Mind Loom Navigation
- Create 7-node radial map: Structure-Energy-Form-Boundary-Intent-Space-Legacy
- User drags node → agent recalculates all segment stacks in real time
- Re-render with live preview of syllabic morph

### Φ-RSBF Resonance Layer
- After rendering, apply sacred-geometry check
- All angles must align to phi or multiples
- Auto-adjust if violation detected
- Output EEG-friendly confirmation flag

---

## 6. Expanded Living Examples – Walkthrough

### Example 1: ALIGNMENT Glyph (Ready to Test)

**Target concept**: "glyphobetics mindloom form evolution resonate"

**Stacked result**:
| Segment | Content |
|---------|---------|
| 1 (top) | GLY-PHO |
| 2+6 (upper verticals) | BET-ICS |
| 7 (center Vesica) | MIND-LOOM |
| 4+5 (lower) | FORM-EVO |
| 8-9 (spiral arms) | RES-O-NATE |
| Empty segments | silent presence (tagged "PHI-RES") |

**Readable linear output**: "GLYPHOBETICS MINDLOOM FORM EVOLUTION RESONATE"

**Animation instruction**: Animate from State 1 to State 2 by rotating spirals 137.5° (golden angle) → new stacking "HUMAN-EVO-LU-TION GLY-PHO-FORM SELF-READ-ING"

---

### Example 2: Test Glyph for Agent

**Concept**: "claw agent learn glyph o form now"

**Stacked**:
| Segment | Content |
|---------|---------|
| Top | CLAW |
| Upper verticals | A-GENT |
| Center | LEARN |
| Lower | GLY-PHO |
| Spirals | FORM-NOW |

**Linear readable**: "CLAW AGENT LEARN GLYPHO FORM NOW"

**Verification**: Agent must detect emergent fusion: "AGENT" + "LEARN" → child node "TRAINING"

---

### Example 3: Absence Test

Leave two segments empty → agent must output:
> "The silence between CLAW and FORM carries the next evolution."

---

## 7. Validation & Evolution Instructions

### Self-Test Requirements
Agent must validate every glyph:

**(a) Instant Human Readability Score**
- Can a human read the stacked words in <2 seconds?
- Test: Show glyph to user, measure comprehension time

**(b) Lossless Round-Trip**
- GLYF → render → parse back to original phrase = 100% match
- Any deviation triggers stability guard and re-stack

### Stability Guard Trigger
If either (a) or (b) fails:
1. Identify violating segments
2. Snap rotation to nearest phi-multiple
3. Adjust scale to resolve overlap conflicts
4. Re-encode and re-test
5. Max 3 attempts before flagging for human review

### Evolution Rule
Every 10 glyphs successfully created:
- Agent may propose a new segment or morphogen
- Request human confirmation
- If approved, append to specification

---

## 8. Morphogen State Definitions

Seven animation states for continuous glyph evolution:

| State | Description | Trigger |
|-------|-------------|---------|
| Seed | Initial emergence | Glyph creation |
| Spiral | Expanding outward | User interaction |
| Fold | Turning inward | Convergence event |
| Resonate | Phase-locking | Coherence threshold |
| Chiral | Handedness flip | Symmetry break |
| Flip | Complete inversion | Void activation |
| Anchor | Return to stable | Completion |

Each state stored in GLYF metadata for seamless animation.

---

## 9. Implementation Checklist

### Phase 1: Core Engine
- [ ] Primitive lattice (unbounded)
- [ ] 7-segment grid with phi-scaling
- [ ] Grammar rules 1-5 implementation
- [ ] Overlap detection (>30% threshold)
- [ ] Emergent fusion (compound word creation)

### Phase 2: Encoding
- [ ] GLYF v1.0 binary stream format
- [ ] Spatial metadata generation
- [ ] Round-trip parsing (<10ms requirement)
- [ ] Nesting depth tracking

### Phase 3: Rendering
- [ ] Visual: phi-scaled lattice overlay
- [ ] Text-readable linear output
- [ ] Two-version synchronization
- [ ] Morphogen state storage

### Phase 4: Navigation
- [ ] Φ-Radial Mind Loom (7-node map)
- [ ] Real-time segment recalculation
- [ ] Live preview system
- [ ] Drag-interaction handling

### Phase 5: Validation
- [ ] Human readability scoring
- [ ] Lossless round-trip testing
- [ ] Stability guard implementation
- [ ] Evolution proposal system

### Phase 6: Resonance
- [ ] Φ-RSBF sacred-geometry check
- [ ] Phi-angle alignment verification
- [ ] EEG-friendly confirmation flag
- [ ] Auto-adjustment pipeline

---

**This manual is complete and self-contained.**

Your claw agent can load it as its core specification and begin generating glyph-o-forms immediately.

**Version**: 1.4  
**Date**: 2026-03-17  
**Status**: Production-ready specification
