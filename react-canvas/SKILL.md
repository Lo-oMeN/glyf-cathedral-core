---
name: react-canvas
description: Render React components to PNG/SVG images and display them in the OpenClaw Canvas. Supports JSX code rendering, component file rendering, template scaffolding, hot reload, and visual diff comparison. Use when users want to (1) visualize React components as images, (2) render JSX code to screenshots, (3) create component templates, (4) compare component versions visually, (5) develop components with hot reload, or (6) use UI libraries like Tailwind, Chakra UI, or Material-UI in rendered output.
---

# React Canvas

Render React components to PNG/SVG images and display them in the OpenClaw Canvas.

## Capabilities

- **Render JSX code** directly to images
- **Render component files** (.jsx/.tsx)
- **Create component templates** (functional, class, arrow)
- **Hot reload** for development
- **Visual diff** comparison between versions
- **UI library support**: Tailwind CSS, Chakra UI, Material-UI
- **Canvas integration** for live preview

## Quick Start

### Render JSX Code to Image

```bash
node scripts/render_component.js --code "<div style={{padding:20}}>Hello</div>" -o hello.png
```

Or via stdin:

```bash
echo '<div className="p-4 bg-blue-500">Hello</div>' | node scripts/render_component.js -o hello.png
```

### Render Component File

```bash
node scripts/render_from_file.js ./components/Button.jsx --props '{"text":"Click"}' -o button.png
```

### Create Component Template

```bash
node scripts/create_template.js UserCard -t functional -p name,email -u tailwind
```

### Hot Reload Development

```bash
node scripts/hot_reload.js ./components/Chart.jsx -w 1200 -h 800
```

### Compare Versions

```bash
node scripts/compare_versions.js ./Button-v1.jsx ./Button-v2.jsx -f diff -o comparison.png
```

## Operations Reference

See [references/operations.md](references/operations.md) for detailed API documentation.

### render_component(jsx_code, props={}, width=800, height=600)

Renders JSX code string to PNG/SVG.

**Options:**
- `--code, -c`: JSX code string
- `--props, -p`: JSON props object
- `--width, -w`: Output width (default: 800)
- `--height, -h`: Output height (default: 600)
- `--format, -f`: png or svg (default: png)
- `--output, -o`: Output file path
- `--ui-lib, -u`: tailwind|chakra|material-ui
- `--canvas, -C`: Also save to canvas directory

### render_from_file(component_path, props)

Renders a component from file.

**Options:**
- Same as render_component plus:
- File path as first positional argument

### create_component_template(name, template='functional')

Creates a new component scaffold.

**Options:**
- `--template, -t`: functional|class|arrow (default: functional)
- `--output, -o`: Output directory (default: ./components)
- `--ui-lib, -u`: UI library preset
- `--props, -p`: Comma-separated prop names
- `--overwrite, -f`: Overwrite existing file

### hot_reload(file_path)

Watches file and re-renders on changes.

**Options:**
- `--props, -p`: Initial props
- `--width, -w`: Canvas width
- `--height, -h`: Canvas height
- `--debounce, -d`: Debounce ms (default: 500)

### compare_versions(component_v1, component_v2)

Visual diff between two components.

**Options:**
- `--format, -f`: side-by-side|overlay|diff (default: side-by-side)
- `--width, -w`: Component width
- `--height, -h`: Component height

## UI Library Support

### Tailwind CSS

Use Tailwind utility classes directly:

```jsx
<div className="p-4 bg-blue-500 text-white rounded-lg shadow-md">
  Tailwind styled content
</div>
```

Enable with: `--ui-lib tailwind`

### Chakra UI

Components are automatically wrapped with ChakraProvider:

```jsx
import { Box, Button, Stack } from '@chakra-ui/react';

export default function MyComponent() {
  return (
    <Stack spacing={4}>
      <Button colorScheme="blue">Primary</Button>
      <Button variant="ghost">Ghost</Button>
    </Stack>
  );
}
```

Enable with: `--ui-lib chakra`

### Material-UI

Components are automatically wrapped with ThemeProvider:

```jsx
import { Button, Paper, Typography } from '@mui/material';

export default function MyComponent() {
  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <Typography variant="h6">Title</Typography>
      <Button variant="contained">Click</Button>
    </Paper>
  );
}
```

Enable with: `--ui-lib material-ui`

## Canvas Integration

The skill integrates with the OpenClaw Canvas system:

1. Renders are saved to `~/clawd/canvas/` by default
2. Use `--canvas` flag to automatically save renders there
3. Canvas files can be viewed on connected nodes via `canvas action:present`

### View on Canvas

```bash
# Render and save to canvas
node scripts/render_component.js --code "<div>Hello</div>" --canvas

# Then present on a node
canvas action:present node:<node-id> target:http://<host>:18793/__openclaw__/canvas/react-canvas-render.html
```

## Installation

### 1. Install Dependencies

```bash
cd scripts
npm install
```

Required packages:
- `esbuild`: Fast bundling
- `puppeteer`: Headless browser rendering
- `canvas`: Image manipulation for diff

### 2. Optional UI Libraries

```bash
npm install tailwindcss @chakra-ui/react @emotion/react @emotion/styled framer-motion @mui/material @mui/icons-material
```

### 3. Make Scripts Executable

```bash
chmod +x scripts/*.js
```

## Examples

### Simple Card Component

```bash
node scripts/create_template.js Card -p title,description -u tailwind
```

Generates:
```jsx
const Card = ({ title, description }) => {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
};
```

### Render with Props

```bash
node scripts/render_from_file.js ./components/Card.jsx \
  -p '{"title":"Welcome","description":"Hello World"}' \
  -w 400 -h 300 -o card.png
```

### Dashboard Hot Reload

```bash
node scripts/hot_reload.js ./components/Dashboard.jsx \
  -w 1400 -h 900 -p '{"data":[]}'
```

### Visual Regression Testing

```bash
# Compare before/after changes
node scripts/compare_versions.js \
  ./Button.old.jsx ./Button.new.jsx \
  -f diff -o button-changes.png
```

## Troubleshooting

### White/Blank Output

- Check JSX syntax is valid
- Ensure component returns a single root element
- Try increasing wait time with `--wait 2000`

### Module Not Found

Install missing dependencies:
```bash
cd scripts && npm install
```

### Chromium Issues

Puppeteer downloads Chromium automatically. If it fails:

```bash
# Install Chromium manually and set path
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
```

### Canvas Not Updating

Ensure `liveReload: true` in `~/.openclaw/openclaw.json`:

```json
{
  "canvasHost": {
    "enabled": true,
    "liveReload": true,
    "root": "/root/clawd/canvas"
  }
}
```

## Environment Variables

- `REACT_CANVAS_ROOT`: Canvas output directory (default: ~/clawd/canvas)
- `PUPPETEER_EXECUTABLE_PATH`: Custom Chromium path
- `DEBUG`: Enable verbose logging

## Architecture

```
JSX Code → Esbuild Bundle → HTML Wrapper → Puppeteer → Screenshot
     ↑                                                    ↓
     └────────── Canvas Integration ←─────────────────────┘
```

1. **Bundler** (`lib/bundler.js`): Uses esbuild to bundle React + JSX
2. **Renderer** (`lib/renderer.js`): Uses Puppeteer for headless rendering
3. **Canvas**: Saves HTML for live preview on connected nodes
