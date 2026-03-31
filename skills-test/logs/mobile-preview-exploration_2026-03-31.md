# Skill Exploration: mobile-preview
**Date:** 2026-03-31 18:40 CST  
**Exploration Type:** Documented capabilities review (no validation script found)

---

## Skill Overview
Mobile device emulation and cross-platform testing using Playwright. Supports iOS, Android, and tablet device profiles for responsive web testing.

## Capabilities Discovered

### Core Operations
| Command | Purpose | Status |
|---------|---------|--------|
| `list` | List all device profiles | ✅ Available |
| `emulate` | Single device screenshot | ✅ Available |
| `rotate` | Orientation switching | ✅ Available |
| `throttle` | Network simulation | ✅ Available |
| `compare` | Side-by-side device shots | ✅ Available |
| `responsive` | Breakpoint testing | ✅ Available |

### Device Coverage
**iOS:** iPhone SE → iPhone 15 Pro Max (full range)  
**Android:** Pixel 5-7 series, Galaxy S21/S23  
**Tablets:** iPad Mini/Pro, Galaxy Tab S8  

### Key Technical Details
- Requires Playwright + Chromium
- Network profiles: offline/3g/4g/wifi/cable
- Orientation: portrait/landscape
- Can generate HTML comparison views

---

## Integration Notes for Cathedral
This skill enables **device-agnostic GLYF visualization testing** — critical for verifying the Looman experience across the Android fleet (Galaxy A03s as primary target).

### Potential Use Cases
1. Screenshot cathedral UI at 375×667 (iPhone SE) vs 430×932 (iPhone 14 Pro Max)
2. Network throttling to validate "offline-first" sovereign mesh
3. Responsive breakpoint testing for φ-harmonic layouts

---

## Missing Validation
No `validate.py` script found in skill directory. Recommend adding:
- Playwright installation check
- Sample emulation test (e.g., `https://example.com` on iPhone 14)
- Network profile verification

---

## Files Referenced
- `skills/mobile-preview/SKILL.md`
