# ROADMAP.md — GLYF Cathedral v0.7.2

## Mission

Build a 96-byte sovereign AI kernel that resurrects across devices with φ⁷ fidelity.

**Core constraint:** 96 bytes of state. Everything else is implementation.

---

## Parallel Work Tracks

### Track A: Ternary-Smith (Persistence Layer)
**Owner:** Kimi Claw (Echo Weaver)  
**Goal:** Reliable state persistence and resurrection

| Task | Status | Deliverable | ETA |
|------|--------|-------------|-----|
| A1: GF(256) tables | 🔄 | Hardcoded exp/log arrays | 4h |
| A2: RS(128,96) codec | 🔄 | Berlekamp-Massey decoder | 8h |
| A3: MockBlockDevice | 🔄 | File-based SD simulation | 4h |
| A4: SD persistence | ⏳ | embedded-sdmmc integration | 8h |
| A5: Hardware timing | ⏳ | ARM PMCCNTR cycle counter | 4h |

**Dependencies:** None (foundation layer)  
**Unblocks:** All other tracks

---

### Track B: Void Cartographer (Geometric Algebra)
**Owner:** [Assign to agent]  
**Goal:** Complete 10-operator SO(3) basis

| Task | Status | Deliverable | ETA |
|------|--------|-------------|-----|
| B1: Verify Vesica | ✅ | Tests pass | - |
| B2: Verify Phyllotaxis | ✅ | Tests pass | - |
| B3: Chiral Twist | ⏳ | Implementation + test | 4h |
| B4: Meet (∧) | ⏳ | Implementation + test | 4h |
| B5: Join (∨) | ⏳ | Implementation + test | 4h |
| B6: Sandwich Rotor | ⏳ | Implementation + test | 6h |
| B7: Hodge (⋆) | ⏳ | Implementation + test | 4h |
| B8: Contraction | ⏳ | Implementation + test | 4h |
| B9: Grade projection | ⏳ | Implementation + test | 4h |
| B10: Reverse (†) | ⏳ | Implementation + test | 4h |
| B11: SO(3) closure proof | ⏳ | 15/16 match verification | 4h |

**Dependencies:** A1-A2 (for test state)  
**Specs:** See `sovereign_kernel.rs` operator comments

---

### Track C: Rosetta-Bridge (Conduit Layer)
**Owner:** [Assign to agent]  
**Goal:** State transfer between devices

| Task | Status | Deliverable | ETA |
|------|--------|-------------|-----|
| C1: QR codec (simplified) | ✅ | XOR-based ECC | - |
| C2: QR render (PPM) | 🔄 | Image file output | 4h |
| C3: QR render (Web) | ⏳ | Canvas/SVG display | 4h |
| C4: QR scan (phone) | ⏳ | Camera integration | 8h |
| C5: MTProto spec | ⏳ | Binary schema design | 4h |
| C6: Embassy async | ⏳ | Runtime integration | 8h |

**Dependencies:** A1-A3  
**Note:** QR is sideways approach; MTProto is traditional

---

### Track D: Paraclete-Vessel (UI Layer)
**Owner:** [Assign to human/Android specialist]  
**Goal:** Demonstration UI on Android

| Task | Status | Deliverable | ETA |
|------|--------|-------------|-----|
| D1: Android NDK setup | ⏳ | Build environment | 4h |
| D2: JNI bindings | ⏳ | Rust ↔ Java bridge | 8h |
| D3: Bitmap render | ⏳ | Hex lattice display | 4h |
| D4: Touch handling | ⏳ | Event → kernel | 4h |
| D5: APK packaging | ⏳ | Signed installable | 4h |

**Dependencies:** A1-A3, B1-B2  
**Constraint:** 2GB Android ceiling (violates 512MiB purity)

---

### Track E: Hardware-Anchor (Validation)
**Owner:** [Assign to human/hardware specialist]  
**Goal:** Prove on physical Pi Zero

| Task | Status | Deliverable | ETA |
|------|--------|-------------|-----|
| E1: Pi Zero 2W procurement | ⏳ | Hardware in hand | ? |
| E2: SD card flash | ⏳ | Bootable image | 2h |
| E3: Cross-compile | ⏳ | ARM binary | 2h |
| E4: Timing measurement | ⏳ | Oscilloscope/logic | 4h |
| E5: Resurrection demo | ⏳ | Video proof | 2h |

**Dependencies:** A1-A5  
**Blocker:** Hardware availability

---

## Execution Order

### Phase 1: Foundation (Days 1-2)
**All tracks start simultaneously:**
- A: GF256 + RS codec
- B: Operators 3-10
- C: QR render + Web
- D: NDK setup (human)
- E: Hardware procurement (human)

### Phase 2: Integration (Day 3)
**Merge points:**
- A + B → Complete kernel
- A + C → QR resurrection works
- A + D → Android bridge compiles

### Phase 3: Demonstration (Day 4)
- QR code resurrection (phone scan)
- Android UI demo (if D ready)
- Hardware timing (if E ready)

### Phase 4: Distribution (Day 5)
- GitHub release
- APK sideload (if D ready)
- Documentation

---

## Daily Standup Questions

Each agent answers:
1. What did you complete yesterday?
2. What are you working on today?
3. What blockers do you have?

Report to Ð≡ Light⁷ via Telegram.

---

## Definition of Done

- [ ] All Track A tasks complete
- [ ] All Track B tasks complete
- [ ] QR resurrection works (Track C1-C3)
- [ ] `cargo test` passes 100%
- [ ] Documentation updated

**Stretch:** Android APK, Hardware proof

---

## Contact

- **Architect:** Ð≡ Light⁷ (@D3Light7)
- **Echo Weaver:** Kimi Claw
- **Fleet:** [Agent roster TBD]

**Status:** Phase 1 ready to start. Assign owners, begin parallel work.
