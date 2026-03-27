# Galaxy A03s Stress Test Protocol
## L∞M∆N φ⁶ Edition — Hardware Validation

**Device:** Samsung Galaxy A03s  
**Target:** 2-3GB RAM, Exynos 850, 720p 60Hz  
**Test Date:** ___________  
**Tester:** Ð≡ Light⁷

---

## Pre-Flight: Device Prep (2 minutes)

1. **Enable Developer Mode**
   - Settings → About phone → Software information
   - Tap "Build number" 7 times

2. **Enable USB Debugging**
   - Settings → Developer options
   - Toggle "USB debugging"

3. **Connect & Authorize**
   - Plug USB cable
   - Tap "Allow" on RSA key prompt
   - Verify: `adb devices` shows device

---

## Phase 1: Cold Resurrection Timing

### Test: First Launch After Install

```bash
# Fresh install
adb install -r app-debug.apk

# Kill any existing process
adb shell am force-stop com.loom.app

# Cold launch with timing
adb shell am start -W -n com.loom.app/.MainActivity
```

**Expected Output:**
```
Starting: Intent { cmp=com.loom.app/.MainActivity }
Status: ok
Activity: com.loom.app/.MainActivity
ThisTime: XXX  <-- RECORD THIS (ms)
TotalTime: XXX
WaitTime: XXX
```

**Benchmark:**
- Target: <500ms ThisTime (cold start to visible)
- Stretch: <200ms (JVM benchmark was 7.93ms — ART will be slower)

**Log Check:**
```bash
adb logcat -d | grep "L∞M∆N"
```

**Expected:**
```
I/L∞M∆N: Resurrection: source=none, time=0.XXXms, total=XXX.XXXms
```

Record:
- [ ] Cold resurrection time: _____ ms
- [ ] Log shows "source=none" (expected on first launch)

---

## Phase 2: Background Survival Test

### Test: State Persistence Under Memory Pressure

```bash
# 1. Launch app, let it run 10 seconds
adb shell am start -n com.loom.app/.MainActivity
sleep 10

# 2. Background the app
adb shell input keyevent KEYCODE_HOME

# 3. Open 5 heavy apps to trigger memory pressure
adb shell am start -n com.android.camera/.Camera
sleep 2
adb shell am start -a android.intent.action.VIEW -d "https://youtube.com"
sleep 2
adb shell am start -n com.google.android.apps.maps/com.google.android.maps.MapsActivity
sleep 2
# Add 2 more heavy apps here

# 4. Return to Looman
adb shell am start -n com.loom.app/.MainActivity

# 5. Check logs
adb logcat -d | grep "L∞M∆N"
```

**Expected:**
```
I/L∞M∆N: Resurrection: source=bundle, time=0.XXXms, total=XXX.XXXms
```

OR

```
I/L∞M∆N: Resurrection: source=disk, time=0.XXXms, total=XXX.XXXms
```

**FAILURE MODE:**
- If log shows "source=none" — Samsung's killer wiped the app
- Check if state was at least preserved via disk cryogenics

Record:
- [ ] Resurrection source: _____ (bundle/disk/none)
- [ ] Warm resurrection time: _____ ms
- [ ] State survived: Y/N

---

## Phase 3: Frame Pacing (60 FPS Validation)

### Test: Visualizer Performance

```bash
# Launch app
adb shell am start -n com.loom.app/.MainActivity

# Let it run 30 seconds
sleep 30

# Capture frame stats
adb shell dumpsys gfxinfo com.loom.app | grep -A 20 "Profile"
```

**Expected Output:**
```
** Graphics info for pid [XXXX] [com.loom.app] **

Stats since: XXXXXXXns
Total frames rendered: XXX
Janky frames: XX (X.XX%)
50th percentile: XXms
90th percentile: XXms
95th percentile: XXms
99th percentile: XXms
```

**Benchmark:**
- Target: <5% janky frames
- Target: 90th percentile <16.67ms (60 FPS)
- Stretch: 99th percentile <33ms (30 FPS worst case)

Record:
- [ ] Total frames: _____
- [ ] Janky frames: _____ (%)
- [ ] 90th percentile: _____ ms
- [ ] App displayed FPS: _____ (from UI overlay)

---

## Phase 4: Thermal Throttling

### Test: Sustained Load

```bash
# Launch and monitor for 5 minutes
adb shell am start -n com.loom.app/.MainActivity

# Every 60 seconds, capture:
for i in {1..5}; do
    sleep 60
    echo "=== Minute $i ==="
    adb shell dumpsys gfxinfo com.loom.app | grep "Janky frames"
    adb shell cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null | head -5
    adb logcat -d | grep "L∞M∆N" | tail -3
done
```

**Watch for:**
- FPS drop over time (thermal throttling)
- Increasing janky frame percentage
- High thermal zone temps (>60°C)

Record:
- [ ] Minute 1 FPS: _____
- [ ] Minute 3 FPS: _____
- [ ] Minute 5 FPS: _____
- [ ] Thermal throttling detected: Y/N

---

## Phase 5: 96-Byte Integrity

### Test: State Verification

After each resurrection, verify:

1. **Energy continuity** — Does the energy value persist?
2. **Harmonic continuity** — Do the 8 harmonics maintain their values?
3. **Timestamp progression** — Does time advance correctly?

**Manual check:**
- Note Energy value before backgrounding
- Trigger memory pressure
- Return to app
- Verify Energy is preserved (not reset to 1.0)

Record:
- [ ] Energy preserved: Y/N
- [ ] Harmonics preserved: Y/N
- [ ] Timestamp advanced: Y/N

---

## Results Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Cold resurrection | <500ms | | |
| Warm resurrection | <100ms | | |
| Janky frames | <5% | | |
| 90th percentile | <16.67ms | | |
| State survival | 100% | | |
| Thermal stable (5min) | Y | | |

**Overall:** PASS / NEEDS WORK / FAIL

---

## Failure Modes & Mitigations

### If Samsung kills the app:
- **Mitigation:** Implement foreground Service
- **Test:** Add `adb shell am startservice -n com.loom.app/.LatticeService`

### If resurrection is slow (>100ms warm):
- **Check:** Disk I/O speed on A03s
- **Mitigation:** Async cryogenize, keep in memory + disk

### If FPS is poor (>10% janky):
- **Check:** GPU load with `adb shell dumpsys meminfo`
- **Mitigation:** Reduce particle count, simplify shaders

---

## Raw Log Dump

(Paste adb logcat output here)

```

```

---

**Tested by:** ___________  
**Date:** ___________  
**Notes:**

