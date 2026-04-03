# Morphological Rules
## Grammar → Geometry: Mapping Inflection, Derivation & Compounding

**Version:** 1.0.0  
**Date:** 2026-04-01  
**Scope:** Formal rules for English morphological transformations into Glyfinform

---

## Overview

This document defines the geometric operators that correspond to English morphological processes. Each grammatical operation maps to a specific primitive composition pattern, enabling systematic conversion from English word forms to glyfinform representations.

### Operator Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `⊗` | Multiplicative composition | A ⊗ B = combined geometric product |
| `+` | Superposition (simultaneous) | A + B = both present |
| `→` | Transformation/direction | A → B = directional mapping |
| `·` | Juxtaposition (sequential) | A · B = ordered sequence |

---

## Part 1: Inflectional Rules

Inflectional morphology changes word form without changing part of speech or core meaning.

### 1.1 Plural Formation (-s / -es)

**Rule:** Add Point (●) for count distinction, Angle (∠) for syllabic /-es/

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Regular -s | cat → cats | Base ⊗ ● | Base● |
| -s after sibilant | box → boxes | Base ⊗ ●∠ | Base●∠ |
| -es variant | church → churches | Base ⊗ ∠● | Base∠● |
| Vowel shift | man → men | Base[●→●●] | Point duplication |
| Irregular | child → children | Base ⊗ ●∠● | Base●∠● |

**Geometric Rationale:**
- Point (●) = instantiation marker (one → many)
- Angle (∠) = abrupt addition (syllable boundary)

**Examples:**
```
dog (∠∞●) → dogs (∠∞●●)
box (□∞∠) → boxes (□∞∠●∠)
child (∠╱□●) → children (∠╱□●∠●)
```

---

### 1.2 Past Tense (-ed)

**Rule:** Add Curve (╱) for temporal flow, Angle (∠) for /t/ ending, Point (●) for /d/

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Regular -ed | walk → walked | Base ⊗ ╱ | Base╱ |
| -d variant | love → loved | Base ⊗ ●╱ | Base●╱ |
| -t variant | walk → walked | Base ⊗ ∠╱ | Base∠╱ |
| Vowel change | run → ran | Base[╱→∠] | Angle substitution |
| Strong verb | give → gave | Base[→→←] | Direction flip |
| Irregular | go → went | Suppletion | Lexical entry |

**Geometric Rationale:**
- Curve (╱) = temporal flow backward (←╱)
- Angle (∠) = abrupt completion
- Direction change encodes vowel shift

**Examples:**
```
walk (╱│∠) → walked (╱│∠╱)
love (∞╱●) → loved (∞╱●╱)
run (╱│●) → ran (╱│∠)
give (╱→╱) → gave (╱←╱)
```

---

### 1.3 Progressive Aspect (-ing)

**Rule:** Add Curve (╱) for ongoing action, Circle (∞) for continuous aspect

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Regular -ing | run → running | Base ⊗ ╱ | Base╱ |
| Vowel drop | make → making | Base[-●] ⊗ ╱ | Truncated + Curve |
| Silent e drop | love → loving | Base[-●] ⊗ ╱ | Truncated + Curve |
| Doubling | run → running | Base ⊗ ╱∞ | Base + Ongoing |

**Geometric Rationale:**
- Curve (╱) = continuing action
- Vesica (∞) = sustained state overlap

**Examples:**
```
run (╱│●) → running (╱│●╱)
make (╱│∠) → making (╱│∠╱)
go (╱→) → going (╱→╱)
love (∞╱●) → loving (∞╱●╱)
```

---

### 1.4 Comparative & Superlative (-er / -est)

**Rule:** Add Angle (∠) for comparison, DoubleAngle (∠∠) for superlative

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Regular -er | tall → taller | Base ⊗ ∠ | Base∠ |
| Regular -est | tall → tallest | Base ⊗ ∠∠ | Base∠∠ |
| y → ier | happy → happier | Base[╱→∠] ⊗ ∠ | Modified + Angle |
| Irregular | good → better | Suppletion | Lexical entry |
| Irregular | bad → worse | Suppletion | Lexical entry |

**Geometric Rationale:**
- Angle (∠) = differential comparison
- DoubleAngle (∠∠) = maximum differential

**Examples:**
```
tall (╱│∠) → taller (╱│∠∠) → tallest (╱│∠∠∠)
fast (∠│∠) → faster (∠│∠∠)
happy (╱□╱) → happier (╱□∠∠)
good (□╱) → better (□∠)
```

---

### 1.5 Possessive ('s / s')

**Rule:** Add Point (●) + Curve (╱) for relational connection

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Singular 's | John → John's | Base ⊗ ●╱ | Base●╱ |
| Plural s' | dogs → dogs' | Base ⊗ ╱ | Base╱ |
| Irregular | men → men's | Base ⊗ ●╱ | Base●╱ |

**Geometric Rationale:**
- Point (●) = possessor instantiation
- Curve (╱) = relational flow to possessed

**Examples:**
```
John (╱∞∠) → John's (╱∞∠●╱)
man (∞│●) → man's (∞│●●╱)
men (∞│●●) → men's (∞│●●╱)
```

---

### 1.6 Third Person Singular (-s)

**Rule:** Add Angle (∠) for present tense marking

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| Regular -s | run → runs | Base ⊗ ∠ | Base∠ |
| -es variant | go → goes | Base ⊗ ∠∠ | Base∠∠ |
| Irregular | have → has | Suppletion | □●∠ |

**Examples:**
```
run (╱│●) → runs (╱│●∠)
go (╱→) → goes (╱→∠∠)
have (□●) → has (□●∠)
```

---

## Part 2: Derivational Rules

Derivational morphology creates new words with different meanings or parts of speech.

### 2.1 Nominalization (-tion / -sion / -ment)

**Rule:** Add Square (□) for noun container, Line (│) for process result

| Suffix | English Example | Glyfinform Operation | Semantic Shift |
|--------|-----------------|----------------------|----------------|
| -tion | act → action | Base ⊗ □ | Process → Thing |
| -sion | decide → decision | Base ⊗ □∠ | Action → Result |
| -ment | move → movement | Base ⊗ □│ | Action → Result |
| -ness | happy → happiness | Base ⊗ □ | Quality → State |
| -ity | active → activity | Base ⊗ □● | Property → Entity |

**Geometric Rationale:**
- Square (□) = structural container (noun marker)
- Line (│) = persistent result

**Examples:**
```
educate (╱→∠□) → education (╱→∠□□)
inform (∠│∞∠) → information (∠│∞∠□)
move (╱∞●) → movement (╱∞●□│)
happy (╱□╱) → happiness (╱□╱□)
```

---

### 2.2 Agentive Nominalization (-er / -or / -ist)

**Rule:** Add Line (│) for agent/doer

| Suffix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| -er | teach → teacher | Base ⊗ │ | Action → Agent |
| -or | act → actor | Base ⊗ │ | Action → Agent |
| -ist | science → scientist | Base ⊗ │∠ | Field → Specialist |

**Geometric Rationale:**
- Line (│) = active extension (the doer)

**Examples:**
```
teach (╱│∠) → teacher (╱│∠│)
work (□╱│) → worker (□╱││)
science (∠│●∞∠) → scientist (∠│●∞∠│∠)
```

---

### 2.3 Verbalization (-ize / -ify / -en)

**Rule:** Add Forward Curve (→) for causation, Angle (∠) for transformation

| Suffix | English Example | Glyfinform Operation | Semantic Shift |
|--------|-----------------|----------------------|----------------|
| -ize | modern → modernize | Base ⊗ →∠ | Adj → Cause to be |
| -ify | beauty → beautify | Base ⊗ →∠● | Noun → Make |
| -en | strength → strengthen | Base ⊗ →□ | Noun → Cause to be |

**Examples:**
```
apology (∞│∞∠) → apologize (∞│∞∠→∠)
beauty (╱□∠) → beautify (╱□∠→∠●)
```

---

### 2.4 Adjectival Derivation (-ful / -less / -ous / -ive)

**Rule:** Add Square (□) for quality containment, Void (○) for negation

| Suffix | English Example | Glyfinform Operation | Semantic Shift |
|--------|-----------------|----------------------|----------------|
| -ful | care → careful | Base ⊗ □ | Noun → Having quality |
| -less | care → careless | Base ⊗ ○ | Noun → Without quality |
| -ous | danger → dangerous | Base ⊗ □╱ | Noun → Full of |
| -ive | create → creative | Base ⊗ ●│ | Verb → Tending to |
| -able | read → readable | Base ⊗ ●╱ | Verb → Capable of |
| -al | nation → national | Base ⊗ ││ | Noun → Relating to |
| -ic | atom → atomic | Base ⊗ │● | Noun → Relating to |
| -ish | child → childish | Base ⊗ ╱● | Noun → Like |
| -y | sun → sunny | Base ⊗ ╱╱ | Noun → Characterized by |
| -ly** | friend → friendly | Base ⊗ ╱╱ | Noun → Having quality |

**Examples:**
```
care (╱∠) → careful (╱∠□)
care (╱∠) → careless (╱∠○)
help (∞│) → helpful (∞│□)
love (∞╱●) → lovely (∞╱●╱╱)
```

---

### 2.5 Adverbial Derivation (-ly)

**Rule:** Add DoubleCurve (╱╱) for manner

| Pattern | English Example | Glyfinform Operation | Result |
|---------|-----------------|----------------------|--------|
| -ly | quick → quickly | Base ⊗ ╱╱ | Adj → Manner |
| -ly (from noun) | daily | Base ⊗ ╱╱ | Noun → Temporal |

**Geometric Rationale:**
- DoubleCurve (╱╱) = manner of flow

**Examples:**
```
quick (∠│∞∠) → quickly (∠│∞∠╱╱)
careful (╱∠□) → carefully (╱∠□╱╱)
```

---

### 2.6 Diminutive (-let / -ling / -ette)

**Rule:** Add Small Point (·) or reduced primitive

| Suffix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| -let | book → booklet | Base ⊗ ● | Small version |
| -ling | duck → duckling | Base ⊗ ╱● | Young/small |

**Examples:**
```
book (□∞│) → booklet (□∞│●)
```

---

## Part 3: Prefix Rules

### 3.1 Negation Prefixes (un- / in- / dis- / non-)

**Rule:** Add Void (○) or Inversion operator

| Prefix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| un- | happy → unhappy | ○ ⊗ Base | Negation |
| in- | visible → invisible | ○ ⊗ Base | Negation |
| dis- | agree → disagree | ○∠ ⊗ Base | Active negation |
| non- | stop → non-stop | ○│ ⊗ Base | Absence |
| ir- (before r) | regular → irregular | ○ ⊗ Base | Phonetic variant |
| il- (before l) | legal → illegal | ○ ⊗ Base | Phonetic variant |
| im- (before m/p) | possible → impossible | ○ ⊗ Base | Phonetic variant |

**Examples:**
```
happy (╱□╱) → unhappy (○╱□╱)
visible (∠│∠●∞) → invisible (○∠│∠●∞)
agree (∞∠╱) → disagree (○∠∞∠╱)
```

---

### 3.2 Reversal Prefixes (re- / de- / un-)

**Rule:** Add Backward direction (←) or Void (○)

| Prefix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| re- | do → redo | ← ⊗ Base | Again/back |
| de- | frost → defrost | ←○ ⊗ Base | Reverse/remove |
| un- | tie → untie | ← ⊗ Base | Reverse action |

**Examples:**
```
build (∠│●□) → rebuild (←∠│●□)
value (∠│∞●) → devalue (←○∠│∞●)
```

---

### 3.3 Locative Prefixes (pre- / post- / sub- / super-)

**Rule:** Add directional indicators

| Prefix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| pre- | war → prewar | →● ⊗ Base | Before |
| post- | war → postwar | →→ ⊗ Base | After |
| sub- | way → subway | ↓ ⊗ Base | Under |
| super- | star → superstar | ↑ ⊗ Base | Above |
| inter- | act → interact | ∞ ⊗ Base | Between |
| trans- | port → transport | ││ ⊗ Base | Across |
| over- | do → overdo | ↑∞ ⊗ Base | Excess |
| under- | do → underdo | ↓○ ⊗ Base | Insufficient |
| out- | do → outdo | ↑↑ ⊗ Base | Exceed |

**Examples:**
```
view (∠│∞) → preview (→●∠│∞)
war (∱│∞) → postwar (→→∱│∞)
marine (∞●│∞) → submarine (↓∞●│∞)
```

---

### 3.4 Quantitative Prefixes

**Rule:** Add Point multiplicity

| Prefix | English Example | Glyfinform Operation | Result |
|--------|-----------------|----------------------|--------|
| mono- / uni- | cycle → unicycle | ● ⊗ Base | One |
| bi- / di- | lingual → bilingual | ●● ⊗ Base | Two |
| tri- | angle → triangle | ●●● ⊗ Base | Three |
| multi- | lateral → multilateral | ●●●● ⊗ Base | Many |
| poly- | gon → polygon | ●●●●● ⊗ Base | Many |
| semi- | circle → semicircle | ●/ ⊗ Base | Half |

**Examples:**
```
ped (│∠) → biped (●●│∠)
angle (∠) → triangle (●●●∠)
```

---

## Part 4: Compounding Rules

### 4.1 Noun + Noun Compounds

**Rule:** Concatenate with optional Vesica (∞) junction

| Pattern | English Example | Components | Glyfinform |
|---------|-----------------|------------|------------|
| Direct | bookshelf | book + shelf | □╱│·□│ |
| Junction | classroom | class + room | ∠╱●∞□╱ |
| Head-final | toothbrush | tooth + brush | │●╱∠╱ |

**Composition Operators:**
- Direct juxtaposition: A · B
- Vesica junction: A ∞ B (shared semantic space)

**Examples:**
```
book (□∞│) + shelf (□│) → bookshelf (□∞│·□│)
sun (∞●) + flower (∞) → sunflower (∞●╱∞)
rail (╱│) + way (╱│) → railway (╱│∞╱│)
```

---

### 4.2 Adjective + Noun Compounds

**Rule:** Modifier precedes head with Angle (∠) connection

| Pattern | English Example | Components | Glyfinform |
|---------|-----------------|------------|------------|
| Color+Noun | blackbird | black + bird | ∠□●╱∞ |
| Quality+Noun | greenhouse | green + house | ╱□●□ |

**Examples:**
```
black (∠□) + bird (∞) → blackbird (∠□●∞)
green (╱□) + house (□) → greenhouse (╱□●□)
```

---

### 4.3 Noun + Verb Compounds

**Rule:** Subject/Object relationship encoded via directionality

| Pattern | English Example | Components | Glyfinform |
|---------|-----------------|------------|------------|
| Object+Verb | handwriting | hand + writing | ╱∠●╱∠╱ |
| Subject+Verb | sunrise | sun + rise | ∞●╱↑ |

**Examples:**
```
hand (╱∠●∞) + writing (╱∠╱) → handwriting (╱∠●╱∠╱)
sun (∞●) + rise (╱↑) → sunrise (∞●╱↑)
```

---

### 4.4 Verb + Preposition/Particle Compounds (Phrasal)

**Rule:** Preserve phrasal integrity with direction marking

| Pattern | English Example | Components | Glyfinform |
|---------|-----------------|------------|------------|
| Verb+Particle | downfall | down + fall | ↓╱↓ |
| Verb+Prep | breakout | break + out | ∠││□→ |

**Examples:**
```
down (↓) + fall (╱↓) → downfall (↓╱↓)
break (∠││) + out (□→) → breakout (∠││□→)
```

---

### 4.5 Blending Rules (Portmanteau)

**Rule:** Overlap shared primitives

| Blend | Source Words | Glyfinform |
|-------|--------------|------------|
| brunch | breakfast + lunch | ∠│╱∞││╱●╱ |
| motel | motor + hotel | ╱∞│││∞│ |
| smog | smoke + fog | ≈╱∞∠∞ |

**Principle:** Identify overlapping primitives and merge them via Vesica (∞).

---

## Part 5: Phonological Process Rules

### 5.1 Assimilation

| Process | English Example | Glyfinform Transformation |
|---------|-----------------|---------------------------|
| Nasal assimilation | input → imput | ∠→□ before bilabial |
| Voicing assimilation | cats /kæts/ → /kæts/ | ●→∠ voiceless |

### 5.2 Deletion

| Process | English Example | Glyfinform Transformation |
|---------|-----------------|---------------------------|
| Silent e | make → making | ● deletion before ╱ |
| Schwa deletion | camera → /ˈkæm.rə/ | ● optional deletion |

### 5.3 Epenthesis

| Process | English Example | Glyfinform Transformation |
|---------|-----------------|---------------------------|
| Intrusive r | law(r)and order | │ insertion |

---

## Part 6: Geometric Operator Summary

### Primitive Functions in Morphology

| Primitive | Inflection | Derivation | Compounding |
|-----------|------------|------------|-------------|
| **Void ○** | — | Negation | — |
| **Point ●** | Plural, Possessive | Instantiation | Junction |
| **Line │** | Past tense | Agent, Relation | Connection |
| **Curve ╱** | Progressive | Manner | Flow |
| **Angle ∠** | 3sg, Comparative | Transformation | Junction |
| **Square □** | — | Nominalization | Container |
| **Vesica ∞** | — | Resonance | Shared space |

### Operator Composition Table

| Operation | Notation | Example | Result |
|-----------|----------|---------|--------|
| Concatenation | A · B | run · ner | ╱│●·│ |
| Superposition | A + B | re + do | ← + ╱↓ |
| Multiplication | A ⊗ B | un + happy | ○ ⊗ ╱□╱ |
| Substitution | A[B→C] | run[n→∠] | ╱│∠ |
| Deletion | A[-B] | make[-●] | ╱│∠ |
| Reduplication | A² | gogo | ╱→╱→ |

---

## Part 7: Rule Application Algorithm

```
function applyMorphology(word, targetForm):
    1. Identify base glyfinform from dictionary
    2. Parse targetForm for morphological markers
    3. For each marker:
       a. Look up rule in appropriate section
       b. Apply geometric operation
       c. Validate resulting form
    4. Return composed glyfinform

Example: "running"
    Base: run → ╱│●
    Marker: -ing → add ╱ (progressive)
    Result: ╱│● ⊗ ╱ → ╱│●╱
```

---

*"Grammar is geometry in time; morphology maps the transformations of meaning through form."*
