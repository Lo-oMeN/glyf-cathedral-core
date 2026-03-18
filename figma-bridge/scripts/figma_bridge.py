#!/usr/bin/env python3
"""
Figma Bridge - Complete Figma API Integration
Provides operations for design system management and file operations.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime

# Figma API Configuration
BASE_URL = "https://api.figma.com"
API_VERSION = "v1"

class FigmaClient:
    """Client for interacting with the Figma REST API."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize with optional token (falls back to FIGMA_TOKEN env var)."""
        self.token = token or os.environ.get("FIGMA_TOKEN")
        if not self.token:
            raise ValueError("Figma token required. Set FIGMA_TOKEN environment variable or pass token.")
    
    def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Make an authenticated request to the Figma API."""
        url = f"{BASE_URL}/{API_VERSION}/{endpoint}"
        headers = {
            "X-Figma-Token": self.token,
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise Exception(f"API Error {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Network Error: {e.reason}")
    
    def get_file(self, file_key: str, **options) -> Dict:
        """
        Fetch complete Figma file structure.
        
        Args:
            file_key: The Figma file key from URL
            options: Additional query parameters (version, depth, ids, etc.)
        """
        query = "&".join(f"{k}={v}" for k, v in options.items() if v is not None)
        endpoint = f"files/{file_key}"
        if query:
            endpoint += f"?{query}"
        return self._request(endpoint)
    
    def get_components(self, file_key: str) -> List[Dict]:
        """
        List all components in a Figma file.
        
        Args:
            file_key: The Figma file key
            
        Returns:
            List of component metadata
        """
        data = self.get_file(file_key)
        components = []
        
        if "components" in data:
            for node_id, component in data["components"].items():
                component["id"] = node_id
                components.append(component)
        
        return components
    
    def export_node(self, file_key: str, node_id: str, 
                    format: str = "png", scale: float = 1,
                    output_path: Optional[str] = None) -> str:
        """
        Export a node as an image.
        
        Args:
            file_key: The Figma file key
            node_id: The node ID to export
            format: Export format (png, jpg, svg, pdf)
            scale: Scale factor (0.01 to 4)
            output_path: Where to save the file (optional)
            
        Returns:
            Path to saved file or URL if output_path not provided
        """
        endpoint = f"images/{file_key}?ids={node_id}&format={format}&scale={scale}"
        response = self._request(endpoint)
        
        if "images" not in response or not response["images"]:
            raise Exception(f"No image returned: {response.get('err', 'Unknown error')}")
        
        image_url = response["images"].get(node_id)
        if not image_url:
            raise Exception(f"No image URL for node {node_id}")
        
        if output_path:
            # Download the image
            req = urllib.request.Request(image_url, headers={"X-Figma-Token": self.token})
            with urllib.request.urlopen(req) as img_response:
                img_data = img_response.read()
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_data)
            return output_path
        
        return image_url
    
    def extract_tokens(self, file_key: str) -> Dict[str, Any]:
        """
        Extract design tokens from a Figma file.
        
        Args:
            file_key: The Figma file key
            
        Returns:
            Dictionary containing colors, typography, spacing, effects tokens
        """
        data = self.get_file(file_key)
        tokens = {
            "colors": {},
            "typography": {},
            "spacing": {},
            "effects": {},
            "borders": {},
            "metadata": {
                "file_name": data.get("name", "Unknown"),
                "last_modified": data.get("lastModified", ""),
                "extracted_at": datetime.now().isoformat()
            }
        }
        
        # Extract styles from the file
        if "styles" in data:
            for style_id, style_info in data["styles"].items():
                style_type = style_info.get("styleType", "").lower()
                style_name = style_info.get("name", "").replace(" ", "-").lower()
                
                if style_type == "fill":
                    tokens["colors"][style_name] = {"style_id": style_id, **style_info}
                elif style_type == "text":
                    tokens["typography"][style_name] = {"style_id": style_id, **style_info}
                elif style_type == "effect":
                    tokens["effects"][style_name] = {"style_id": style_id, **style_info}
                elif style_type == "grid":
                    tokens["spacing"][style_name] = {"style_id": style_id, **style_info}
        
        # Extract from document tree
        document = data.get("document", {})
        self._extract_tokens_from_node(document, tokens)
        
        return tokens
    
    def _extract_tokens_from_node(self, node: Dict, tokens: Dict):
        """Recursively extract tokens from document nodes."""
        node_type = node.get("type", "").upper()
        node_name = node.get("name", "").replace(" ", "-").lower()
        
        # Extract fills (colors)
        if "fills" in node:
            for i, fill in enumerate(node["fills"]):
                if fill.get("type") == "SOLID" and "color" in fill:
                    color_name = f"{node_name}-{i}" if node_name else f"color-{i}"
                    color = fill["color"]
                    rgb = {
                        "r": round(color.get("r", 0) * 255),
                        "g": round(color.get("g", 0) * 255),
                        "b": round(color.get("b", 0) * 255),
                        "a": color.get("a", 1)
                    }
                    tokens["colors"][color_name] = {
                        "value": f"rgba({rgb['r']}, {rgb['g']}, {rgb['b']}, {rgb['a']})",
                        "hex": self._rgba_to_hex(rgb),
                        "raw": color
                    }
        
        # Extract typography
        if "style" in node and node_type in ["TEXT", "TEXT_NODE"]:
            text_style = node["style"]
            tokens["typography"][node_name] = {
                "fontFamily": text_style.get("fontFamily"),
                "fontSize": text_style.get("fontSize"),
                "fontWeight": text_style.get("fontWeight"),
                "lineHeight": text_style.get("lineHeightPx"),
                "letterSpacing": text_style.get("letterSpacing"),
                "textAlign": text_style.get("textAlignHorizontal")
            }
        
        # Extract spacing from frame/padding
        if "paddingLeft" in node or "paddingRight" in node or "itemSpacing" in node:
            tokens["spacing"][node_name] = {
                "paddingLeft": node.get("paddingLeft"),
                "paddingRight": node.get("paddingRight"),
                "paddingTop": node.get("paddingTop"),
                "paddingBottom": node.get("paddingBottom"),
                "itemSpacing": node.get("itemSpacing"),
                "layoutMode": node.get("layoutMode")
            }
        
        # Extract effects (shadows)
        if "effects" in node:
            for i, effect in enumerate(node["effects"]):
                if effect.get("type") in ["DROP_SHADOW", "INNER_SHADOW"]:
                    effect_name = f"{node_name}-shadow-{i}" if node_name else f"shadow-{i}"
                    tokens["effects"][effect_name] = {
                        "type": effect.get("type"),
                        "color": effect.get("color"),
                        "offset": effect.get("offset"),
                        "radius": effect.get("radius"),
                        "spread": effect.get("spread")
                    }
        
        # Recurse into children
        for child in node.get("children", []):
            self._extract_tokens_from_node(child, tokens)
    
    def _rgba_to_hex(self, rgba: Dict) -> str:
        """Convert RGBA dict to hex color string."""
        r = int(rgba.get("r", 0))
        g = int(rgba.get("g", 0))
        b = int(rgba.get("b", 0))
        a = rgba.get("a", 1)
        
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        if a < 1:
            a_hex = int(a * 255)
            hex_color += f"{a_hex:02x}"
        return hex_color.upper()
    
    def generate_css(self, tokens: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Generate CSS custom properties from design tokens.
        
        Args:
            tokens: Design tokens dictionary from extract_tokens
            output_path: Optional path to save CSS file
            
        Returns:
            CSS string with CSS custom properties
        """
        css_lines = [
            "/* Design Tokens - Generated from Figma */",
            f"/* Source: {tokens.get('metadata', {}).get('file_name', 'Unknown')} */",
            f"/* Generated: {datetime.now().isoformat()} */",
            "",
            ":root {"
        ]
        
        # Colors
        if tokens.get("colors"):
            css_lines.append("  /* Colors */")
            for name, color_data in tokens["colors"].items():
                value = color_data.get("hex") or color_data.get("value")
                if value:
                    safe_name = name.replace("/", "-").replace(" ", "-").lower()
                    css_lines.append(f"  --color-{safe_name}: {value};")
            css_lines.append("")
        
        # Typography
        if tokens.get("typography"):
            css_lines.append("  /* Typography */")
            for name, type_data in tokens["typography"].items():
                safe_name = name.replace("/", "-").replace(" ", "-").lower()
                if type_data.get("fontSize"):
                    css_lines.append(f"  --font-size-{safe_name}: {type_data['fontSize']}px;")
                if type_data.get("fontFamily"):
                    css_lines.append(f"  --font-family-{safe_name}: {type_data['fontFamily']};")
                if type_data.get("fontWeight"):
                    css_lines.append(f"  --font-weight-{safe_name}: {type_data['fontWeight']};")
                if type_data.get("lineHeight"):
                    css_lines.append(f"  --line-height-{safe_name}: {type_data['lineHeight']}px;")
            css_lines.append("")
        
        # Spacing
        if tokens.get("spacing"):
            css_lines.append("  /* Spacing */")
            for name, space_data in tokens["spacing"].items():
                safe_name = name.replace("/", "-").replace(" ", "-").lower()
                for key in ["paddingLeft", "paddingRight", "paddingTop", "paddingBottom", "itemSpacing"]:
                    if space_data.get(key):
                        css_lines.append(f"  --spacing-{safe_name}-{key.lower()}: {space_data[key]}px;")
            css_lines.append("")
        
        # Effects (Shadows)
        if tokens.get("effects"):
            css_lines.append("  /* Effects */")
            for name, effect_data in tokens["effects"].items():
                if effect_data.get("type") in ["DROP_SHADOW", "INNER_SHADOW"]:
                    safe_name = name.replace("/", "-").replace(" ", "-").lower()
                    color = effect_data.get("color", {})
                    offset = effect_data.get("offset", {})
                    radius = effect_data.get("radius", 0)
                    spread = effect_data.get("spread", 0)
                    
                    r = round(color.get("r", 0) * 255)
                    g = round(color.get("g", 0) * 255)
                    b = round(color.get("b", 0) * 255)
                    a = color.get("a", 1)
                    
                    x = offset.get("x", 0)
                    y = offset.get("y", 0)
                    
                    shadow_value = f"{x}px {y}px {radius}px {spread}px rgba({r}, {g}, {b}, {a})"
                    css_lines.append(f"  --shadow-{safe_name}: {shadow_value};")
        
        css_lines.append("}")
        css = "\n".join(css_lines)
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(css)
        
        return css
    
    def compare_versions(self, file_key: str, version1: str, version2: str) -> Dict:
        """
        Compare two versions of a Figma file.
        
        Args:
            file_key: The Figma file key
            version1: First version ID
            version2: Second version ID
            
        Returns:
            Dictionary with added, removed, and modified components
        """
        v1_data = self.get_file(file_key, version=version1)
        v2_data = self.get_file(file_key, version=version2)
        
        v1_components = v1_data.get("components", {})
        v2_components = v2_data.get("styles", {})
        
        v1_ids = set(v1_components.keys())
        v2_ids = set(v2_components.keys())
        
        result = {
            "metadata": {
                "file_key": file_key,
                "version1": version1,
                "version2": version2,
                "file_name_v1": v1_data.get("name"),
                "file_name_v2": v2_data.get("name"),
                "compared_at": datetime.now().isoformat()
            },
            "added": [],
            "removed": [],
            "modified": []
        }
        
        # Find added components
        for comp_id in v2_ids - v1_ids:
            result["added"].append({
                "id": comp_id,
                **v2_components[comp_id]
            })
        
        # Find removed components
        for comp_id in v1_ids - v2_ids:
            result["removed"].append({
                "id": comp_id,
                **v1_components[comp_id]
            })
        
        # Find potentially modified components (same ID, check lastModified)
        for comp_id in v1_ids & v2_ids:
            v1_info = v1_components[comp_id]
            v2_info = v2_components[comp_id]
            
            # Compare key properties
            if v1_info != v2_info:
                result["modified"].append({
                    "id": comp_id,
                    "before": v1_info,
                    "after": v2_info
                })
        
        return result
    
    def comment_on_node(self, file_key: str, node_id: str, message: str) -> Dict:
        """
        Add a comment to a specific node in a Figma file.
        
        Args:
            file_key: The Figma file key
            node_id: The node ID to comment on
            message: The comment message
            
        Returns:
            API response with comment details
        """
        data = {
            "message": message,
            "client_meta": {
                "node_id": node_id
            }
        }
        return self._request(f"files/{file_key}/comments", method="POST", data=data)
    
    def get_comments(self, file_key: str) -> List[Dict]:
        """Get all comments on a Figma file."""
        response = self._request(f"files/{file_key}/comments")
        return response.get("comments", [])
    
    def get_file_versions(self, file_key: str) -> List[Dict]:
        """Get version history of a Figma file."""
        response = self._request(f"files/{file_key}/versions")
        return response.get("versions", [])


def main():
    """CLI interface for Figma Bridge."""
    parser = argparse.ArgumentParser(description="Figma Bridge - Figma API Integration")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Global arguments
    parser.add_argument("--token", "-t", help="Figma API token (or set FIGMA_TOKEN env var)")
    
    # get_file command
    get_file_parser = subparsers.add_parser("get-file", help="Fetch Figma file structure")
    get_file_parser.add_argument("file_key", help="Figma file key")
    get_file_parser.add_argument("--output", "-o", help="Output JSON file path")
    get_file_parser.add_argument("--depth", type=int, help="Depth limit for node tree")
    
    # get_components command
    get_components_parser = subparsers.add_parser("get-components", help="List all components")
    get_components_parser.add_argument("file_key", help="Figma file key")
    get_components_parser.add_argument("--output", "-o", help="Output JSON file path")
    
    # export_node command
    export_parser = subparsers.add_parser("export-node", help="Export node as image")
    export_parser.add_argument("file_key", help="Figma file key")
    export_parser.add_argument("node_id", help="Node ID to export")
    export_parser.add_argument("--format", default="png", choices=["png", "jpg", "svg", "pdf"])
    export_parser.add_argument("--scale", type=float, default=1, help="Scale factor (0.01-4)")
    export_parser.add_argument("--output", "-o", required=True, help="Output file path")
    
    # extract_tokens command
    tokens_parser = subparsers.add_parser("extract-tokens", help="Extract design tokens")
    tokens_parser.add_argument("file_key", help="Figma file key")
    tokens_parser.add_argument("--output", "-o", default="tokens.json", help="Output JSON file")
    
    # generate_css command
    css_parser = subparsers.add_parser("generate-css", help="Generate CSS from tokens")
    css_parser.add_argument("tokens_file", help="Input tokens JSON file")
    css_parser.add_argument("--output", "-o", default="tokens.css", help="Output CSS file")
    
    # compare_versions command
    compare_parser = subparsers.add_parser("compare-versions", help="Compare file versions")
    compare_parser.add_argument("file_key", help="Figma file key")
    compare_parser.add_argument("version1", help="First version ID")
    compare_parser.add_argument("version2", help="Second version ID")
    compare_parser.add_argument("--output", "-o", help="Output JSON file")
    
    # comment command
    comment_parser = subparsers.add_parser("comment", help="Add comment to node")
    comment_parser.add_argument("file_key", help="Figma file key")
    comment_parser.add_argument("node_id", help="Node ID")
    comment_parser.add_argument("message", help="Comment message")
    
    # get_comments command
    get_comments_parser = subparsers.add_parser("get-comments", help="Get all comments")
    get_comments_parser.add_argument("file_key", help="Figma file key")
    get_comments_parser.add_argument("--output", "-o", help="Output JSON file")
    
    # get_versions command
    versions_parser = subparsers.add_parser("get-versions", help="Get file version history")
    versions_parser.add_argument("file_key", help="Figma file key")
    versions_parser.add_argument("--output", "-o", help="Output JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        # Commands that don't need API access
        if args.command == "generate-css":
            with open(args.tokens_file, "r") as f:
                tokens = json.load(f)
            # Create client without token just for the method (it doesn't need API)
            css = FigmaClient.generate_css(None, tokens, args.output)
            print(f"CSS generated to {args.output}")
            return
        
        # All other commands need API access
        client = FigmaClient(args.token)
        
        if args.command == "get-file":
            opts = {}
            if args.depth:
                opts["depth"] = args.depth
            result = client.get_file(args.file_key, **opts)
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"File saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "get-components":
            result = client.get_components(args.file_key)
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Components saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "export-node":
            result = client.export_node(args.file_key, args.node_id, 
                                       format=args.format, scale=args.scale,
                                       output_path=args.output)
            print(f"Image exported to {result}")
        
        elif args.command == "extract-tokens":
            tokens = client.extract_tokens(args.file_key)
            with open(args.output, "w") as f:
                json.dump(tokens, f, indent=2)
            print(f"Tokens extracted to {args.output}")
        
        elif args.command == "compare-versions":
            result = client.compare_versions(args.file_key, args.version1, args.version2)
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Comparison saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "comment":
            result = client.comment_on_node(args.file_key, args.node_id, args.message)
            print(f"Comment added: {json.dumps(result, indent=2)}")
        
        elif args.command == "get-comments":
            result = client.get_comments(args.file_key)
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Comments saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        
        elif args.command == "get-versions":
            result = client.get_file_versions(args.file_key)
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"Versions saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
