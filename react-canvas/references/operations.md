# React Canvas Operations Reference

## Core Operations

### render_component(jsx_code, props={}, width=800, height=600)

Renders JSX code to PNG or SVG image.

**Parameters:**
- `jsx_code` (string): JSX code to render
- `props` (Object): Props to pass to the component
- `width` (number): Output width in pixels
- `height` (number): Output height in pixels
- `format` (string): 'png' or 'svg'

**Returns:** Path to generated image file

**Example:**
```javascript
render_component(`
  <div style={{ padding: 20, background: '#f0f0f0' }}>
    <h1>Hello {name}</h1>
  </div>
`, { name: 'World' }, 400, 300, 'png')
```

### render_from_file(component_path, props)

Renders a saved component file.

**Parameters:**
- `component_path` (string): Path to .jsx or .tsx file
- `props` (Object): Props to pass to the component

**Returns:** Path to generated image file

**Example:**
```javascript
render_from_file('./components/Button.jsx', { text: 'Click me' })
```

### create_component_template(name, template='functional')

Scaffolds a new React component.

**Parameters:**
- `name` (string): Component name (PascalCase)
- `template` (string): 'functional', 'class', or 'arrow'

**Returns:** Path to created file

**Example:**
```javascript
create_component_template('UserCard', 'functional')
```

### hot_reload(file_path)

Watches a file and auto-reloads on changes.

**Parameters:**
- `file_path` (string): Path to component file

**Returns:** None (runs until interrupted)

**Example:**
```javascript
hot_reload('./components/Chart.jsx')
```

### compare_versions(component_v1, component_v2)

Creates a visual diff between two component versions.

**Parameters:**
- `component_v1` (string): Path or code for version 1
- `component_v2` (string): Path or code for version 2
- `format` (string): 'side-by-side', 'overlay', or 'diff'

**Returns:** Path to comparison image

**Example:**
```javascript
compare_versions('./Button-v1.jsx', './Button-v2.jsx', 'diff')
```

## UI Library Support

### Tailwind CSS

Components using Tailwind classes are automatically styled.

```jsx
<div className="p-4 bg-blue-500 text-white rounded-lg">
  Tailwind styled content
</div>
```

### Chakra UI

Wraps components with ChakraProvider automatically.

```jsx
import { Box, Button } from '@chakra-ui/react';

<Box p={4} shadow="md">
  <Button colorScheme="blue">Click</Button>
</Box>
```

### Material-UI

Wraps components with ThemeProvider automatically.

```jsx
import { Button, Paper } from '@mui/material';

<Paper elevation={3}>
  <Button variant="contained">Click</Button>
</Paper>
```

## File Structure

```
react-canvas/
├── scripts/
│   ├── lib/
│   │   ├── bundler.js      # Esbuild bundling logic
│   │   └── renderer.js     # Puppeteer rendering logic
│   ├── render_component.js # Main render script
│   ├── render_from_file.js # File render script
│   ├── create_template.js  # Template generator
│   ├── hot_reload.js       # File watcher
│   ├── compare_versions.js # Visual diff
│   └── react-canvas.js     # CLI wrapper
├── references/
│   └── operations.md       # This file
└── SKILL.md                # Main skill documentation
```

## Environment Variables

- `REACT_CANVAS_ROOT`: Canvas output directory (default: ~/clawd/canvas)
- `DEBUG`: Enable debug output

## Error Handling

All operations throw descriptive errors for:
- Missing files
- Invalid JSX syntax
- Bundle failures
- Rendering timeouts
