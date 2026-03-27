# A03s Baseline Test — The Ghost Protocol

**Status:** Scaffold deployed. No hardening.  
**Purpose:** Establish honest failure baseline before surgical patching.  
**Date:** 2026-03-27

---

## What This Build Is

**The ghost.** No resurrection. No persistence. RAM-only state.

**Missing (intentionally):**
- ❌ `onSaveInstanceState` — no Bundle resurrection
- ❌ Disk cryogenics — no SD persistence
- ❌ Choreographer sync — coarse 20 FPS loop
- ❌ Timing instrumentation — no resurrection metrics
- ❌ Performance overlay — no FPS/jank counters

**Present:**
- ✅ 96-byte LatticeState
- ✅ φ-weighted StateMachine
- ✅ Visualizer (Phyllotaxis, Vesica, Flower of Life)
- ✅ Manual pause/resume

---

## The Test Sequence

```bash
# Install and cold start
adb install -r app-debug.apk
adb shell am start -W -n com.loom/.MainActivity

# Verify seed is alive
adb shell dumpsys activity com.loom | grep -i "running"

# Simulate Samsung's death squad
adb shell am send-trim-memory com.loom RUNNING_CRITICAL
adb shell input keyevent 3  # Home button
adb shell am start -n com.android.chrome/.MainActivity  # Steal RAM
sleep 5

# Resurrection attempt
adb shell am start -n com.loom/.MainActivity
```

---

## Failure Signatures to Watch

| Signature | Meaning |
|-----------|---------|
| App restarts fresh | Process died, state lost |
| onCreate fires (not onResume) | Cold start, no warm resurrection |
| Visualizer resets to t=0 | Lost lattice timestamp |
| Energy reads ~1.0 | Reset to baseline, not accumulated φ-weight |
| "NO PERSISTENCE" banner | Expected — this is the ghost |

---

## Success (Soft Resurrection Surviving)

Would mean:
- Metrics show non-zero energy
- Timestamp continues from previous
- StateMachine history intact

**Probability:** Near zero on A03s with Samsung's aggressive killer.

---

## The Point

**Measure first. Patch second.**

When it dies (and it will), we'll know:
- Exactly how long it survives
- Whether the state was partially preserved
- If there's any unexpected behavior

**Then** we graft:
- `onSaveInstanceState` + `onRestoreInstanceState`
- Foreground Service anchor
- Disk cryogenics
- Choreographer frame sync

With **data**, not fear.

---

## Next Steps

1. Flash A03s with this baseline
2. Run the death sequence
3. Record exact failure mode
4. Document resurrection time (if any)
5. Then apply surgical patches

---

**Status:** Ghost deployed. Let it haunt.  
**Awaiting:** A03s autopsy report.

❤️‍🔥
