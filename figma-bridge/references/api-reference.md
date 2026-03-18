# Figma REST API Reference

## Authentication

All API requests require authentication via a Personal Access Token:

**Header:** `X-Figma-Token: YOUR_TOKEN`

Get your token from Figma Settings → Personal Access Tokens.

## Base URL

```
https://api.figma.com/v1/
```

## Core Endpoints

### Files

#### GET /files/:key
Fetch complete file JSON structure including document tree, components, and styles.

**Query Parameters:**
- `version` - Specific version ID
- `depth` - Limit tree traversal depth
- `ids` - Comma-separated list of node IDs
- `geometry=paths` - Include vector path data

#### GET /files/:key/nodes
Fetch specific nodes by ID with their subtrees.

**Query Parameters:**
- `ids` (required) - Comma-separated node IDs
- `depth` - Limit depth
- `version` - Specific version

### Images

#### GET /images/:key
Export nodes as images (PNG, JPG, SVG, PDF).

**Query Parameters:**
- `ids` (required) - Node IDs to render
- `format` - png, jpg, svg, pdf
- `scale` - 0.01 to 4
- `svg_outline_text` - Default true
- `contents_only` - Default true

### Components & Styles

#### GET /files/:key/components
Get all components in a file.

#### GET /files/:key/styles
Get all styles in a file.

#### GET /teams/:team_id/components
Get team library components.

### Comments

#### GET /files/:key/comments
List all comments on a file.

#### POST /files/:key/comments
Add a comment to a file.

**Request Body:**
```json
{
  "message": "Comment text",
  "client_meta": {
    "node_id": "123:456",
    "node_offset": {"x": 100, "y": 200}
  }
}
```

### Versions

#### GET /files/:key/versions
Get version history of a file.

### Projects

#### GET /teams/:team_id/projects
List team projects.

#### GET /projects/:project_id/files
List files in a project.

## Node Types

| Type | Description |
|------|-------------|
| `DOCUMENT` | Root of the file |
| `CANVAS` | Page/frame |
| `FRAME` | Container with auto-layout |
| `GROUP` | Group of nodes |
| `RECTANGLE` | Rectangle shape |
| `ELLIPSE` | Ellipse shape |
| `VECTOR` | Custom vector path |
| `TEXT` | Text element |
| `COMPONENT` | Component definition |
| `INSTANCE` | Component instance |
| `STAR` | Star shape |
| `LINE` | Line shape |
| `POLYGON` | Polygon shape |
| `BOOLEAN_OPERATION` | Boolean operation result |

## Common Properties

### Paint (Fill/Stroke)
```json
{
  "type": "SOLID|GRADIENT_LINEAR|GRADIENT_RADIAL|GRADIENT_ANGULAR|GRADIENT_DIAMOND|IMAGE|EMOJI",
  "visible": true,
  "opacity": 1,
  "color": {"r": 0, "g": 0, "b": 0, "a": 1}
}
```

### Text Style
```json
{
  "fontFamily": "Inter",
  "fontPostScriptName": "Inter-Bold",
  "fontSize": 16,
  "fontWeight": 700,
  "lineHeightPx": 24,
  "letterSpacing": 0,
  "textAlignHorizontal": "LEFT",
  "textAlignVertical": "TOP"
}
```

### Effect
```json
{
  "type": "DROP_SHADOW|INNER_SHADOW|LAYER_BLUR|BACKGROUND_BLUR",
  "visible": true,
  "radius": 4,
  "color": {"r": 0, "g": 0, "b": 0, "a": 0.25},
  "offset": {"x": 0, "y": 2},
  "spread": 0
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 403 | Forbidden - Invalid/expired token |
| 404 | Not Found - File/node doesn't exist |
| 429 | Rate Limited |
| 500 | Server Error |

## Rate Limits

- Free plan: 1000 requests/hour
- Professional: 10,000 requests/hour
- Organization: 100,000 requests/hour

## Getting File Keys

From any Figma URL:
```
https://www.figma.com/file/:FILE_KEY/:FILE_NAME
https://www.figma.com/file/:FILE_KEY/:FILE_NAME?node-id=:NODE_ID
```

## Getting Node IDs

Right-click any element in Figma → Copy Link → Extract `node-id` parameter:
```
node-id=123%3A456  (URL encoded = 123:456)
```

Or use the plugin "Export Frame IDs" or access via Dev Mode.
