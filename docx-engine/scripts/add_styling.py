#!/usr/bin/env python3
"""
Add styling to existing DOCX document.
Usage: python3 add_styling.py input.docx styles.json output.docx
"""

import json
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.style import WD_STYLE_TYPE


def add_styling(doc_path, styles, output_path):
    """Apply styles to an existing DOCX document."""
    doc = Document(doc_path)
    
    # Apply document-level font settings
    if 'default_font' in styles or 'default_size' in styles:
        style = doc.styles['Normal']
        font = style.font
        if 'default_font' in styles:
            font.name = styles['default_font']
        if 'default_size' in styles:
            font.size = Pt(styles['default_size'])
    
    # Apply heading styles
    heading_font = styles.get('heading_font')
    heading_color = styles.get('heading_color')
    
    for i in range(1, 10):  # Heading 1-9
        style_name = f'Heading {i}'
        if style_name in doc.styles:
            heading_style = doc.styles[style_name]
            font = heading_style.font
            
            if heading_font:
                font.name = heading_font
            if heading_color:
                color = heading_color
                if color.startswith('#'):
                    color = color[1:]
                font.color.rgb = RGBColor(
                    int(color[0:2], 16),
                    int(color[2:4], 16),
                    int(color[4:6], 16)
                )
            if f'heading_{i}_size' in styles:
                font.size = Pt(styles[f'heading_{i}_size'])
    
    # Apply paragraph styles to existing paragraphs
    paragraph_styles = styles.get('paragraphs', {})
    if paragraph_styles:
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if paragraph_styles.get('font'):
                    run.font.name = paragraph_styles['font']
                if paragraph_styles.get('size'):
                    run.font.size = Pt(paragraph_styles['size'])
                if paragraph_styles.get('color'):
                    color = paragraph_styles['color']
                    if color.startswith('#'):
                        color = color[1:]
                    run.font.color.rgb = RGBColor(
                        int(color[0:2], 16),
                        int(color[2:4], 16),
                        int(color[4:6], 16)
                    )
    
    # Apply page settings
    if 'page' in styles:
        page = styles['page']
        section = doc.sections[0]
        
        if 'width' in page:
            section.page_width = Inches(page['width'])
        if 'height' in page:
            section.page_height = Inches(page['height'])
        if 'margin_top' in page:
            section.top_margin = Inches(page['margin_top'])
        if 'margin_bottom' in page:
            section.bottom_margin = Inches(page['margin_bottom'])
        if 'margin_left' in page:
            section.left_margin = Inches(page['margin_left'])
        if 'margin_right' in page:
            section.right_margin = Inches(page['margin_right'])
    
    # Save styled document
    doc.save(output_path)
    print(f"Styled document saved: {output_path}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Add styling to DOCX document')
    parser.add_argument('input', help='Input DOCX file')
    parser.add_argument('styles', help='JSON file with style configuration')
    parser.add_argument('output', help='Output DOCX file')
    
    args = parser.parse_args()
    
    # Load styles
    with open(args.styles, 'r', encoding='utf-8') as f:
        styles = json.load(f)
    
    add_styling(args.input, styles, args.output)
