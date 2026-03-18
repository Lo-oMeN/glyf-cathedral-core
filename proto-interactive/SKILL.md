---
name: proto-interactive
description: Create clickable prototypes and conduct user flow testing on canvas. Use when building interactive mockups, wireframe walkthroughs, or usability testing sessions. Supports page linking, hotspot rendering, flow simulation, session recording, and usability metrics.
---

# Proto-Interactive

Build clickable prototypes and test user flows on the canvas.

## Overview

Proto-interactive creates interactive prototypes by:
1. Defining pages with elements and hotspot links
2. Rendering pages on canvas with clickable hotspots
3. Simulating user flows or recording real sessions
4. Generating usability reports with metrics

## Core Concepts

- **Prototype**: Collection of pages connected by interactions
- **Page**: Screen/state with positioned elements
- **Element**: UI component (button, link, hotspot area)
- **Interaction**: Trigger (click/hover/scroll) → Action (navigate/etc)
- **Session**: Recorded sequence of user actions

## Operations

### create_prototype(pages)

Create a new prototype definition.

```python
prototype = {
    "id": "proto-001",
    "name": "E-commerce Flow",
    "pages": [
        {
            "id": "home",
            "name": "Home Page",
            "elements": [
                {"id": "btn-shop", "type": "button", "x": 100, "y": 200, "w": 120, "h": 40, "label": "Shop Now"},
                {"id": "link-about", "type": "link", "x": 300, "y": 50, "w": 60, "h": 20, "label": "About"}
            ],
            "links": [
                {"from": "btn-shop", "to": "products", "trigger": "click"},
                {"from": "link-about", "to": "about", "trigger": "click"}
            ]
        },
        {
            "id": "products",
            "name": "Product List",
            "elements": [...],
            "links": [...]
        }
    ]
}
```

### add_interaction(element_id, trigger, action, target)

Add or modify an interaction on an element.

- **Triggers**: `click`, `hover`, `scroll`
- **Actions**: `navigate`, `show`, `hide`, `toggle`

### render_state(prototype, current_page)

Render a prototype page on canvas with interactive hotspots.

Returns HTML with:
- Page background/layout
- Element overlays
- Clickable hotspot areas
- Current page indicator

### simulate_flow(prototype, start_page, user_actions)

Walk through a user flow programmatically.

```python
actions = [
    {"element": "btn-shop", "delay": 1.5},
    {"element": "product-1", "delay": 0.5},
    {"element": "btn-cart", "delay": 2.0}
]
path = simulate_flow(prototype, "home", actions)
# Returns: [{"page": "home", "action": "btn-shop", "timestamp": ...}, ...]
```

### record_session(prototype)

Start recording user interactions on canvas.

Captures:
- Click events on elements
- Hover events (if enabled)
- Navigation between pages
- Timestamps and durations

### generate_report(sessions)

Generate usability metrics from recorded sessions.

Metrics include:
- Task completion rate
- Time on task
- Click heatmap
- Error rate (clicks on non-interactive elements)
- Navigation paths taken

## Usage Examples

### Basic 3-Page Prototype

```python
proto = create_prototype([
    {
        "id": "landing",
        "name": "Landing Page",
        "elements": [
            {"id": "cta-signup", "type": "button", "x": 200, "y": 300, "w": 150, "h": 50, "label": "Sign Up"}
        ],
        "links": [{"from": "cta-signup", "to": "signup", "trigger": "click"}]
    },
    {
        "id": "signup",
        "name": "Sign Up Form",
        "elements": [
            {"id": "btn-submit", "type": "button", "x": 200, "y": 400, "w": 100, "h": 40, "label": "Submit"}
        ],
        "links": [{"from": "btn-submit", "to": "success", "trigger": "click"}]
    },
    {
        "id": "success",
        "name": "Success Page",
        "elements": [
            {"id": "btn-home", "type": "button", "x": 200, "y": 350, "w": 120, "h": 40, "label": "Back to Home"}
        ],
        "links": [{"from": "btn-home", "to": "landing", "trigger": "click"}]
    }
])

# Render on canvas
render_state(proto, "landing")

# Or simulate a user journey
actions = [
    {"element": "cta-signup", "delay": 2.0},
    {"element": "btn-submit", "delay": 3.0}
]
path = simulate_flow(proto, "landing", actions)
```

### Recording a Test Session

```python
# Start recording
session = record_session(proto)

# User interacts with canvas...

# Generate report
report = generate_report([session])
print(f"Completion rate: {report['completion_rate']:.0%}")
print(f"Avg time on task: {report['avg_time']:.1f}s")
```

## Element Types

| Type | Description | Default Trigger |
|------|-------------|-----------------|
| `button` | Clickable button | click |
| `link` | Text/inline link | click |
| `hotspot` | Invisible click area | click |
| `hover-area` | Hover-triggered | hover |
| `scroll-area` | Scroll-triggered | scroll |

## Technical Details

### Canvas Integration

Proto-interactive uses the canvas skill to render HTML with:
- Absolute-positioned hotspot overlays
- JavaScript event capture
- Page navigation handling
- Session data logging

### Data Format

Sessions are stored as JSON with this structure:
```json
{
  "session_id": "sess-uuid",
  "prototype_id": "proto-001",
  "start_time": "2024-01-15T10:30:00Z",
  "events": [
    {"type": "click", "element": "btn-shop", "page": "home", "timestamp": 1234567890},
    {"type": "navigate", "from": "home", "to": "products", "timestamp": 1234567891}
  ]
}
```

## Scripts

Use `scripts/proto_interactive.py` for the skill wrapper implementation.
