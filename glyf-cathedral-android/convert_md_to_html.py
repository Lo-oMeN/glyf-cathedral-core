#!/usr/bin/env python3
"""Convert Markdown to HTML for PDF printing"""
import re

# Read markdown file
with open('COMPLETE_SOURCE.md', 'r') as f:
    md_content = f.read()

# Convert markdown to basic HTML
html = md_content

# Headers
html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

# Code blocks
html = re.sub(r'```(\w+)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
html = re.sub(r'```\n(.*?)```', r'<pre>\1</pre>', html, flags=re.DOTALL)

# Inline code
html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

# Bold
html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

# Italic
html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

# Tables - simple conversion
lines = html.split('\n')
new_lines = []
in_table = False
for line in lines:
    if '|' in line and not in_table:
        in_table = True
        new_lines.append('<table>')
    elif '|' not in line and in_table:
        in_table = False
        new_lines.append('</table>')
    
    if in_table and '---' not in line:
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if cells:
            new_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
    else:
        new_lines.append(line)

html = '\n'.join(new_lines)

# Paragraphs
html = re.sub(r'\n\n([^\u003c])', r'</p><p>\1', html)

# Read header
with open('pdf_header.html', 'r') as f:
    header = f.read()

# Combine
full_html = header + html + '\n</body>\n</html>'

# Write output
with open('COMPLETE_SOURCE.html', 'w') as f:
    f.write(full_html)

print("HTML file created: COMPLETE_SOURCE.html")
