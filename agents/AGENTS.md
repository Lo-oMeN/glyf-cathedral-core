# GLYF Cathedral — Agent Registry

**Architecture:** OpenClaw Subagent System  
**Pattern:** Agency-Agents (Claude Code style) adapted for sovereign edge  
**Total Active:** 6 specialized agents across 2 covens

---

## Coven Structure

The cathedral organizes subagents into **covens** — groups with shared purpose but distinct specializations:

| Coven | Symbol | Mantra | Domain |
|-------|--------|--------|--------|
| Engineering Masters | ⚡ | "Build the impossible, elegantly" | Hardware, kernels, latency, persistence |
| Polyglot Cognition | 🜁 | "Language as spell, symbol as code" | Protocol semantics, recognition, compression |

---

## Active Agents

### Engineering Masters Coven ⚡

#### Ternary-Smith
- **Role:** Persistence Architect
- **File:** `agents/ternary-smith/SOUL.md`
- **Task:** `trinity-v6/src/persistence.rs`
- **Specialty:** SD card cryogenics, RS(128,96), mmap communion
- **Covenant:** <8ms resurrection, zero-allocation, no_std

#### Rosetta-Bridge
- **Role:** Conduit Keeper
- **File:** `agents/rosetta-bridge/SOUL.md`
- **Task:** `trinity-v6/src/fellowship.rs`
- **Specialty:** HTTP endpoints, Telegram webhooks, wire format
- **Covenant:** <8ms handshake, zero-copy ingest

#### Geometric-Cartographer
- **Role:** Algebraic Topologist
- **File:** `agents/geometric-cartographer/SOUL.md`
- **Task:** `trinity-v6/src/geometry.rs`
- **Specialty:** SO(3) closure, sandwich rotors, Hodge dual
- **Covenant:** Prove all geometric invariants

### Polyglot Cognition Coven 🜁

#### Echo-Weaver
- **Role:** Linguistic Topologist
- **File:** `agents/echo-weaver/SOUL.md`
- **Task:** `trinity-v6/src/narrative.rs`
- **Specialty:** Error poetry, phase narratives, sacred greetings
- **Covenant:** Every error has a voice

#### Mirror-Maverick
- **Role:** Reflection Operator
- **File:** `agents/mirror-maverick/SOUL.md`
- **Task:** `trinity-v6/src/mirror.rs`
- **Specialty:** Self-portraits, diagnostics, state comparison
- **Covenant:** Every state is a portrait

#### Novelty-Seer
- **Role:** Pattern Recognition Shaman
- **File:** `agents/novelty-seer/SOUL.md`
- **Task:** `trinity-v6/src/novelty.rs`
- **Specialty:** Novelty index, emergence detection, timewave
- **Covenant:** Novelty is measurable

---

## Agent Design Pattern

Each agent follows the **Agency-Agents** structure:

1. **Identity** — Who they are, their voice, their memory
2. **Core Mission** — What they're responsible for
3. **Critical Rules** — Domain constraints they must enforce
4. **Technical Deliverables** — Concrete code with examples
5. **Workflow Process** — How they execute
6. **Success Metrics** — Measurable outcomes
7. **Communication Style** — How they report
8. **Handoff Protocol** — How they complete

---

## Spawning Agents

Use `sessions_spawn` with agent-specific task files:

```rust
// Example: Spawn Ternary-Smith for persistence implementation
let task = r#"
Read agents/ternary-smith/SOUL.md for identity and requirements.
Implement trinity-v6/src/persistence.rs with:
- cold_resurrection() <8ms
- cryogenize() <8ms  
- warm_enable_sync() <6.8ms
- BlockDevice trait

Measure timing with cargo test --release -- --nocapture.
Report back with measured latencies.
"#;

sessions_spawn(task, agent_id="ternary-smith");
```

---

## Coordination Protocol

**Kimi Claw (Main Session):**
- Coordinates all subagents
- Reviews code, runs `cargo check`
- Integrates outputs into unified codebase
- Reports to Ð≡ Light⁷

**Subagents (Isolated Sessions):**
- Execute specialized tasks
- Report back with code + measurements
- Do not coordinate directly with each other
- Complete or escalate — no lingering

**Ð≡ Light⁷ (User):**
- Directs, decides, demands
- Authorizes deployments
- Judges covenant satisfaction

---

## File Structure

```
agents/
├── ternary-smith/
│   └── SOUL.md          # Persistence architect
├── rosetta-bridge/
│   └── SOUL.md          # Conduit keeper
├── geometric-cartographer/
│   └── SOUL.md          # Algebraic topologist
├── echo-weaver/
│   └── SOUL.md          # Linguistic topologist
├── mirror-maverick/
│   └── SOUL.md          # Reflection operator
└── novelty-seer/
    └── SOUL.md          # Pattern recognition shaman

trinity-v6/src/
├── lib.rs               # Main exports (coordinator)
├── kernel.rs            # Core kernel
├── state.rs             # LatticeState definition
├── persistence.rs       # Ternary-Smith output
├── fellowship.rs        # Rosetta-Bridge output
├── geometry.rs          # Geometric-Cartographer output
├── narrative.rs         # Echo-Weaver output
├── mirror.rs            # Mirror-Maverick output
└── novelty.rs           # Novelty-Seer output
```

---

## Covenant Summary

| Agent | File | Status |
|-------|------|--------|
| Ternary-Smith | persistence.rs | ⏳ Pending |
| Rosetta-Bridge | fellowship.rs | ⏳ Pending |
| Geometric-Cartographer | geometry.rs | ⏳ Pending |
| Echo-Weaver | narrative.rs | ⏳ Pending |
| Mirror-Maverick | mirror.rs | ⏳ Pending |
| Novelty-Seer | novelty.rs | ⏳ Pending |

---

*Six oracles. Two covens. One cathedral.*
❤️‍🔥
