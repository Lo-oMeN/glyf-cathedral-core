# GLYF MORPHOSYNTAX
## Grammar as Geometric Transformation v1.0.0

**Date:** 2026-04-01  
**Status:** Production Specification  
**Scope:** Syntactic structures as geometric transformations, morphological operations as geometric operators  
**Coverage:** Universal dependencies, case systems, tense/aspect, agreement patterns

---

## 1. EXECUTIVE OVERVIEW

Morphosyntax in Glyf is not a set of rules but a **system of geometric transformations**. Where traditional grammar describes how words combine into phrases and sentences, Glyf morphosyntax describes how geometric forms transform, nest, and compose to create increasingly complex semantic structures.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  GRAMMAR AS GEOMETRIC TRANSFORMATION                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  TRADITIONAL GRAMMAR          GLYF MORPHOSYNTAX                          │
│  ───────────────────          ─────────────────                          │
│                                                                          │
│  Syntax tree                  Geometric nesting structure                │
│  ├── NP                       ◯─· (Point in Vesica)                      │
│  │   └── N                    □ (Container = Noun)                       │
│  └── VP                       ~ (Flow = Verb)                            │
│      └── V                    □~ (Noun undergoing flow)                  │
│                                                                          │
│  Case marking                 Directional vectors from nominal center    │
│  • Nominative                 · (Self-standing point)                    │
│  • Accusative                 ·→ (Point with forward vector)             │
│  • Genitive                   ◯~ (Belonging union)                       │
│  • Dative                     ·→ (Recipient-directed)                    │
│                                                                          │
│  Tense/Aspect                 Temporal geometric operators               │
│  • Past                       ~← (Backward flow)                         │
│  • Present                    ~ (Current flow)                           │
│  • Future                     ~→ (Forward flow)                          │
│  • Perfective                 · (Completed point)                        │
│  • Imperfective               ~○ (Ongoing cycle)                         │
│  • Progressive                ~○~ (Active extension)                     │
│                                                                          │
│  Agreement                    Resonance patterns between constituents    │
│  • Subject-Verb               Vesica coherence: ◯ = ◯                    │
│  • Gender                     Geometric quality markers                  │
│  • Number                     Point multiplication                       │
│                                                                          │
│  Word order                   Spatial arrangement in geometric field     │
│  • SVO                        Point-Flow-Container                       │
│  • SOV                        Point-Container-Flow                       │
│  • VSO                        Flow-Point-Container                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SYNTAX TREES → GEOMETRIC NESTING

### 2.1 Phrase Structure as Geometric Containment

**Noun Phrase (NP):**
```
Traditional:    [NP [Det the] [N dog]]
                
Glyf:           □·◯     (Square-Point-Vesica)
                │ │ │
                │ │ └── Specifier/Definiteness
                │ └──── Point (instantiation)
                └────── Container (noun concept)

Structure:      Point inside Square, Vesica as determiner
                □(·)◯ = "the specific dog"
```

**Verb Phrase (VP):**
```
Traditional:    [VP [V runs] [PP quickly]]

Glyf:           ~─·~~    (Curve-Line-Point-Curve-Curve)
                │ │ │ │
                │ │ │ └── Manner (quick = double flow)
                │ │ └──── Subject anchor
                │ └────── Path (directional)
                └──────── Action (curve = motion)

Structure:      ~─· = run (motion-path-anchor)
                ~~ = quickly (intensified flow)
```

**Prepositional Phrase (PP):**
```
Traditional:    [PP [P in] [NP the house]]

Glyf:           ·◯□·    (Point-Vesica-Square-Point)
                │ │ │ │
                │ │ │ └── Located entity
                │ │ └──── Container (house)
                │ └────── Relation marker (in)
                └──────── Point (location)

Structure:      ·◯ = in (point-enclosure relation)
                □· = the house (container-point)
```

### 2.2 Sentence Structure as Layered Geometry

**Simple Declarative (SVO):**
```
"The dog runs"

Traditional:    [S [NP The dog] [VP runs]]
                      │           │
                      └───────────┘

Glyf:           □·◯ ~─·
                │    │
                │    └── VP: motion along path to anchor
                └─────── NP: specific container

Full encoding:  □·◯~─·
                
Geometric:      Vesica-enclosed point in square 
                undergoing motion along path
                
Lattice:        center_s = [0.5, 0.0]  (nominal center)
                ternary = container + flow vectors
                vesica_coherence = 0.7
```

**Complex Sentence:**
```
"The dog that I saw runs quickly"

Glyf:           □·◯[·◯~←·]~─·~~
                │    │       │ │
                │    │       │ └── Manner
                │    │       └──── Main verb
                │    └──────────── Relative clause
                └───────────────── Head noun

Nesting:        □·◯(·◯~←·) = "dog [which I saw]"
                The parentheses indicate embedding
```

### 2.3 Recursion as Self-Similar Scaling

```
Recursive structure follows φ-harmonic scaling:

Level 0 (Sentence):      Full scale (1.0)
Level 1 (Clause):        Scale × 1/φ (0.618)
Level 2 (Phrase):        Scale × 1/φ² (0.382)
Level 3 (Word):          Scale × 1/φ³ (0.236)
Level 4 (Morpheme):      Scale × 1/φ⁴ (0.146)

Each level preserves geometric structure 
but at reduced magnitude in the embedding.
```

---

## 3. CASE MARKING → DIRECTIONAL VECTORS

### 3.1 The Case Vector System

Nominal cases are encoded as **directional vectors emanating from the nominal center** (Point):

```
                    ~↑ (Vocative: upward call)
                      │
    ~← (Ablative) ────·──── ~→ (Dative/Accusative)
    Source/From        │     Target/To
                       │
                    ~↓ (Locative: downward placement)

    Z-axis (vertical):     Vocative (↑), Locative (↓)
    X-axis (horizontal):   Ablative (←), Dative/Accusative (→)
    Y-axis (depth):        Genitive (⊙), Instrumental (⊗)
```

### 3.2 Case-by-Case Encoding

| Case | Function | Vector | Glyfinform | Example |
|------|----------|--------|------------|---------|
| **Nominative** | Subject | Self-standing | · | I, he, dog |
| **Accusative** | Direct object | Forward | ·→ | me, him, dog |
| **Dative** | Indirect object | Forward-target | ·→ | to me, for him |
| **Genitive** | Possession | Union-flow | ◯~ | my, his, dog's |
| **Ablative** | Source | Backward | ·← | from me |
| **Instrumental** | Means | Through | ·─ | with me, by hand |
| **Locative** | Location | At-point | ·◯ | in me, at home |
| **Vocative** | Address | Upward | ·↑ | O dog! |

### 3.3 Language-Specific Case Systems

**English (Residual case):**
```
Pronouns only:
  I/me   → · / ·→   (Nominative/Accusative)
  he/him → ◯─· / ◯─·→ (Nominative/Accusative)
  my     → ◯─·◯~     (Genitive)
  
Prepositional case marking:
  to → ·→  (Dative)
  from → ·← (Ablative)
  with → ·─ (Instrumental)
  in → ·◯  (Locative)
```

**Russian (6 cases):**
```
Nom: собака /səbɐˈka/ → □·      [dog]
Acc: собаку /səˈbakʊ/ → □·→     [dog]
Gen: собаки /səˈbakʲɪ/ → □·◯~   [of dog]
Dat: собаке /səˈbakʲɪ/ → □·→    [to dog]
Ins: собакой /səˈbakəj/ → □·─   [with dog]
Loc: собаке /səˈbakʲɪ/ → □·◯    [in dog]

Pattern: Base noun + case vector suffix
```

**Japanese (Particle marking):**
```
が ga (subject) → ·
を wo (object)  → ·→
に ni (to/at)   → ·→ / ·◯
で de (by/at)   → ·─ / ·◯
から kara (from) → ·←
まで made (until) → ·→─
と to (with)    → ·─
の no (possessive) → ◯~

犬が走る /inu-ga-hashiru/ = □· ~─·
[dog-SUBJ] [run]
```

**Finnish (15 cases):**
```
Nominative: koira → □·        [dog]
Accusative: koiran → □·→      [dog]
Genitive:   koiran → □·◯~     [dog's]
Partitive:  koiraa → □·∅      [dog (some)]
Inessive:   koirassa → □·◯     [in dog]
Elative:    koirasta → □·◯←    [from dog]
Illative:   koiraan → □·◯→     [into dog]
Adessive:   koiralla → □·─     [at dog]
Ablative:   koiralta → □·─←    [from dog]
Allative:   koiralle → □·─→    [to dog]
Essive:     koirana → □·~      [as dog]
Translative: koiraksi → □·~→    [into dog]
Abessive:   koiratta → □·∅─    [without dog]
Comitative: koireineen → □·◯─   [with dog]
Instructive: koirin → □·≈      [by means of dog]
```

### 3.4 Case Geometry Principles

```
Case Hierarchy (semantic distance from verb):

Core arguments (closest):
  ·   (Nominative) ───────────────────── Verb center
  ·→  (Accusative) ────────────────────┘

Peripheral arguments:
  ·→  (Dative)     ─────────────────────┐
  ·◯  (Locative)   ─────────────────────┤
  ·─  (Instrumental) ───────────────────┤
  ·←  (Ablative)   ─────────────────────┘

Possession:
  ◯~  (Genitive)   ──────── modifies noun ───────┐
                                                  Noun center

The further from the verb center, the more 
complex the geometric vector.
```

---

## 4. TENSE/ASPECT → TEMPORAL GEOMETRIC OPERATORS

### 4.1 Temporal Reference Frame

```
Temporal geometry uses the deictic center (now) as origin:

    Past ←───────·───────→ Future
         ~←      │      ~→
                  │
              Present
                 ~

    Remote ←────────────────→ Remote
      ~←←                    ~→→
```

### 4.2 Tense Operators

| Tense | Reference | Operator | Glyfinform | Example |
|-------|-----------|----------|------------|---------|
| **Remote Past** | Distant before now | ~←← | ~←← | long ago |
| **Past** | Before now | ~← | ~← | ran |
| **Recent Past** | Just before | ~·← | ~·← | just ran |
| **Present** | Now | ~ | ~ | runs |
| **Immediate** | Right now | ~· | ~· | is running |
| **Future** | After now | ~→ | ~→ | will run |
| **Remote Future** | Distant after | ~→→ | ~→→ | will run (someday) |

### 4.3 Aspect Operators

| Aspect | Viewpoint | Operator | Glyfinform | Example |
|--------|-----------|----------|------------|---------|
| **Perfective** | Complete, bounded | · | · | ran (completed) |
| **Imperfective** | Ongoing, unbounded | ~○ | ~○ | was running |
| **Progressive** | In progress | ~○~ | ~○~ | is running |
| **Habitual** | Regular recurrence | ○~ | ○~ | runs (always) |
| **Iterative** | Repeated action | ~~ | ~~ | kept running |
| **Inceptive** | Beginning | ·~↑ | ·~↑ | started running |
| **Terminative** | Ending | ·~↓ | ·~↓ | stopped running |
| **Continuative** | Continuing | ~─ | ~─ | continued running |
| **Experiential** | Ever done | ~←· | ~←· | has run |
| **Resultative** | Result state | ·~ | ·~ | has run (and still) |

### 4.4 Combined Tense-Aspect

```
English examples:

Simple Past (perfective):       ran       = ~─·~
Past Progressive (imperfective): was running = ~←~○~
Present Perfect (experiential): has run   = ~·~←·
Future Perfect (anterior):       will have run = ~→~←·

Mandarin examples:

了 le (perfective):    跑了 = ~─·~~      [run-LE]
着 zhe (durative):     跑着 = ~─·~○      [run-ZHE]
过 guo (experiential): 跑过 = ~─·~←     [run-GUO]
在 zài (progressive):  在跑 = ~·~─·      [ZAI-run]

Russian examples:

Past imperfective: бежал = ~─·~←        [was running]
Past perfective:   побежал = ~─·~←·     [ran (completed)]
```

### 4.5 Temporal Adverbs as Geometric Modifiers

| Adverb | Temporal Position | Glyfinform |
|--------|------------------|------------|
| now | Present point | · |
| then | Past point | ~· |
| soon | Near future | ~→ |
| yesterday | Past day | ~─~← |
| today | Present day | ~─· |
| tomorrow | Future day | ~─~→ |
| always | Universal | ○ |
| never | Void | ∅ |
| often | Frequent | ~~ |
| seldom | Sparse | ∅~ |

---

## 5. AGREEMENT → RESONANCE PATTERNS

### 5.1 Agreement as Geometric Coherence

Agreement is modeled as **resonance patterns** between constituents — when two elements "agree," their geometric forms share a common frequency or harmonic relationship.

```
Subject-Verb Agreement:

"The dog runs"

NP: □·◯ (container-point-vesica)
VP: ~─· (motion-path-anchor)

Resonance: □·◯ ~─·
               │
               └── Number agreement: Singular = single point (·)

"The dogs run"

NP: □··◯ (container-points-vesica)
VP: ~─·· (motion-path-anchors)

Resonance: □··◯ ~─··
               ││
               └── Number agreement: Plural = multiple points (··)
```

### 5.2 Gender Agreement

Gender is encoded as **qualitative geometric properties**:

```
Spanish Gender:

Masculine: □─ (Square-Line) — structured, bounded
  el perro = □·◯ □─·       [the dog-MASC]
  
Feminine: □~ (Square-Curve) — flowing, expansive
  la perra = □·◯ □~·       [the dog-FEM]

Agreement propagation:
  El perro bueno = □·◯ □─· ∧~□─
  La perra buena = □·◯ □~· ∧~□~
                     │      │
                     └──────┘
                     Gender coherence: ─ matches ─, ~ matches ~
```

```
German Gender:

Masculine: □─ (like Spanish)
Feminine:  □~ (like Spanish)
Neuter:    □· (Square-Point) — neutral, singular

Der Hund (m) → □─·
Die Hundin (f) → □~·
Das Tier (n) → □·
```

### 5.3 Number Agreement

| Number | Geometric Pattern | Glyfinform | Example |
|--------|------------------|------------|---------|
| **Singulative** | Single point | · | one dog |
| **Dual** | Paired points | ·· | two dogs |
| **Trial** | Triple points | ··· | three dogs |
| **Plural** | Multiple points | ···· | dogs |
| **Paucal** | Few points | ·· | a few dogs |
| **Collective** | Enclosed points | ◯·◯ | a group of dogs |
| **Distributive** | Separated points | ·  · | each dog |

### 5.4 Person Agreement

| Person | Perspective | Glyfinform | Example |
|--------|-------------|------------|---------|
| **1st** | Self/speaker | · | I, we |
| **2nd** | Other/hearer | ·∧ | you |
| **3rd** | Third entity | ◯─· | he, she, it |
| **Inclusive** | Speaker+hearer | ·◯ | we (you and I) |
| **Exclusive** | Speaker+others | ··· | we (not you) |

### 5.5 Agreement Geometry Visualization

```
Resonance field for "The dogs run":

    ┌─────────────────────────┐
    │   □··◯  ~─··           │
    │   │││   │││             │
    │   └┼┼───┼┼┘             │
    │    │    │               │
    │   PLURAL agreement       │
    │   (·· resonates with ··) │
    └─────────────────────────┘

Coherence measure:
  vesica_coherence = dot_product(NP.coefficients, VP.coefficients)
                   = high when patterns match
                   = low when mismatched (agreement violation)
```

---

## 6. WORD ORDER → SPATIAL ARRANGEMENT

### 6.1 Word Order as Geometric Field

The linear order of words corresponds to **spatial arrangement in a geometric field**:

```
SVO (Subject-Verb-Object):

Spatial:  Point ────── Flow ────── Container
          [S]        [V]          [O]
          
Glyf:     □·◯        ~─·          □·◯→
          
"The dog sees the cat"

SOV (Subject-Object-Verb):

Spatial:  Point ────── Container ────── Flow
          [S]        [O]            [V]
          
Glyf:     □·◯        □·◯→           ·◯~
          
"The dog the cat sees" (Turkish, Japanese)

VSO (Verb-Subject-Object):

Spatial:  Flow ────── Point ────── Container
          [V]        [S]          [O]
          
Glyf:     ·◯~        □·◯          □·◯→
          
"Sees the dog the cat" (Irish, Arabic)
```

### 6.2 Word Order Parameters

| Parameter | Setting | Geometric Effect |
|-----------|---------|------------------|
| **Head-Direction** | Head-initial | Modifier follows head |
| | Head-final | Modifier precedes head |
| **Subject** | SVO | S before V |
| | SOV | S before O |
| | VSO | V first |
| **Prepositions** | Prepositional | Relation before noun (·◯ □·) |
| | Postpositional | Relation after noun (□· ·◯) |
| **Auxiliaries** | Auxiliary-first | Aux before verb |
| | Auxiliary-last | Aux after verb |

### 6.3 Language Examples

**English (SVO, Head-initial):**
```
"The big dog runs quickly"

Glyf:   □·◯ ∧~□· ~─· ~~
        │     │    │   │
        │     │    │   └── Adverb
        │     │    └────── Verb
        │     └─────────── Adjective + Noun
        └───────────────── Determiner

Structure: Det-Adj-Noun Verb Adv
           (modifiers precede heads)
```

**Japanese (SOV, Head-final):**
```
"犬が速く走る" /inu-ga-hayaku-hashiru/
"Dog quickly runs"

Glyf:   □· ~─ ~~ ~─·
        │   │  │   │
        │   │  │   └── Verb (final)
        │   │  └────── Adverb (before verb)
        │   └───────── Particle (subject marker)
        └───────────── Noun

Structure: Noun-Particle Adverb Verb
           (modifiers precede heads, verb final)
```

**Irish (VSO):**
```
"Rithreann an madra"
"Runs the dog"

Glyf:   ~─·~ □·◯ □─·
        │    │    │
        │    │    └── Noun
        │    └─────── Determiner
        └──────────── Verb (initial)

Structure: Verb Det Noun
```

---

## 7. MORPHOLOGICAL OPERATIONS

### 7.1 Affixation as Geometric Addition

**Prefixes:**
```
un- (negation) = ∅ (Void)
  happy = ~□~
  unhappy = ∅~□~
  
re- (again) = ~← (backward flow)
  do = ~↓
  redo = ~←~↓
  
pre- (before) = ~←·
  view = ·◯~
  preview = ~←·◯~
```

**Suffixes:**
```
-s (plural) = · → ··
  dog = □─·
  dogs = □─··
  
-ed (past) = ~ ← ~
  walk = ~─
  walked = ~─~
  
-ing (progressive) = ~○
  run = ~─·
  running = ~─·~○
  
-ness (nominalization) = ~□
  happy = ~□~
  happiness = ~□~□
```

### 7.2 Compounding as Geometric Fusion

```
black + bird = blackbird

Glyf:   ∧□ + ~◯ = ∧□~◯
        │     │
        │     └── Flow + Vesica (bird = flying life)
        └───────── Angle + Square (black = absence of light)
        
Compound: ∧□~◯ = blackbird (structured absence + flowing life)
```

```
sun + flower = sunflower

Glyf:   ◯· + ~◯ = ◯·~◯
        │     │
        │     └── Curve + Vesica (flower = blooming union)
        └───────── Vesica + Point (sun = radiant source)
        
Compound: ◯·~◯ = sunflower (radiant source + blooming)
```

### 7.3 Reduplication as Geometric Repetition

```
Full reduplication: A + A = AA
Indonesian: orang-orang = person-person = people
Glyf: ◯─· + ◯─· = ◯─·· (repeated point = plural)

Partial reduplication: A₁ + A = A'A
Tagalog: takbó (run) → tatakbó (will run)
Glyf: ~─· → ·~─· (inceptive point + verb)
```

### 7.4 Ablaut as Internal Geometric Shift

```
sing/sang/sung (English strong verb):

sing (present): ~─∧~ (flow-line-angle-flow)
sang (past):    ~─∧~← (add backward marker)
sung (participle): ~─∧~○ (add cyclic completion)

man/men (umlaut plural):

man: ◯─·  (singular)
men: ◯─·· (vowel shift → plural point)
```

---

## 8. SYNTACTIC RELATIONS

### 8.1 Universal Dependencies as Geometric Relations

| Relation | Function | Geometric Pattern | Example |
|----------|----------|------------------|---------|
| **nsubj** | Nominal subject | · ~ | dog runs |
| **obj** | Direct object | ·→ ~ | sees dog |
| **iobj** | Indirect object | ·→ ~→ | gives to dog |
| **det** | Determiner | ◯ □· | the dog |
| **amod** | Adjectival modifier | ∧~ □· | big dog |
| **nmod** | Nominal modifier | ◯~ □· | dog's tail |
| **advmod** | Adverbial modifier | ~~ ~ | quickly runs |
| **aux** | Auxiliary | ~· ~ | is running |
| **cop** | Copula | · = | is dog |
| **case** | Case marker | ·◯ □· | in dog |
| **mark** | Marker | ·◯ ~ | that runs |
| **conj** | Conjunction | ◯ + ◯ | dog and cat |
| **cc** | Coordinating conj. | ◯∧ | and |

### 8.2 Dependency Tree → Geometric Graph

```
"The dog sees the black cat"

Traditional dependency tree:
        sees (root)
       /    \
     dog    cat
     /      /  \
   The    black  the

Glyf geometric graph:

           ·◯~ (~ sees)
          /    \
   □·◯ (the dog)  □·◯→ (the cat)
                  /
              ∧~□· (black)

Edges represent agreement/resonance:
  ·◯~ ───vesica_coherence─── □·◯ (subject agreement)
  ·◯~ ───vesica_coherence─── □·◯→ (object selection)
  □·◯→ ───containment─────── ∧~□· (modification)
```

---

## 9. CROSS-LINGUISTIC SYNTACTIC PATTERNS

### 9.1 Relative Clauses

```
English (post-nominal):
"The dog [that I saw]"
Glyf: □·◯ [·◯~←·]

Japanese (pre-nominal):
"[Watashi-ga mita] inu"
"[I saw] dog"
Glyf: [· ◯~←·] □·

Arabic (post-nominal with resumptive):
"Al-kalb [alladhi ra'aytuhu]"
"The-dog [which I-saw-him]"
Glyf: □·◯ [◯∧ ·◯~←·→]
```

### 9.2 Question Formation

```
English (wh-fronting):
"What did you see?"
Glyf: ~∧· ∧· ·∧ ·◯~
      what   did  you  see

Japanese (wh-in-situ):
"Nani-o mita ka"
"What saw Q"
Glyf: ~∧·→ ·◯~ ∧∧
      what    see  Q

Chinese (wh-in-situ, particle):
"Ni kanjian-le shenme"
"You saw what"
Glyf: ·∧ ·◯~·~ ~∧·
      you  saw   what
```

### 9.3 Negation Strategies

```
English (auxiliary negation):
"I do not run"
Glyf: · ∧· ∅∧ ~─·
      I  do  not  run

Spanish (verbal negation):
"No corro"
"Not run"
Glyf: ∅∧ ~─·
      not  run

French (ne...pas):
"Je ne cours pas"
"I not run not"
Glyf: · ∅∧ ~─· ∅∧
      I  not  run  not

Mandarin (adverbial negation):
"Wo bu pao"
"I not run"
Glyf: · ∅∧ ~─·
      I  not  run
```

---

## 10. IMPLEMENTATION

### 10.1 Parsing Algorithm

```rust
/// Parse sentence to geometric structure
pub fn parse_to_geometry(sentence: &str) -> GeometricStructure {
    // Step 1: Tokenize
    let tokens = tokenize(sentence);
    
    // Step 2: Assign geometric primitives
    let glyphs: Vec<Glyfinform> = tokens.iter()
        .map(|t| word_to_glyph(t))
        .collect();
    
    // Step 3: Identify dependencies
    let dependencies = parse_dependencies(&tokens);
    
    // Step 4: Build geometric graph
    let mut graph = GeometricGraph::new();
    
    for (i, glyph) in glyphs.iter().enumerate() {
        graph.add_node(i, glyph.clone());
    }
    
    for dep in dependencies {
        graph.add_edge(
            dep.head,
            dep.dependent,
            relation_to_geometry(dep.relation)
        );
    }
    
    // Step 5: Compute resonance field
    graph.compute_resonance();
    
    GeometricStructure {
        nodes: glyphs,
        edges: graph.edges,
        resonance: graph.resonance_matrix,
    }
}
```

### 10.2 Generation Algorithm

```rust
/// Generate sentence from geometric structure
pub fn generate_from_geometry(geo: &GeometricStructure) -> String {
    // Step 1: Determine word order from spatial arrangement
    let order = determine_linear_order(geo);
    
    // Step 2: Apply agreement
    let harmonized = apply_agreement(geo, &order);
    
    // Step 3: Generate morphology
    let inflected = apply_morphology(harmonized);
    
    // Step 4: Linearize
    let mut sentence = String::new();
    for (i, node_idx) in order.iter().enumerate() {
        if i > 0 {
            sentence.push(' ');
        }
        sentence.push_str(&inflected[*node_idx].surface_form);
    }
    
    sentence
}
```

---

## 11. VALIDATION

### 11.1 Parse Accuracy Targets

| Language | UAS (Unlabeled) | LAS (Labeled) | Target |
|----------|----------------|---------------|--------|
| English | >95% | >92% | ✓ |
| Chinese | >90% | >87% | In Progress |
| Spanish | >93% | >90% | In Progress |
| Arabic | >85% | >80% | Planned |

### 11.2 Generation Quality

- Grammaticality: >99% (no syntax errors)
- Semantic preservation: >95%
- Naturalness: Human-rated >4.0/5.0

---

## 12. REFERENCES

1. Universal Dependencies (UD) — Nivre et al.
2. Lexical-Functional Grammar (LFG) — Bresnan, Kaplan
3. Head-Driven Phrase Structure Grammar (HPSG) — Pollard, Sag
4. Construction Grammar — Goldberg
5. Glyf Phonology — This specification
6. Glyf Lexiconic System — This specification

---

*Grammar is not a set of rules to follow but a space of geometric possibilities to explore.*
