# Content Blocks Schema

When creating documents from scratch, define content as an array of blocks.

## Block Types

### Heading

```json
{
  "type": "heading",
  "level": 1,
  "text": "Document Title",
  "style": {
    "font": "Arial",
    "size": 24,
    "color": "#1F4E78"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Must be "heading" |
| level | int | No | 1-6 (default: 1) |
| text | string | Yes | Heading text |
| style | object | No | Font, size, color |

### Paragraph

```json
{
  "type": "paragraph",
  "text": "This is a paragraph of text.",
  "alignment": "justify",
  "style": {
    "bold": false,
    "italic": true,
    "font": "Calibri",
    "size": 11
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Must be "paragraph" |
| text | string | Yes | Paragraph text |
| alignment | string | No | left, center, right, justify |
| style | object | No | Formatting options |

### Table

```json
{
  "type": "table",
  "rows": [
    ["Header 1", "Header 2", "Header 3"],
    ["Cell 1", "Cell 2", "Cell 3"],
    ["Cell 4", "Cell 5", "Cell 6"]
  ],
  "style": "Table Grid",
  "alignment": "CENTER",
  "header_style": {
    "bold": true,
    "background": "#F2F2F2"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Must be "table" |
| rows | array | Yes | 2D array of cell values |
| style | string | No | Table style name |
| alignment | string | No | LEFT, CENTER, RIGHT |
| header_style | object | No | First row formatting |

### Image

```json
{
  "type": "image",
  "path": "/path/to/image.png",
  "width": 4.0,
  "height": 3.0
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | Yes | Must be "image" |
| path | string | Yes | Image file path |
| width | float | No | Width in inches |
| height | float | No | Height in inches |

### Page Break

```json
{
  "type": "page_break"
}
```

## Full Example

```json
{
  "style": {
    "default_font": "Calibri",
    "default_size": 11,
    "page": {
      "width": 8.5,
      "height": 11,
      "margin_top": 1,
      "margin_bottom": 1,
      "margin_left": 1,
      "margin_right": 1
    }
  },
  "content": [
    {
      "type": "heading",
      "level": 1,
      "text": "Quarterly Report"
    },
    {
      "type": "paragraph",
      "text": "This report summarizes our Q4 performance.",
      "alignment": "left"
    },
    {
      "type": "table",
      "rows": [
        ["Metric", "Q3", "Q4"],
        ["Revenue", "$100K", "$120K"],
        ["Expenses", "$80K", "$85K"]
      ]
    },
    {
      "type": "page_break"
    },
    {
      "type": "heading",
      "level": 2,
      "text": "Detailed Analysis"
    }
  ]
}
```

## Global Style Options

```json
{
  "style": {
    "default_font": "Calibri",
    "default_size": 11,
    "page": {
      "width": 8.5,
      "height": 11,
      "margin_top": 1,
      "margin_bottom": 1,
      "margin_left": 1,
      "margin_right": 1
    }
  }
}
```
