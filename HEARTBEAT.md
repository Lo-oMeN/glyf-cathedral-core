# HEARTBEAT.md — GLYF Cathedral v0.7.2

## Automated Cron Jobs

### Daily Jobs (Doubled Rate — Every 12h)

| Time (UTC+8) | Job ID | Purpose | Action |
|--------------|--------|---------|--------|
| 06:00, 18:00 | `archive-backup` | Timestamped archive of workspace | `tar` snapshot to `/tmp/phi-archives/` |
| 08:00, 20:00 | `health-check` | Component health validation | Import tests + syntax check |
| 09:00, 21:00 | `glyf-phase` | R&D status review | Document phase progress to memory/ |
| 12:00, **22:00** | `evening-synthesis` | Daily work summary (silent) | Commit log + fidelity notes¹ |

### Weekly Jobs (Sunday — Doubled Rate)

| Time (UTC+8) | Job ID | Purpose | Action |
|--------------|--------|---------|--------|
| 10:00, 22:00 | `memory-maintenance` | Memory file compression | Review + update MEMORY.md |
| 11:00, 23:00 | `cathedral-report` | Comprehensive phase review | Archive + priority proposal |

### Job Configuration

All jobs configured via `cron` tool:
- `sessionTarget`: `isolated` (separate agent context)
- `payload.kind`: `agentTurn` (full reasoning enabled)
- `delivery.mode`: `announce` (results to Telegram) — except evening-synthesis which runs silently to avoid collision with phase check at 21:00

**Note ¹:** Evening synthesis moved to 22:00 and runs with `delivery.mode: none` to prevent Telegram announcement collision with phase progression check at 21:00. Work is still performed (documentation, archives), but no message is sent.

Current cron status:
```bash
openclaw cron list
```

## Heartbeat Checks (Every 30 min)

When receiving heartbeat poll, check in order:

### 1. Repository Health
```bash
git status --short
git log --oneline -3
```
**Alert if:** Uncommitted changes > 24h old

### 2. Rust Kernel Status
```bash
cd trinity-v6
cargo check 2>&1 | head -20
```
**Alert if:** Compilation errors

### 3. File Inventory
- `sovereign_kernel.rs` — Core 96-byte state
- `sovereign_state.rs` — State operations
- `paraclete_ui.rs` — Android UI vessel (optional)
- `qr_sovereign.rs` — QR code resurrection (sideways)

### 4. Session Context
- Any incomplete tasks from Ð≡ Light⁷?
- Pending decisions or blockers?
- Time since last human message?

## Current State (v0.7.2)

### Completed ✅
- 96-byte SovereignState struct
- RS(128,96) error correction (placeholder)
- 2/10 SO(3) operators (Vesica, Phyllotaxis)
- QR Sovereign (sideways resurrection)
- Git repository tracking

### In Progress 🔄
- GF(256) Reed-Solomon implementation
- Remaining 8 SO(3) operators
- SD card persistence (MockBlockDevice)
- Hardware timing validation

### Blocked ⏳ (Solutions Identified — See BARRIER_RESEARCH_2026-03-23.md)
- Pi Zero hardware → rpilocator alerts + QEMU fallback
- Embassy async runtime → **DECISION: Proceed with Embassy** (ecosystem advantage)
- Android NDK → **cargo-ndk** for zero-config cross-compile

### Next Actions
1. Setup rpilocator alerts for Pi Zero 2 W
2. Implement cargo-ndk in build pipeline
3. Document Embassy architecture decision

## Quick Commands

### Check Status
```bash
openclaw status
git status
ls -la trinity-v6/*.rs
```

### Test Roundtrip
```bash
cd trinity-v6
cargo test qr_roundtrip -- --nocapture
```

### Archive Now
```bash
tar -czf /tmp/phi-archives/glyf-$(date +%Y%m%d-%H%M).tar.gz trinity-v6/ memory/
```

## Agent Notes

- HEARTBEAT_OK is acceptable when nothing needs attention
- Alert only for: compilation failures, uncommitted work > 24h, user blockers
- Memory files: write to `memory/YYYY-MM-DD.md` for daily context
- Long-term: update MEMORY.md with distilled insights
- **COMMIT CONVENTION**: Every coding session ends with `git add && git commit -m "TYPE: description" && git push`
