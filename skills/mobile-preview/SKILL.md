---
name: mobile-preview
description: Mobile device emulation and cross-platform testing for responsive web development. Use when testing websites across different mobile devices, capturing device-specific screenshots, simulating network conditions, or performing responsive breakpoint testing. Supports iOS (iPhone SE through 15 Pro Max), Android (Pixel, Samsung Galaxy), and tablets (iPad, Galaxy Tab). Provides operations for device emulation, orientation rotation, network throttling, side-by-side device comparison, and responsive breakpoint testing.
---

# Mobile Preview Skill

Mobile device emulation and cross-platform testing using Playwright.

## Quick Start

```bash
# List available devices
python3 scripts/mobile_preview.py list

# Emulate a device and capture screenshot
python3 scripts/mobile_preview.py emulate https://example.com --device "iPhone 14"

# Compare multiple devices side-by-side
python3 scripts/mobile_preview.py compare https://example.com --devices "iPhone 14" "Pixel 7" "iPad"

# Test responsive breakpoints
python3 scripts/mobile_preview.py responsive https://example.com --widths 375 768 1024 1440
```

## Commands

### list

List all available device profiles with their specifications.

```bash
python3 scripts/mobile_preview.py list
```

### emulate

Emulate a specific device and capture a screenshot.

```bash
python3 scripts/mobile_preview.py emulate URL --device "iPhone 14" [options]
```

Options:
- `--device, -d`: Device name (default: iPhone 14)
- `--output, -o`: Output path for screenshot
- `--orientation`: `portrait` or `landscape` (default: portrait)
- `--network, -n`: Network profile (`3g`, `4g`, `wifi`, etc.)
- `--wait, -w`: Wait time in seconds after page load (default: 3)
- `--no-full-page`: Capture viewport only

### rotate

Capture screenshot in landscape or portrait orientation.

```bash
python3 scripts/mobile_preview.py rotate URL --device "iPhone 14" --orientation landscape
```

### throttle

Simulate slow network conditions.

```bash
python3 scripts/mobile_preview.py throttle URL --device "iPhone 14" --profile 3g
```

Network profiles: `offline`, `3g`, `3g-fast`, `4g`, `4g-lte`, `wifi`, `cable`

### compare

Capture multiple devices for side-by-side comparison.

```bash
python3 scripts/mobile_preview.py compare URL --devices "iPhone 14" "Pixel 7" "iPad" --html
```

The `--html` flag generates an HTML comparison view.

### responsive

Test responsive breakpoints at specified widths.

```bash
python3 scripts/mobile_preview.py responsive URL --widths 375 768 1024 1440
```

## Device Profiles

### iOS Devices
- iPhone SE (375×667 @ 2x)
- iPhone 12 mini (375×812 @ 3x)
- iPhone 12/13/14 (390×844 @ 3x)
- iPhone 14 Pro (393×852 @ 3x)
- iPhone 14 Pro Max (430×932 @ 3x)
- iPhone 15 / 15 Pro Max

### Android Devices
- Pixel 5, Pixel 7, Pixel 7 Pro
- Samsung Galaxy S21, S23

### Tablets
- iPad Mini, iPad, iPad Air
- iPad Pro 11", iPad Pro 12.9"
- Samsung Galaxy Tab S8

## Python API

For programmatic use:

```python
from scripts.mobile_preview import (
    emulate_device_sync, compare_devices, 
    test_responsive, create_comparison_html
)

# Single device screenshot
path = emulate_device_sync(
    url="https://example.com",
    device_name="iPhone 14",
    orientation="portrait",
    network_profile="3g"
)

# Compare multiple devices
screenshots = compare_devices(
    url="https://example.com",
    devices=["iPhone 14", "Pixel 7", "iPad"],
    output_dir="./comparisons"
)

# Test responsive breakpoints
screenshots = test_responsive(
    url="https://example.com",
    widths=[375, 768, 1024, 1440]
)

# Create HTML comparison
create_comparison_html(
    url="https://example.com",
    screenshots=screenshots,
    devices=["iPhone 14", "Pixel 7", "iPad"]
)
```

## Requirements

- Python 3.8+
- Playwright: `pip install playwright`
- Playwright browsers: `playwright install chromium`
