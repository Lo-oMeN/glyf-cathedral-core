# ACTIVE_PROJECTS.md — Ð≡ Light⁷'s Working Queue

**Last updated:** 2026-03-28  
**Status:** Live tracker — edit this to reorder/prioritize

---

## 🔥 URGENT / BLOCKING

*None currently — voice synthesis moved to back burner*

---

## 🔥 BACK BURNER (Deferred)

### Voice Synthesis — Neural Model Missing
- **Status:** 🔴 Deferred — not blocking current work
- **What exists:** ChristKey formant synth (abstract/vowel-like, not words)
- **What we need:** Neural TTS for intelligible speech (Female Alan Watts)
- **When to resume:** User provides model location OR we install Piper TTS
- **Context:** Dual-channel communication (text + audio) wanted but not blocking

---

## 🚧 IN PROGRESS

### GLYF Typing System
- **Status:** 🟡 Parser + converter functional, needs integration testing
- **Files:** `GlyfParser.kt`, `converter.py`
- **Next step:** End-to-end validation (text → GLYF → output)

### Trinity v6 Rust Kernel
- **Status:** 🟡 2/10 SO(3) operators complete
- **Completed:** Vesica, Phyllotaxis kernels
- **Remaining:** 8 operators + GF(256) Reed-Solomon
- **Blocked:** Pi Zero hardware (rpilocator alert needed)

### Cristdraline Framework Integration
- **Status:** 🟡 PDF received, analysis complete
- **Purpose:** 7-axis semantic alignment (Quadraline Dynamics)
- **NOT:** Voice model (different purpose than expected)
- **Next step:** Wire into GLYF semantic pipeline if desired

---

## 📋 QUEUED (Ordered by Priority)

### 1. Infrastructure Deployment
- **Task:** Deploy GLYF services on user's IP/server
- **Needs:** SSH access details, server specs
- **Depends on:** Voice model location resolved

### 2. Greek Lexeme Completion
- **Task:** Add remaining 3 Greek lexemes (χαρά, μακροθυμία, χρηστότης)
- **Context:** 11 of 14 complete in Cultural Atlas

### 3. Paraclete Keys
- **Task:** Add 9 remaining keys (seamless_gate through thorn_crown)

### 4. Metaphor Similarity Graph
- **Task:** Build shared sense.metaphors proximity mapping

### 5. WebSocket Bridge
- **Task:** Connect loom.html to Python core

### 6. Input Encoder Rebuild
- **Task:** 676 bigrams → trinary addresses

### 7. SD Card Persistence
- **Task:** MockBlockDevice → real SD implementation

---

## ✅ COMPLETED (Recent)

- **Threefold Seven-Type Glyfobetic Glyfo Form System** — Formal architecture document
- 96-byte LatticeState struct
- ChristKey formant synthesizer (abstract voice)
- GLYF parser + converter (multi-mode output)
- Rosetta-Bridge webhook endpoint
- Ternary-Smith RS correction
- Geometric-Cartographer SO(3) verification

---

## 🎯 HOW TO USE THIS FILE

**When overwhelmed:**
1. Read from top (URGENT → IN PROGRESS → QUEUED)
2. Pick ONE item from the highest non-empty category
3. Ignore everything else until it's done
4. Update status as you go

**To reprioritize:**
- Move items between sections
- Add 🔥 emoji to flag urgent items
- Add blocker notes under "Blocked by:"

**To add new work:**
- Append to QUEUED by default
- Only move up if it's truly blocking

---

## 📊 Current Workload

| Category | Count | Mental Load |
|----------|-------|-------------|
| URGENT | 1 | High |
| IN PROGRESS | 3 | Medium-High |
| QUEUED | 7 | Medium |
| **Total Active** | **11** | **Heavy** |

**Recommendation:** Close or defer 3+ QUEUED items before adding new work.

---

*"The board is full. Finish a piece before starting another."*

❤️‍🔥
