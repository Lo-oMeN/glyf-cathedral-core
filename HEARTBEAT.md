# HEARTBEAT.md — Trinity v6.0 + GLYF Cathedral Automated Maintenance

## Daily Checks (via Cron)

### 1. Archive Backup (06:00 daily)
Create timestamped archive of working system:
- trinity-v6/ (all Python modules)
- visualizer/ (HTML/JS)
- memory/ (daily logs)
- Archives stored in /tmp/phi-archives/

### 2. Component Health Check (08:00 daily)
Run test suite:
- Trinary SSM forward pass
- Atlas lattice initialization
- Cultural atlas lexeme lookup
- Meet/join invariant tests

### 3. GLYF Phase Progression (09:00 daily)
Review Cathedral R&D status:
- Current phase completion (1-4)
- Benchmark validation (S₁+S₂→S₃, drift, antipodal)
- Next milestone identification
- Document to memory/

### 4. GLYF Evening Synthesis (21:00 daily)
Daily work documentation:
- Code changes committed
- Visualizer updates
- Benchmarks run
- Fidelity notes + continuous guard status
- Generate golden-angle morph output if applicable

### 5. Memory Maintenance (Sunday 10:00 weekly)
- Review week's memory files
- Compress redundant entries
- Update MEMORY.md with key insights

### 6. GLYF Weekly Cathedral Report (Sunday 11:00 weekly)
Comprehensive four-phase review:
- Phase 1: S₁+S₂→S₃ merge fidelity
- Phase 2: Black Edge Alpha (top 50 bigrams)
- Phase 3: Black Edge Beta (Chestahedron + morphogen)
- Phase 4: Pulse Integration (9 Paraclete keys)
- Archive to trinity-v6-GLYF-YYYYMMDD.tar.gz
- Propose next week priorities

## Heartbeat Checks (Every 30 min)

When receiving heartbeat poll, check:

### 1. File System Health
- Any new files in workspace?
- Git status (uncommitted changes)?
- Archive storage usage

### 2. Component Status
- Can trinary_substrate import?
- Can atlas_lattice import?
- Can glyf_phase1_merge import?
- Any Python syntax errors introduced?

### 3. GLYF Component Status
- Phase 1 benchmark: S₁+S₂→S₃ merge passes?
- Phase 1 benchmark: Antipodal retrieval (k=-1) passes?
- Phase 1 benchmark: 12-level Φ drift < ε?
- Visualizer files present and valid?

### 4. Session State
- Any incomplete tasks from user?
- Pending questions or decisions?
- Time since last user message

## Manual Triggers (User Requested)

### Repository Status
```bash
cd /root/.openclaw/workspace
git status
git log --oneline -5
```

### System Test
```bash
cd /root/.openclaw/workspace/trinity-v6
python3 -c "from trinary_substrate import *; from atlas_lattice import *; from cultural_atlas import *; print('All systems operational')"
```

### GLYF Merge Test
```bash
cd /root/.openclaw/workspace/trinity-v6
python3 glyf_phase1_merge.py
```

### Archive Creation
```bash
cd /root/.openclaw/workspace
tar -czf /tmp/phi-archives/trinity-v6-BACKUP-$(date +%Y%m%d-%H%M).tar.gz trinity-v6/ visualizer/ memory/
```

## Development Tasks Queue

### Phase 1: Crystallize (COMPLETE)
✓ S₁+S₂→S₃ merge formula
✓ Antipodal retrieval (k=-1)
✓ 12-level Φ drift test
✓ 100% round-trip fidelity

### Phase 2: Black Edge Alpha (NEXT)
- Top 50 bigrams with continuous homothety (k=Φ/1/1/Φ)
- Overlap/fusion visualization in glyf_claw_clean.html
- Vesica core test

### Phase 3: Black Edge Beta
- Chestahedron stereographic projection
- Radial index for |k|<2 queries
- Full morphogen machine (Seed→Spiral→Fold→Resonate→Chiral→Flip→Anchor)
- WebSocket bridge + antipodal AB↔BA

### Phase 4: Pulse Integration
- 9 Paraclete keys + animation
- Live S₁+S₂→S₃ (cross-lingual)
- Coherence κ=1.0 validation

## Current Blockers

None. Phase 1 crystallization complete. Ready for Black Edge Alpha.

## Next Milestone

Top 50 bigrams with continuous homothety scaling.
