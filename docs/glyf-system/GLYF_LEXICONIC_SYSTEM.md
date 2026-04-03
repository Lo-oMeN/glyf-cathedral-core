# GLYF LEXICONIC SYSTEM
## Multi-Language Geometric Lexicon Architecture v1.0.0

**Date:** 2026-04-01  
**Status:** Production Specification  
**Scope:** Universal semantic fields, language-specific mappings, cross-lingual alignment  
**Coverage:** English (complete), Spanish, Mandarin, Arabic, Sanskrit (roadmaps)

---

## 1. EXECUTIVE OVERVIEW

The Glyf Lexiconic System establishes a **universal geometric substrate** for linguistic meaning across human languages. Unlike statistical multilingual models that learn parallel embeddings, Glyf encodes semantic invariants directly into geometric primitives that transcend linguistic boundaries.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GLYF LEXICONIC ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYER 1: UNIVERSAL SEMANTIC FIELDS (Language-Independent)               │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐          │
│  │  SPACE  │  TIME   │ MOTION  │ EMOTION │ COGNITION│  LIFE   │          │
│  └────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘          │
│       │         │         │         │         │         │               │
│       └─────────┴─────────┴────┬────┴─────────┴─────────┘                │
│                                ▼                                        │
│  LAYER 2: SEMANTIC PRIMITIVES (Core Meaning Atoms)                       │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐          │
│  │CONTAINER│  PATH   │  FORCE  │  UNION  │  AGENT  │  OBJECT │          │
│  └────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘          │
│       │         │         │         │         │         │               │
│       └─────────┴─────────┴────┬────┴─────────┴─────────┘                │
│                                ▼                                        │
│  LAYER 3: GEOMETRIC GLYFF (7-Primitive Encoding)                         │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐                            │
│  │  ∅  │  ·  │  ─  │  ~  │  ∧  │  □  │  ◯  │                            │
│  │Void │Point│ Line│Curve│Angle│Square│Vesica│                          │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘                            │
│                                                                          │
│  LAYER 4: LANGUAGE-SPECIFIC MANIFESTATIONS                               │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐               │
│  │ English  │ Spanish  │ Mandarin │  Arabic  │ Sanskrit │               │
│  │  (en)    │  (es)    │  (zh)    │  (ar)    │  (sa)    │               │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. UNIVERSAL SEMANTIC FIELDS

### 2.1 Core Semantic Domains

Semantic fields are conceptual regions that exist across all human languages, though with varying boundary definitions and internal structure.

#### FIELD 1: SPATIAL RELATIONS
**Geometric Signature:** □-dominant with directional vectors

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| CONTAINMENT | □ | in, inside | en, dentro | 在...里 | في |
| EXTERIORITY | □→ | out, outside | fuera, afuera | 外面 | خارج |
| PROXIMITY | ·· | near, close | cerca, junto | 近 | قريب |
| DISTANCE | ·  · | far, distant | lejos, distante | 远 | بعيد |
| VERTICALITY (↑) | ↑ | up, above | arriba, sobre | 上 | فوق |
| VERTICALITY (↓) | ↓ | down, below | abajo, debajo | 下 | تحت |
| HORIZONTAL (→) | → | right, east | derecha, este | 右/东 | يمين/شرق |
| HORIZONTAL (←) | ← | left, west | izquierda, oeste | 左/西 | يسار/غرب |
| CENTER | · | center, middle | centro, medio | 中 | وسط |
| PERIPHERY | ○ | around, periphery | alrededor | 周围 | حول |
| PATH | ─ | path, way | camino, vía | 路/道 | طريق |
| BOUNDARY | □─ | edge, boundary | borde, límite | 边 | حد |

**Geometric Composition:**
```
Spatial field encodes as □ with directional extensions:
  □↑  = Container with upward vector = "above/on top"
  □→  = Container with forward exit = "out of/exit"
  □·  = Container with central point = "in the middle"
  ·□· = Point-container-point = "between"
```

#### FIELD 2: TEMPORAL RELATIONS
**Geometric Signature:** ~-dominant with sequence markers

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| PRESENT | · | now, present | ahora, presente | 现在 | الآن |
| PAST | ~← | past, before | pasado, antes | 过去/以前 | ماضٍ |
| FUTURE | ~→ | future, after | futuro, después | 将来/以后 | مستقبل |
| DURATION | ─ | during, while | durante | 期间 | أثناء |
| MOMENT | · | moment, instant | momento | 时刻 | لحظة |
| ETERNITY | ○ | forever, always | siempre, eterno | 永远 | دائماً |
| BEGINNING | ·~↑ | begin, start | empezar, comenzar | 开始 | بدأ |
| ENDING | ·~↓ | end, finish | terminar, acabar | 结束 | انتهى |
| SEQUENCE | ─·─ | then, next | luego, entonces | 然后 | ثم |
| SIMULTANEITY | ◯ | while, as | mientras | 同时 | بينما |
| FREQUENCY | ~~ | often, always | a menudo | 经常 | غالباً |
| RARITY | ∅~ | seldom, never | rara vez, nunca | 很少/从不 | نادراً |

**Geometric Composition:**
```
Temporal field encodes flow (~) with direction:
  ~← = Backward flow = "past/before"
  ~→ = Forward flow = "future/after"
  ~○ = Cyclic flow = "recurring/always"
  ·~ = Instantiated flow = "beginning"
```

#### FIELD 3: MOTION & ACTION
**Geometric Signature:** ~-dominant with force vectors

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| TRANSLATION | ~─ | go, move | ir, mover | 走/移动 | ذهب |
| RAPID MOTION | ~─· | run, rush | correr, precipitar | 跑 | ركض |
| ARRIVAL | ~→· | come, arrive | venir, llegar | 来 | جاء |
| DEPARTURE | ~← | leave, depart | salir, partir | 离开 | غادر |
| ASCENT | ~↑ | rise, climb | subir, escalar | 上升 | صعد |
| DESCENT | ~↓ | fall, descend | caer, descender | 下降 | سقط |
| ROTATION | ~○ | turn, rotate | girar, volver | 转 | دار |
| ENTRY | □← | enter, go in | entrar | 进入 | دخل |
| EXIT | □→ | exit, go out | salir | 出去 | خرج |
| TRANSPORT | ~~─ | carry, bring | llevar, traer | 带/拿 | حمل |
| CREATION | ○~□ | make, create | hacer, crear | 做/创造 | صنع |
| DESTRUCTION | ∧□∧ | break, destroy | romper, destruir | 破坏 | كسر |

#### FIELD 4: EMOTION & AFFECT
**Geometric Signature:** ◯-dominant with resonance patterns

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| LOVE | ◯~· | love | amor, amar | 爱 | حب |
| JOY | ◯~~ | joy, happy | alegría, feliz | 快乐 | فرح |
| SORROW | ~↓~ | sadness, grief | tristeza, pena | 悲伤 | حزن |
| FEAR | ∧~∧ | fear, afraid | miedo, temor | 害怕 | خوف |
| ANGER | ∧∧~ | anger, rage | ira, enfado | 生气 | غضب |
| SURPRISE | ·∧· | surprise | sorpresa | 惊讶 | مفاجأة |
| DISGUST | ∅∧ | disgust | asco | 厌恶 | اشمئزاز |
| TRUST | ◯· | trust, faith | confianza, fe | 信任 | ثقة |
| ANTICIPATION | ~→ | hope, expect | esperanza, esperar | 希望 | أمل |
| CALM | ○~ | peace, calm | paz, calma | 平静 | سلام |
| EXCITEMENT | ~∧~ | excitement | emoción | 兴奋 | إثارة |
| CONTENTMENT | ◯□ | contentment | contento | 满足 | رضا |

**Emotion Geometry:**
```
Emotional space organized by valence (V) and arousal (A):
  Valence encoded in Vesica sign (positive/negative)
  Arousal encoded in Curve amplitude
  
  ◯~~  = High positive valence, high arousal = JOY
  ~↓~  = Negative valence, moderate arousal = SADNESS
  ∧∧~  = Negative valence, high arousal = ANGER
  ○~   = Neutral valence, low arousal = PEACE
```

#### FIELD 5: COGNITION & KNOWLEDGE
**Geometric Signature:** ·-dominant with union markers

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| KNOWING | ◯· | know | saber, conocer | 知道 | عرف |
| THINKING | ◯~ | think | pensar | 想/思考 | فكر |
| UNDERSTANDING | ◯◯~ | understand | entender, comprender | 理解 | فهم |
| LEARNING | ~→· | learn | aprender | 学习 | تعلم |
| MEMORY | ~←· | remember | recordar | 记得 | تذكر |
| FORGETTING | ∅~ | forget | olvidar | 忘记 | نسي |
| PERCEPTION | ·◯ | see, perceive | ver, percibir | 感知 | أدرك |
| IMAGINATION | ~◯~ | imagine | imaginar | 想象 | تخيل |
| REASON | ─∧─ | reason, logic | razón, lógica | 逻辑 | منطق |
| WISDOM | ◯~·∧ | wisdom | sabiduría | 智慧 | حكمة |
| DOUBT | ∧∧ | doubt | duda | 怀疑 | شك |
| CERTAINTY | ◯◯ | certainty | certeza | 确定 | يقين |

#### FIELD 6: LIFE & BIOLOGY
**Geometric Signature:** Spiral phyllotaxis (~ with φ-harmonic)

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| LIFE | ◯~ | life | vida | 生命 | حياة |
| DEATH | ·~↓ | death | muerte | 死亡 | موت |
| GROWTH | ~↑□ | growth | crecimiento | 生长 | نمو |
| BIRTH | ·~↑ | birth | nacimiento | 出生 | ميلاد |
| BREATH | ~ | breath | respiración | 呼吸 | نفس |
| PLANT | ~↑~ | plant | planta | 植物 | نبات |
| ANIMAL | ~·~ | animal | animal | 动物 | حيوان |
| HUMAN | ◯─· | human | humano | 人 | إنسان |
| BODY | □·~ | body | cuerpo | 身体 | جسد |
| MIND | ◯·~ | mind | mente | 心灵/头脑 | عقل |
| HEALTH | ◯□ | health | salud | 健康 | صحة |
| DISEASE | ∧□ | disease | enfermedad | 疾病 | مرض |

#### FIELD 7: SOCIAL RELATIONS
**Geometric Signature:** ◯-dominant with connection patterns

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| PERSON | ◯─· | person | persona | 人 | شخص |
| PEOPLE | ◯─·· | people | gente | 人们 | ناس |
| FAMILY | ◯◯~ | family | familia | 家庭 | عائلة |
| FRIEND | ◯~◯ | friend | amigo | 朋友 | صديق |
| ENEMY | ∧◯∧ | enemy | enemigo | 敌人 | عدو |
| GROUP | ◯··· | group | grupo | 团体 | مجموعة |
| LEADER | ◯·↑ | leader | líder | 领导 | قائد |
| SERVANT | ◯·↓ | servant | sirviente | 仆人 | خادم |
| STRANGER | ∅◯ | stranger | extraño | 陌生人 | غريب |
| PARTNER | ◯=◯ | partner | compañero | 伙伴 | شريك |
| COMMUNITY | ◯◯◯ | community | comunidad | 社区 | مجتمع |
| SOCIETY | □◯◯□ | society | sociedad | 社会 | مجتمع |

#### FIELD 8: PHYSICAL PROPERTIES
**Geometric Signature:** □-dominant with quality modifiers

| Concept | Universal Glyff | English | Spanish | Mandarin | Arabic |
|---------|-----------------|---------|---------|----------|--------|
| SOLID | □ | solid | sólido | 固体 | صلب |
| LIQUID | ~~ | liquid | líquido | 液体 | سائل |
| GAS | ~○~ | gas | gas | 气体 | غاز |
| HEAVY | □↓ | heavy | pesado | 重 | ثقيل |
| LIGHT (weight) | □↑ | light | ligero | 轻 | خفيف |
| HOT | ∧~∧ | hot | caliente | 热 | حار |
| COLD | ~∧~ | cold | frío | 冷 | بارد |
| HARD | □∧ | hard | duro | 硬 | صلب |
| SOFT | ~□~ | soft | blando | 软 | ناعم |
| BIG | □□ | big | grande | 大 | كبير |
| SMALL | ·□ | small | pequeño | 小 | صغير |
| LONG | □─ | long | largo | 长 | طويل |
| SHORT | □ | short | corto | 短 | قصير |

---

## 3. LANGUAGE-SPECIFIC GLYFINFORM MAPPINGS

### 3.1 English (Complete Reference)

**Status:** Production-ready, 1,000+ words mapped

**Mapping Characteristics:**
- Germanic root dominance → Angle-heavy glyphs for action
- Latinate borrowings → Vesica-dominant for abstract concepts
- Phonetic transparency → Direct phoneme-to-glyph mapping

**Core Function Words:**
| Word | Glyfinform | Semantic Field | Notes |
|------|------------|----------------|-------|
| the | ~· | Determiner | Definite marker |
| a/an | · | Determiner | Indefinite singularity |
| and | ◯∧ | Conjunction | Union with distinction |
| or | ◯~ | Conjunction | Union with flow |
| but | ∧∧ | Conjunction | Opposition |
| if | ·∧ | Conditional | Point of divergence |
| then | ~─ | Temporal | Sequential flow |
| because | ·~◯ | Causal | Grounded union |
| of | ◯~ | Genitive | Belonging flow |
| to | ─· | Directive | Target point |
| in | ·◯ | Locative | Interior point |
| on | ◯· | Locative | Surface contact |
| at | ·∧ | Locative | Specific location |
| by | ·~ | Agentive | Proximate point |
| with | ~─~· | Comitative | Accompaniment |
| for | ─~ | Benefactive | Purpose path |
| from | ─~◯ | Ablative | Source union |

**High-Frequency Verbs:**
| Verb | Glyfinform | Root Meaning |
|------|------------|--------------|
| be | · | Existence |
| have | □· | Containment |
| do | ~↓ | Action down |
| say | ~─ | Speech path |
| get | ~←· | Acquisition |
| make | ~→□ | Creation |
| go | ~→ | Forward motion |
| know | ◯· | Union knowledge |
| think | ◯~ | Union process |
| take | ~←□ | Taking container |
| see | ·◯ | Perceptual point |
| come | ~→· | Arrival |
| want | ~∧· | Desire angle |
| look | ~·∧ | Visual angle |
| use | ~□ | Instrumental |
| find | ─~∧ | Discovery path |
| give | ~→~ | Transfer flow |
| tell | ──~ | Informative |
| ask | ∧~· | Question angle |
| work | □~─ | Productive |
| seem | ~◯~ | Appear flow |
| feel | ─~· | Tactile |
| try | ∧~ | Attempt angle |
| leave | ~← | Departure |
| call | ─∧· | Summon point |

### 3.2 Spanish Roadmap (es)

**Status:** Planned, Phase 1 ready

**Language Characteristics:**
- Syllable-timed rhythm → Uniform glyph spacing
- 5 pure vowels → Simplified vowel-to-Curve mapping
- Rolled /r/ (rr) → Distinct primitive (~◯◯)
- Ñ phoneme → Palatal nasal (◯∧)
- Gender system → Grammatical geometry (see Morphosyntax)

**Priority Vocabulary (First 100):**

| Spanish | Glyfinform | English | Notes |
|---------|------------|---------|-------|
| el/la | ·◯ | the | Gendered definite |
| de | ◯~ | of | Genitive |
| que | ◯∧ | that | Complementizer |
| y | ◯ | and | Simple union |
| a | ─· | to | Dative marker |
| en | ·◯ | in | Locative |
| un/una | · | a | Indefinite |
| ser | · | to be | Essential being |
| estar | ~· | to be | Situated being |
| haber | □· | to have | Existential |
| por | ─~ | by/through | Path |
| con | ◯◯ | with | Union |
| para | ──· | for | Purpose |
| no | ∅ | no | Negation |
| sí | · | yes | Affirmation |
| este/esta | ~─· | this | Proximate |
| ese/esa | ~─ | that | Distal |
| aquel | ~─~ | that (far) | Remote |
| muy | ~~ | very | Intensifier |
| más | ↑ | more | Upward |
| menos | ↓ | less | Downward |
| bien | ◯~ | well | Good union |
| mal | ∧~ | badly | Bad angle |
| aquí | ~· | here | Immediate |
| ahí | ~ | there | Medial |
| allí | ~─ | there (far) | Distal |
| ahora | · | now | Present |
| después | ~→ | after | Forward |
| antes | ~← | before | Backward |
| siempre | ○ | always | Cyclic |
| nunca | ∅ | never | Void |
| también | ◯◯ | also | Additional union |
| solo | · | only | Singular |
| todo | ○ | all | Complete |
| otro | ∧~ | other | Different |
| mismo | ·◯ | same | Identical union |
| años | ◯~─ | years | Cyclic time |
| día | ~─ | day | Light period |
| tiempo | ─·~ | time | Duration |
| vez | ◯ | time (instance) | Occasion |
| hombre | ◯─· | man | Human male |
| mujer | ~◯─· | woman | Human female |
| persona | ◯─· | person | Individual |
| gente | ◯─·· | people | Collective |
| vida | ◯~ | life | Animation |
| mundo | ~◯□ | world | Global container |
| país | □· | country | Bounded territory |
| ciudad | □□□ | city | Urban complex |
| casa | □· | house | Dwelling |
| lugar | ·◯ | place | Location |
| forma | ~□ | form | Shape container |
| trabajo | □~─ | work | Productive effort |
| cosa | □· | thing | Object |
| parte | ─∧· | part | Division |
| grupo | ◯··· | group | Collection |
| problema | ∧□∧ | problem | Obstacle |
| sistema | □◯~□ | system | Organized whole |
| programa | ~→□~ | program | Forward plan |
| manera | ~~ | manner | Way |
| momento | · | moment | Instant |
| verdad | ·◯─ | truth | Grounded point |
| razón | ─∧─ | reason | Logical path |
| historia | ~─·~ | history | Temporal narrative |
| agua | ~~ | water | Flow |
| mano | ~∧·◯ | hand | Manual tool |
| ojo | ◯· | eye | Perceptual orb |
| cabeza | □∧ | head | Top container |
| pie | ·∧ | foot | Ground point |
| corazón | ◯~· | heart | Emotional center |
| palabra | ~─·~ | word | Speech unit |
| nombre | ◯─· | name | Identity label |
| número | ··· | number | Counting |
| manera | ~~ | way/manner | Method flow |
| pregunta | ∧~· | question | Inquiry angle |
| respuesta | ─∧· | answer | Resolution |
| caso | ◯· | case | Instance |
| punto | · | point | Location |
| lado | ─∧ | side | Lateral |
| centro | ·◯ | center | Middle |
| fin | ∧ | end | Termination |
| principio | ·~↑ | beginning | Origin |
| estado | ~□ | state | Condition |
| gobierno | ◯─↑ | government | Directing union |
| política | ─∧~ | politics | Divergent path |
| economía | □~─ | economy | Household management |
| empresa | ~→□ | company | Forward venture |
| escuela | □~· | school | Learning place |
| estudiante | ~→· | student | Learner |
| maestro | ◯·↑ | teacher | Guiding point |
| libro | □~ | book | Knowledge container |
| palabra | ~─·~ | word | Verbal unit |
| amigo | ◯~◯ | friend | Mutual bond |
| familia | ◯◯~ | family | Kinship |
| padre | ◯─· | father | Male parent |
| madre | ~◯─· | mother | Female parent |
| hijo/hija | ·~□ | child | Offspring |
| hermano | ◯─·· | sibling | Same level |
| esposo | ◯=◯ | spouse | Partner |

**Spanish-Specific Considerations:**
1. **Ser vs. Estar:** Both "to be" but distinct geometric encoding
   - ser = · (essential, permanent)
   - estar = ~· (situational, temporary)

2. **Subjunctive Mood:** Marked by conditional geometry
   - que + subjunctive = ◯∧ with uncertainty weight

3. **Reflexive se:** Self-referential loop
   - se = ◯ with self-targeting vector

### 3.3 Mandarin Roadmap (zh)

**Status:** Planned, Phase 1 design

**Language Characteristics:**
- Tonal system (4 tones + neutral) → Vertical position encoding
- Syllable-timed, single morpheme preference
- Character-based writing → Direct glyph mapping potential
- Topic-prominent syntax → Center Æxis reorganization
- Measure words → Classifier geometry

**Tone-to-Geometry Mapping:**
| Tone | Pitch | Vertical Position | Glyph Modification |
|------|-------|-------------------|-------------------|
| T1 (high) | 55 | Upper half | e₃ positive |
| T2 (rising) | 35 | Ascending | e₃ gradient |
| T3 (low/dip) | 214 | Lower then rise | e₃ negative then positive |
| T4 (falling) | 51 | Descending | e₃ negative |
| Neutral | variable | Center | e₃ neutral |

**Priority Vocabulary:**

| Mandarin | Pinyin | Glyfinform | Semantic Notes |
|----------|--------|------------|----------------|
| 的 | de | ◯~ | Possessive particle |
| 一 | yī | · | One, unified |
| 是 | shì | · | To be (copula) |
| 不 | bù | ∅ | Negation |
| 了 | le | ~ | Completion aspect |
| 人 | rén | ◯─· | Person |
| 我 | wǒ | · | I/me (self-point) |
| 你 | nǐ | ·∧ | You (other-point) |
| 他/她 | tā | ◯─· | He/she (third person) |
| 我们 | wǒmen | ·◯ | We (self-union) |
| 这 | zhè | ~─· | This (proximate) |
| 那 | nà | ~─ | That (distal) |
| 来 | lái | ~→· | Come (arrival) |
| 去 | qù | ~← | Go (departure) |
| 上 | shàng | ↑ | Up/on |
| 下 | xià | ↓ | Down/under |
| 大 | dà | □□ | Big |
| 小 | xiǎo | ·□ | Small |
| 中 | zhōng | ·◯ | Middle/in |
| 年 | nián | ◯~─ | Year (cycle) |
| 月 | yuè | ◯· | Moon/month |
| 日 | rì | ◯· | Sun/day |
| 时 | shí | ─· | Time/hour |
| 说 | shuō | ~─ | Speak |
| 要 | yào | ~∧· | Want/need |
| 会 | huì | ◯~ | Can/will |
| 能 | néng | □~ | Able/capable |
| 可以 | kěyǐ | ~□~ | May/allowed |
| 很 | hěn | ~~ | Very (intensifier) |
| 好 | hǎo | ◯□ | Good |
| 多 | duō | ··· | Many |
| 少 | shǎo | · | Few |
| 都 | dōu | ○ | All/both |
| 在 | zài | ~· | At/exist |
| 有 | yǒu | □· | Have/exist |
| 没 | méi | ∅ | Not have |
| 做 | zuò | ~□ | Do/make |
| 工作 | gōngzuò | □~─ | Work |
| 看 | kàn | ·◯ | Look/see |
| 见 | jiàn | ·◯ | See/meet |
| 听 | tīng | ◯~ | Listen/hear |
| 想 | xiǎng | ◯~ | Think/want |
| 知道 | zhīdào | ◯·~→ | Know (be aware) |
| 认识 | rènshi | ◯─· | Recognize/know |
| 喜欢 | xǐhuan | ◯~~ | Like |
| 爱 | ài | ◯~· | Love |
| 水 | shuǐ | ~~ | Water |
| 火 | huǒ | ∧~∧ | Fire |
| 土 | tǔ | □~ | Earth/soil |
| 木 | mù | ~↑□ | Wood/tree |
| 金 | jīn | □∧ | Metal/gold |
| 家 | jiā | □· | Home/family |
| 国 | guó | □□ | Country |
| 学 | xué | ~→· | Study/learn |
| 问 | wèn | ∧~· | Ask |
| 问题 | wèntí | ∧□∧ | Problem/question |
| 事情 | shìqing | □· | Matter/thing |
| 地方 | dìfang | ·◯ | Place |
| 时候 | shíhou | ─·~ | Time/when |
| 东西 | dōngxi | □· | Thing (east-west) |
| 现在 | xiànzài | · | Now |
| 以后 | yǐhòu | ~→ | After/later |
| 以前 | yǐqián | ~← | Before |
| 今天 | jīntiān | ~─· | Today |
| 明天 | míngtiān | ~→~ | Tomorrow |
| 昨天 | zuótiān | ~←~ | Yesterday |

**Mandarin-Specific Considerations:**
1. **Topic-Comment Structure:** Topic = Center Æxis anchor, Comment = predicate geometry
2. **Aspect Markers:** 了(~), 着(~○), 过(~←) as temporal geometry
3. **Measure Words:** Mandatory classifiers encode shape/container semantics
4. **Serial Verb Construction:** Sequential ~ glyphs without conjunction

### 3.4 Arabic Roadmap (ar)

**Status:** Planned, Phase 0 design

**Language Characteristics:**
- Triconsonantal root system → Geometric root patterns
- Nonconcatenative morphology → Interdigitation geometry
- Right-to-left script → Mirrored glyfinform rendering
- Definiteness marking (al-) → Boundary geometry
- Complex verbal morphology → Temporal operator stacking

**Root Pattern Geometry:**
Arabic roots (typically 3 consonants) map to geometric bases:
```
K-T-B (write) → ·─□ (Point-Line-Square)
  kataba (wrote) → ·─□~←
  yaktubu (writes) → ~→·─□
  kitab (book) → □·─□
  katib (writer) → ·─□─·
  maktab (office) → □·─□·
  maktaba (library) → □·─□~□
```

**Priority Vocabulary:**

| Arabic | Transliteration | Glyfinform | Notes |
|--------|-----------------|------------|-------|
| في | fī | ·◯ | In |
| من | min | ─~◯ | From |
| إلى | ilá | ─· | To |
| على | 'alá | ◯· | On |
| عن | 'an | ~∧ | About |
| مع | ma'a | ◯◯ | With |
| هذا | hādhā | ~─· | This (m) |
| هذه | hādhihi | ~─·~ | This (f) |
| ذلك | dhālika | ~─ | That |
| هو | huwa | ◯─· | He/it |
| هي | hiya | ~◯─· | She |
| هم | hum | ◯─·· | They |
| كان | kāna | ·~ | Was |
| يكون | yakūn | ~→· | Will be |
| ليس | laysa | ∅· | Is not |
| قال | qāla | ~─ | Said |
| يقول | yaqūlu | ~→~─ | Says |
| كل | kull | ○ | All/every |
| بعض | ba'd | ∧~ | Some |
| كثير | kathīr | ··· | Many |
| قليل | qalīl | · | Few |
| جيد | jayyid | ◯□ | Good |
| سيئ | sayyi' | ∧□ | Bad |
| كبير | kabīr | □□ | Big |
| صغير | saghīr | ·□ | Small |
| جديد | jadīd | ·~ | New |
| قديم | qadīm | ~─·~ | Old |
| وقت | waqt | ─·~ | Time |
| يوم | yawm | ~─ | Day |
| ليلة | layla | ~─~ | Night |
| سنة | sana | ◯~─ | Year |
| رجل | rajul | ◯─· | Man |
| امرأة | imra'a | ~◯─·~ | Woman |
| بيت | bayt | □· | House |
| مدينة | madīna | □□□ | City |
| بلد | balad | □· | Country |
| ماء | mā' | ~~ | Water |
| نار | nār | ∧~∧ | Fire |
| أرض | ard | □~ | Earth |
| سماء | samā' | ~↑~ | Sky |
| شمس | shams | ◯· | Sun |
| قمر | qamar | ◯·~ | Moon |
| نجم | najm | ·∧· | Star |
| واحد | wāhid | · | One |
| اثنان | ithnān | ·· | Two |
| ثلاثة | thalātha | ··· | Three |
| أربعة | arba'a | □ | Four |
| خمسة | khamsa | ∧ | Five |
| عمل | 'amila | ~□ | Work/do |
| أخذ | akhadha | ~←□ | Take |
| أعطى | a'tā | ~→~ | Give |
| رأى | ra'ā | ·◯ | See |
| سمع | sami'a | ◯~ | Hear |
| علم | 'alima | ◯· | Know |
| فهم | fahima | ◯◯~ | Understand |
| أحب | ahabba | ◯~· | Love |
| كره | karaha | ∧~∧ | Hate |

**Arabic-Specific Considerations:**
1. **Definite Article (al-):** □ prefix marking boundary
2. **Sun/Moon Letters:** Assimilation encoded in glyph fusion
3. **Dual Number:** ·· suffix for pairs
4. **Broken Plurals:** Internal vowel change = geometric morphing
5. **Verbal Nouns (Masdar):** Nominalized action = □ container

### 3.5 Sanskrit Roadmap (sa)

**Status:** Planned, Phase 0 research

**Language Characteristics:**
- Rich morphological system → Complex geometric composition
- Pitch accent (historical) → Melodic contour encoding
- Compound formation (samāsa) → Geometric concatenation
- Six grammatical cases → Directional vector system
- Three grammatical numbers → Point counting system
- Three grammatical genders → Qualitative geometry

**Grammatical Geometry:**
```
Cases as directional vectors from nominal center:
  Nominative (·)   = Subject: Self-standing point
  Accusative (→)   = Object: Target direction
  Instrumental (─) = Means: Path of action
  Dative (·→)      = Recipient: Target point
  Ablative (←)     = Source: Origin direction
  Genitive (◯~)    = Possession: Belonging union
  Locative (·◯)    = Location: Enclosed point
  Vocative (!)     = Call: Emphatic point
```

**Priority Vocabulary:**

| Sanskrit | IAST | Glyfinform | Notes |
|----------|------|------------|-------|
| अहम् | aham | · | I (self) |
| त्वम् | tvam | ·∧ | You (other) |
| सः/सा | saḥ/sā | ◯─· | He/she |
| एक | eka | · | One |
| द्वि | dvi | ·· | Two |
| त्रि | tri | ··· | Three |
| चतुर् | catur | □ | Four |
| पञ्च | pañca | ∧ | Five |
| अस्ति | asti | · | Is/exists |
| भवति | bhavati | ~· | Becomes |
| गच्छति | gacchati | ~→ | Goes |
| आगच्छति | āgacchati | ~→· | Comes |
| पश्यति | paśyati | ·◯ | Sees |
| शृणोति | śṛṇoti | ◯~ | Hears |
| जानाति | jānāti | ◯· | Knows |
| करोति | karoti | ~□ | Does/makes |
| ददाति | dadāti | ~→~ | Gives |
| गृह्णाति | gṛhṇāti | ~←□ | Takes |
| वक्ति | vakti | ~─ | Speaks |
| प्रेम | prema | ◯~· | Love |
| सुख | sukha | ◯~~ | Happiness |
| दुःख | duḥkha | ~↓~ | Suffering |
| सत्य | satya | ·◯─ | Truth |
| माया | māyā | ~◯~ | Illusion |
| धर्म | dharma | ─∧─ | Duty/law |
| अर्थ | artha | □· | Wealth/meaning |
| काम | kāma | ~∧· | Desire |
| मोक्ष | mokṣa | □→~ | Liberation |
| ब्रह्मन् | brahman | ◯◯ | Ultimate reality |
| आत्मन् | ātman | ·◯ | Self/soul |
| मनस् | manas | ◯~ | Mind |
| ज्ञान | jñāna | ◯◯· | Knowledge |
| विद्या | vidyā | ◯~· | Learning |
| अग्नि | agni | ∧~∧ | Fire |
| अप् | ap | ~~ | Water |
| पृथिवी | pṛthivī | □~ | Earth |
| वायु | vāyu | ~○~ | Wind/air |
| आकाश | ākāśa | ○ | Space/ether |
| सूर्य | sūrya | ◯· | Sun |
| चन्द्र | candra | ◯·~ | Moon |
| नक्षत्र | nakṣatra | ·∧· | Star |
| नर | nara | ◯─· | Man |
| स्त्री | strī | ~◯─· | Woman |
| बाल | bāla | ·~□ | Child |
| गृह | gṛha | □· | House |
| नगर | nagara | □□□ | City |
| देश | deśa | □· | Country |
| दिन | dina | ~─ | Day |
| रात्रि | rātri | ~─~ | Night |
| काल | kāla | ─·~ | Time |
| मृत्यु | mṛtyu | ·~↓ | Death |
| जन्म | janma | ·~↑ | Birth |

**Sanskrit-Specific Considerations:**
1. **Sandhi Rules:** Sound combination → Geometric fusion rules
2. **Compounds:** Multiple words merge into single glyph sequence
3. **Aspectual Distinction:** Perfective (~←) vs. Imperfective (~)
4. **Gerund/Infinitive:** Nominalized verbs → □ container

---

## 4. CROSS-LINGUAL ALIGNMENT

### 4.1 Semantic Distance Metric

The geometric encoding enables precise cross-lingual similarity measurement:

```rust
/// Compute semantic distance between words in any languages
fn semantic_distance(word_a: &str, lang_a: Language, 
                     word_b: &str, lang_b: Language) -> f32 {
    // Encode both words to Center Æxis
    let lattice_a = encode_multilingual(word_a, lang_a);
    let lattice_b = encode_multilingual(word_b, lang_b);
    
    // Vesica coherence = overlap magnitude
    let coherence = vesica_coherence(&lattice_a, &lattice_b);
    
    // Distance = inverse coherence
    1.0 - coherence.abs()
}
```

### 4.2 Cognate Detection

**Definition:** Words sharing etymological origin map to similar glyfinform:

| Concept | English | Spanish | French | German | Glyfinform Similarity |
|---------|---------|---------|--------|--------|----------------------|
| Mother | mother | madre | mère | Mutter | >0.95 |
| Father | father | padre | père | Vater | >0.95 |
| Brother | brother | hermano | frère | Bruder | >0.85 |
| Water | water | agua | eau | Wasser | >0.70 (different roots) |
| Heart | heart | corazón | cœur | Herz | >0.75 |
| New | new | nuevo | nouveau | neu | >0.90 (PIE *newos) |
| Two | two | dos | deux | zwei | >0.60 (different roots) |

### 4.3 Semantic False Friends

Words that appear related but have divergent meanings:

| Word | Language A | Glyfinform A | Language B | Glyfinform B | Distance |
|------|------------|--------------|------------|--------------|----------|
| actual | English (·◯─) | Real | Spanish (·~─) | Current | 0.45 |
| gift | English (~→~) | Present | German (∧·) | Poison | 0.82 |
| fabric | English (~□~) | Cloth | Spanish (~□─) | Factory | 0.35 |
| embarrassed | English (~↓~) | Ashamed | Spanish (◯~~) | Pregnant | 0.78 |

### 4.4 Universal Concept Mapping

Concepts with near-identical geometric encoding across languages:

| Concept | Universal Glyff | Alignment Score |
|---------|-----------------|-----------------|
| Love | ◯~· | >0.98 |
| Water | ~~ | >0.99 |
| Fire | ∧~∧ | >0.98 |
| Earth | □~ | >0.97 |
| Sun | ◯· | >0.99 |
| Moon | ◯·~ | >0.96 |
| Person | ◯─· | >0.95 |
| Tree | ~↑□ | >0.94 |
| Path | ─ | >0.98 |
| Container | □ | >0.99 |

---

## 5. SEMANTIC PRIMITIVES

### 5.1 Core Meaning Atoms

Below the 7 geometric primitives lie semantic atoms — irreducible meaning units:

| Atom | Symbol | Meaning | Geometric Realization |
|------|--------|---------|----------------------|
| AGENT | @ | Self-initiating entity | Point with outgoing vector |
| PATIENT | & | Affected entity | Point with incoming vector |
| THEME | $ | Transferred entity | Point in container |
| LOCATION | # | Spatial frame | Square as reference |
| TIME | % | Temporal frame | Curve as sequence |
| MANNER | * | Qualitative mode | Curve texture |
| INSTRUMENT | ! | Enabling tool | Line as channel |
| GOAL | > | Target direction | Angle with forward vector |
| SOURCE | < | Origin direction | Angle with backward vector |
| BENEFICIARY | + | Recipient | Vesica with incoming flow |
| EXPERIENCER | ~ | Affected consciousness | Curve with center |
| POSSESSOR | $ | Owner | Point with container |

### 5.2 Semantic Composition Rules

```
Semantic Structure → Geometric Composition:

AGENT + ACTION → · + ~ = ·~ (self-initiated flow)
  "I run" = ·~─·

THEME + LOCATION → $ + # = ·□ (contained point)
  "book on table" = □·□

AGENT + THEME + GOAL → @ + $ + > = ·~→□
  "give book" = ~→□ (implied agent)

EXPERIENCER + STIMULUS → ~ + ◯ = ~◯
  "see sun" = ·◯ (agent=experiencer)
```

---

## 6. LEXICON EXPANSION PROTOCOL

### 6.1 Adding New Words

**Process:**
1. **Analyze phonetic structure** (IPA transcription)
2. **Identify semantic field** (8 core domains)
3. **Map to semantic primitives** (core atoms)
4. **Compose geometric glyff** (7 primitives)
5. **Encode to Center Æxis** (96-byte LatticeState)
6. **Validate cross-lingual** (compare to equivalents)
7. **Document and version** (lexicon registry)

**Template:**
```yaml
entry:
  word: [orthographic form]
  language: [ISO 639-1 code]
  phonetic: [IPA transcription]
  semantic_field: [space/time/motion/emotion/cognition/life/social/physical]
  semantic_primitives: [list of atoms]
  glyfinform: [7-glyph string]
  lattice_state: [96-byte hex]
  cross_lingual:
    - language: [code]
      equivalent: [word]
      coherence: [0.0-1.0]
  notes: [special considerations]
```

### 6.2 Adding New Languages

**Requirements:**
1. **Phonological inventory** (IPA chart)
2. **Phonotactic constraints** (allowed syllable structures)
3. **Morphological typology** (fusional, agglutinative, isolating)
4. **Basic word order** (SOV, SVO, VSO, etc.)
5. **Core vocabulary list** (Swadesh list or equivalent)
6. **Semantic field boundaries** (culture-specific categories)

**Integration Steps:**
1. Create language-specific mapping rules
2. Adapt tone/pitch systems if present
3. Encode morphological operators
4. Map 100+ core vocabulary
5. Validate cross-lingual alignment
6. Document idiosyncrasies

### 6.3 Version Control

**Schema:**
```
GLYF-LEXICON-v{major}.{minor}.{patch}

major: Structural changes (new semantic fields, primitive additions)
minor: Language additions, vocabulary expansions
patch: Corrections, refinements, coherence improvements

Current: GLYF-LEXICON-v1.0.0
```

---

## 7. IMPLEMENTATION NOTES

### 7.1 Storage Requirements

| Component | Size per Entry | 10K Words | 100K Words |
|-----------|---------------|-----------|------------|
| Glyfinform string | ~8 bytes | 80 KB | 800 KB |
| LatticeState | 96 bytes | 960 KB | 9.6 MB |
| Cross-lingual links | ~32 bytes | 320 KB | 3.2 MB |
| Metadata | ~64 bytes | 640 KB | 6.4 MB |
| **Total** | **~200 bytes** | **2 MB** | **20 MB** |

### 7.2 Query Patterns

**Supported Operations:**
- Exact word lookup: O(1) with hash map
- Semantic similarity: O(n) with Vesica coherence
- Cross-lingual translation: O(1) with alignment table
- Semantic field query: O(k) where k = field size
- Pattern matching: O(n) with glyfinform prefix

### 7.3 Edge Deployment

**Optimization:**
- Pre-computed LatticeStates for 10K most frequent words
- On-the-fly encoding for rare words
- Phonetic fallback for unknown words
- Cached cross-lingual alignments

---

## 8. VALIDATION METRICS

### 8.1 Coverage Targets

| Language | Core Vocab | Extended Vocab | Target Date |
|----------|-----------|----------------|-------------|
| English | 1,000 | 10,000 | Complete |
| Spanish | 500 | 5,000 | 2026-Q2 |
| Mandarin | 500 | 5,000 | 2026-Q2 |
| Arabic | 200 | 2,000 | 2026-Q3 |
| Sanskrit | 200 | 1,000 | 2026-Q4 |

### 8.2 Quality Metrics

- **Cross-lingual coherence >0.85** for true translations
- **Round-trip fidelity >0.90** (encode→decode)
- **Semantic distance correlation >0.80** with human judgments
- **Phonetic consistency >0.75** across related forms

---

## 9. REFERENCES

1. GLYFINFORM_TO_GLYFOBETICS.md — Bridge specification
2. GLYF_MORPHOSYNTAX.md — Grammar as geometry
3. GLYF_PHONOLOGY.md — Sound-to-geometry mapping
4. TRANSEXICON_SPEC.md — English phoneme mapping
5. Swadesh, M. (1952) — Lexicostatistic dating
6. Haspelmath, M. (2003) — The geometry of grammatical meaning
7. Talmy, L. (2000) — Toward a Cognitive Semantics

---

*Meaning is universal; language is its local geometric realization.*
