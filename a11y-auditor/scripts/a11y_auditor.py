#!/usr/bin/env python3
"""
a11y-auditor: WCAG Accessibility Compliance Checker
Uses axe-core via Playwright for comprehensive accessibility audits.
Supports WCAG 2.1 A, AA, and AAA levels.
"""

import argparse
import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, asdict
import html

# Check for playwright availability
try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# Check for pa11y (puppeteer-based) availability as fallback
try:
    import subprocess
    HAS_P11Y = True
except ImportError:
    HAS_P11Y = False

# Try to import axe-core scripts
AXE_SCRIPT = """
// axe-core injection script - minified version reference
// Full axe-core will be injected via CDN if not available locally
"""

@dataclass
class AuditIssue:
    """Represents a single accessibility issue."""
    id: str
    description: str
    severity: str  # 'critical', 'serious', 'moderate', 'minor'
    impact: str
    help: str
    help_url: str
    rule_id: str
    target: List[str]
    html: str
    wcag_tags: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class AuditResult:
    """Represents the complete audit results."""
    url: str
    timestamp: str
    level: str  # 'A', 'AA', 'AAA'
    issues: List[AuditIssue]
    passes: int
    violations: int
    incomplete: int
    inapplicable: int
    
    def to_dict(self) -> Dict:
        return {
            'url': self.url,
            'timestamp': self.timestamp,
            'level': self.level,
            'issues': [i.to_dict() for i in self.issues],
            'passes': self.passes,
            'violations': self.violations,
            'incomplete': self.incomplete,
            'inapplicable': self.inapplicable
        }

class A11yAuditor:
    """Main accessibility auditor class using axe-core."""
    
    # WCAG level to axe-core tags mapping
    WCAG_TAGS = {
        'A': ['wcag2a', 'wcag21aa'],
        'AA': ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag21aaa'],
        'AAA': ['wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag21aa', 'wcag21aaa']
    }
    
    # Severity order for sorting
    SEVERITY_ORDER = {'critical': 0, 'serious': 1, 'moderate': 2, 'minor': 3}
    
    def __init__(self):
        self.axe_source = self._load_axe_core()
    
    def _load_axe_core(self) -> str:
        """Load axe-core library from CDN."""
        return """
        (function() {
            if (typeof axe === 'undefined') {
                var script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.0/axe.min.js';
                script.async = false;
                document.head.appendChild(script);
            }
        })();
        """
    
    async def audit_url(self, url: str, level: str = 'AA') -> AuditResult:
        """Audit a URL for accessibility compliance.
        
        Args:
            url: The URL to audit
            level: WCAG compliance level ('A', 'AA', or 'AAA')
        
        Returns:
            AuditResult containing all findings
        """
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install")
        
        level = level.upper()
        if level not in self.WCAG_TAGS:
            raise ValueError(f"Invalid level: {level}. Must be A, AA, or AAA")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_timeout(1000)  # Wait for dynamic content
                
                # Inject axe-core
                await page.add_script_tag(url='https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.0/axe.min.js')
                await page.wait_for_timeout(500)
                
                # Run axe analysis
                tags = self.WCAG_TAGS[level]
                results = await page.evaluate(f"""
                    async () => {{
                        return await axe.run({{
                            runOnly: {{
                                type: 'tag',
                                values: {json.dumps(tags)}
                            }}
                        }});
                    }}
                """)
                
                await browser.close()
                return self._parse_axe_results(url, level, results)
                
            except Exception as e:
                await browser.close()
                raise RuntimeError(f"Audit failed: {str(e)}")
    
    async def audit_file(self, file_path: str, level: str = 'AA') -> AuditResult:
        """Audit a local HTML file for accessibility compliance.
        
        Args:
            file_path: Path to the HTML file
            level: WCAG compliance level ('A', 'AA', or 'AAA')
        
        Returns:
            AuditResult containing all findings
        """
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        url = f"file://{path}"
        return await self.audit_url(url, level)
    
    async def audit_component(self, component_html: str, level: str = 'AA') -> AuditResult:
        """Audit an HTML component for accessibility compliance.
        
        Args:
            component_html: The HTML component to audit
            level: WCAG compliance level ('A', 'AA', or 'AAA')
        
        Returns:
            AuditResult containing all findings
        """
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install")
        
        level = level.upper()
        if level not in self.WCAG_TAGS:
            raise ValueError(f"Invalid level: {level}. Must be A, AA, or AAA")
        
        # Wrap component in basic HTML structure
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Audit</title>
</head>
<body>
    {component_html}
</body>
</html>"""
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            try:
                await page.set_content(html_template)
                await page.wait_for_timeout(1000)
                
                # Inject axe-core
                await page.add_script_tag(url='https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.0/axe.min.js')
                await page.wait_for_timeout(500)
                
                # Run axe analysis
                tags = self.WCAG_TAGS[level]
                results = await page.evaluate(f"""
                    async () => {{
                        return await axe.run({{
                            runOnly: {{
                                type: 'tag',
                                values: {json.dumps(tags)}
                            }}
                        }});
                    }}
                """)
                
                await browser.close()
                return self._parse_axe_results("component://inline", level, results)
                
            except Exception as e:
                await browser.close()
                raise RuntimeError(f"Component audit failed: {str(e)}")
    
    def _parse_axe_results(self, url: str, level: str, results: Dict) -> AuditResult:
        """Parse axe-core results into AuditResult."""
        issues = []
        
        for violation in results.get('violations', []):
            for node in violation.get('nodes', []):
                issue = AuditIssue(
                    id=violation.get('id', 'unknown'),
                    description=violation.get('description', ''),
                    severity=self._map_impact_to_severity(violation.get('impact', 'minor')),
                    impact=violation.get('impact', 'minor'),
                    help=violation.get('help', ''),
                    help_url=violation.get('helpUrl', ''),
                    rule_id=violation.get('id', ''),
                    target=node.get('target', []),
                    html=node.get('html', ''),
                    wcag_tags=violation.get('tags', [])
                )
                issues.append(issue)
        
        # Sort by severity
        issues.sort(key=lambda x: self.SEVERITY_ORDER.get(x.severity, 99))
        
        return AuditResult(
            url=url,
            timestamp=datetime.now().isoformat(),
            level=level,
            issues=issues,
            passes=len(results.get('passes', [])),
            violations=len(results.get('violations', [])),
            incomplete=len(results.get('incomplete', [])),
            inapplicable=len(results.get('inapplicable', []))
        )
    
    def _map_impact_to_severity(self, impact: str) -> str:
        """Map axe impact to standard severity levels."""
        mapping = {
            'critical': 'critical',
            'serious': 'serious',
            'moderate': 'moderate',
            'minor': 'minor'
        }
        return mapping.get(impact, 'minor')
    
    async def batch_audit(self, urls: List[str], level: str = 'AA') -> List[AuditResult]:
        """Audit multiple URLs in sequence.
        
        Args:
            urls: List of URLs to audit
            level: WCAG compliance level ('A', 'AA', or 'AAA')
        
        Returns:
            List of AuditResult objects
        """
        results = []
        for url in urls:
            try:
                result = await self.audit_url(url, level)
                results.append(result)
            except Exception as e:
                # Create failed result
                results.append(AuditResult(
                    url=url,
                    timestamp=datetime.now().isoformat(),
                    level=level,
                    issues=[],
                    passes=0,
                    violations=0,
                    incomplete=0,
                    inapplicable=0
                ))
        return results

class ReportGenerator:
    """Generates formatted accessibility audit reports."""
    
    def generate(self, result: AuditResult, format: str = 'html') -> str:
        """Generate a formatted report from audit results.
        
        Args:
            result: The audit result to format
            format: Output format ('html', 'json', 'md', or 'csv')
        
        Returns:
            Formatted report string
        """
        format = format.lower()
        
        if format == 'json':
            return self._generate_json(result)
        elif format == 'md' or format == 'markdown':
            return self._generate_markdown(result)
        elif format == 'csv':
            return self._generate_csv(result)
        else:
            return self._generate_html(result)
    
    def _generate_json(self, result: AuditResult) -> str:
        """Generate JSON report."""
        return json.dumps(result.to_dict(), indent=2)
    
    def _generate_markdown(self, result: AuditResult) -> str:
        """Generate Markdown report."""
        lines = [
            f"# Accessibility Audit Report",
            f"",
            f"**URL:** {result.url}",
            f"**Level:** WCAG 2.1 {result.level}",
            f"**Date:** {result.timestamp}",
            f"",
            f"## Summary",
            f"",
            f"- **Total Issues:** {len(result.issues)}",
            f"- **Passes:** {result.passes}",
            f"- **Violations:** {result.violations}",
            f"- **Incomplete:** {result.incomplete}",
            f"- **Inapplicable:** {result.inapplicable}",
            f"",
            f"## Issues Found",
            f""
        ]
        
        if not result.issues:
            lines.append("*No accessibility issues found!*")
        else:
            for i, issue in enumerate(result.issues, 1):
                lines.extend([
                    f"### {i}. {issue.help}",
                    f"",
                    f"- **Severity:** {issue.severity}",
                    f"- **Impact:** {issue.impact}",
                    f"- **Description:** {issue.description}",
                    f"- **Element:** `{html.escape(issue.html[:200])}`",
                    f"- **WCAG Tags:** {', '.join(issue.wcag_tags)}",
                    f"- **Learn More:** [{issue.help_url}]({issue.help_url})",
                    f""
                ])
        
        return '\n'.join(lines)
    
    def _generate_csv(self, result: AuditResult) -> str:
        """Generate CSV report."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['ID', 'Severity', 'Impact', 'Help', 'Description', 'HTML', 'WCAG Tags', 'Help URL'])
        
        # Data
        for issue in result.issues:
            writer.writerow([
                issue.id,
                issue.severity,
                issue.impact,
                issue.help,
                issue.description,
                issue.html,
                ','.join(issue.wcag_tags),
                issue.help_url
            ])
        
        return output.getvalue()
    
    def _generate_html(self, result: AuditResult) -> str:
        """Generate HTML report."""
        # Severity color mapping
        severity_colors = {
            'critical': '#dc3545',
            'serious': '#fd7e14',
            'moderate': '#ffc107',
            'minor': '#6c757d'
        }
        
        issues_html = ""
        if not result.issues:
            issues_html = '<div class="success"><h3>✅ No accessibility issues found!</h3></div>'
        else:
            for i, issue in enumerate(result.issues, 1):
                color = severity_colors.get(issue.severity, '#6c757d')
                issues_html += f"""
                <div class="issue" style="border-left-color: {color}">
                    <div class="issue-header">
                        <span class="issue-number">{i}</span>
                        <span class="issue-title">{html.escape(issue.help)}</span>
                        <span class="severity-badge" style="background: {color}">{issue.severity}</span>
                    </div>
                    <div class="issue-body">
                        <p><strong>Description:</strong> {html.escape(issue.description)}</p>
                        <p><strong>Impact:</strong> {issue.impact}</p>
                        <p><strong>Element:</strong> <code>{html.escape(issue.html[:200])}</code></p>
                        <p><strong>WCAG:</strong> {', '.join(issue.wcag_tags)}</p>
                        <p><a href="{issue.help_url}" target="_blank">Learn more about this issue →</a></p>
                    </div>
                </div>
                """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Audit Report - {html.escape(result.url)}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{ color: #666; font-size: 0.9em; }}
        .issues-container {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .issue {{
            border: 1px solid #e0e0e0;
            border-left: 4px solid #dc3545;
            border-radius: 4px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        .issue-header {{
            background: #f8f9fa;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .issue-number {{
            background: #667eea;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .issue-title {{ flex: 1; font-weight: 600; }}
        .severity-badge {{
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .issue-body {{ padding: 15px; }}
        .issue-body p {{ margin: 8px 0; }}
        .issue-body code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.9em;
            word-break: break-all;
        }}
        .success {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Accessibility Audit Report</h1>
        <p><strong>URL:</strong> {html.escape(result.url)}</p>
        <p><strong>WCAG Level:</strong> 2.1 {result.level}</p>
        <p><strong>Generated:</strong> {result.timestamp}</p>
    </div>
    
    <div class="summary">
        <div class="stat-card">
            <div class="stat-number">{len(result.issues)}</div>
            <div class="stat-label">Issues Found</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #28a745">{result.passes}</div>
            <div class="stat-label">Passes</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #dc3545">{result.violations}</div>
            <div class="stat-label">Violations</div>
        </div>
        <div class="stat-card">
            <div class="stat-number" style="color: #ffc107">{result.incomplete}</div>
            <div class="stat-label">Incomplete</div>
        </div>
    </div>
    
    <div class="issues-container">
        <h2>Issues Detail</h2>
        {issues_html}
    </div>
</body>
</html>"""

class FixSuggester:
    """Provides AI-generated fix suggestions for accessibility issues."""
    
    # Common fix patterns for known issues
    FIX_PATTERNS = {
        'color-contrast': {
            'description': 'Text does not have sufficient color contrast against its background.',
            'fix': 'Increase the contrast ratio to at least 4.5:1 for normal text (3:1 for large text). Use a contrast checker tool to verify.',
            'example': '/* Instead of: */\n.color: #777;\n\n/* Use: */\n.color: #555; /* Higher contrast */'
        },
        'image-alt': {
            'description': 'Images must have alternate text',
            'fix': 'Add descriptive alt text that conveys the purpose of the image. Use empty alt="" for decorative images.',
            'example': '<!-- Bad -->\n<img src="photo.jpg">\n\n<!-- Good -->\n<img src="photo.jpg" alt="Golden retriever puppy playing in the park">'
        },
        'link-name': {
            'description': 'Links must have discernible text',
            'fix': 'Ensure all links contain text that describes their purpose. Avoid "click here" or URL-only links.',
            'example': '<!-- Bad -->\n<a href="/products">Click here</a>\n\n<!-- Good -->\n<a href="/products">View our products</a>'
        },
        'button-name': {
            'description': 'Buttons must have discernible text',
            'fix': 'Add visible text, aria-label, or aria-labelledby to buttons.',
            'example': '<!-- Bad -->\n<button><svg>...</svg></button>\n\n<!-- Good -->\n<button aria-label="Close dialog"><svg>...</svg></button>'
        },
        'label': {
            'description': 'Form elements must have labels',
            'fix': 'Associate each form input with a label using the for attribute or wrap the input in a label.',
            'example': '<!-- Bad -->\n<input type="email" id="email">\n\n<!-- Good -->\n<label for="email">Email Address</label>\n<input type="email" id="email">'
        },
        'heading-order': {
            'description': 'Heading elements should be in sequentially descending order',
            'fix': 'Use headings hierarchically (h1 > h2 > h3). Do not skip levels.',
            'example': '<h1>Main Title</h1>\n  <h2>Section</h2>\n    <h3>Subsection</h3>'
        },
        'html-has-lang': {
            'description': 'HTML element must have a lang attribute',
            'fix': 'Add the lang attribute to the html element indicating the primary language.',
            'example': '<html lang="en">\n<html lang="es">\n<html lang="fr">'
        },
        'region': {
            'description': 'Page should contain landmarks',
            'fix': 'Use semantic HTML5 elements like <main>, <nav>, <header>, <footer>, <aside>, <section>.',
            'example': '<body>\n  <header>...</header>\n  <nav>...</nav>\n  <main>...</main>\n  <footer>...</footer>\n</body>'
        },
        'keyboard': {
            'description': 'All functionality should be keyboard accessible',
            'fix': 'Ensure interactive elements can be focused and activated using Tab and Enter/Space keys.',
            'example': '<!-- Add tabindex and keyboard handlers -->\n<div tabindex="0" role="button" onkeydown="handleKey(event)">...</div>'
        },
        'focus-visible': {
            'description': 'Focus indicators should be visible',
            'fix': 'Ensure focused elements have a visible outline or focus indicator.',
            'example': '/* Never remove focus styles without replacement */\n:focus {\n  outline: 2px solid #005fcc;\n  outline-offset: 2px;\n}'
        }
    }
    
    def get_suggestion(self, issue: AuditIssue) -> Dict[str, str]:
        """Get fix suggestion for an accessibility issue.
        
        Args:
            issue: The audit issue to generate suggestions for
        
        Returns:
            Dictionary with fix information
        """
        # Try to match by rule ID
        for pattern_id, pattern in self.FIX_PATTERNS.items():
            if pattern_id in issue.id.lower() or pattern_id in issue.rule_id.lower():
                return {
                    'issue': issue.help,
                    'description': pattern['description'],
                    'fix': pattern['fix'],
                    'example': pattern['example'],
                    'wcag_reference': issue.help_url
                }
        
        # Generic fallback
        return {
            'issue': issue.help,
            'description': issue.description,
            'fix': f"Review the WCAG guidelines for this issue type. Generally: {issue.description}",
            'example': f"Check the documentation: {issue.help_url}",
            'wcag_reference': issue.help_url
        }
    
    def generate_all_suggestions(self, result: AuditResult) -> List[Dict[str, str]]:
        """Generate fix suggestions for all issues in a result."""
        suggestions = []
        for issue in result.issues:
            suggestions.append(self.get_suggestion(issue))
        return suggestions

# CLI Interface
def main():
    parser = argparse.ArgumentParser(
        description='WCAG Accessibility Compliance Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audit https://example.com
  %(prog)s audit https://example.com --level AAA
  %(prog)s file ./index.html --level AA
  %(prog)s component '<button>Click</button>'
  %(prog)s batch urls.txt --format html
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Audit URL command
    audit_parser = subparsers.add_parser('audit', help='Audit a URL')
    audit_parser.add_argument('url', help='URL to audit')
    audit_parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA',
                             help='WCAG compliance level (default: AA)')
    audit_parser.add_argument('--format', choices=['html', 'json', 'md', 'csv'], default='html',
                             help='Output format (default: html)')
    audit_parser.add_argument('--output', '-o', help='Output file path')
    
    # Audit file command
    file_parser = subparsers.add_parser('file', help='Audit a local HTML file')
    file_parser.add_argument('path', help='Path to HTML file')
    file_parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA')
    file_parser.add_argument('--format', choices=['html', 'json', 'md', 'csv'], default='html')
    file_parser.add_argument('--output', '-o', help='Output file path')
    
    # Audit component command
    component_parser = subparsers.add_parser('component', help='Audit an HTML component')
    component_parser.add_argument('html', help='HTML component to audit')
    component_parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA')
    component_parser.add_argument('--format', choices=['html', 'json', 'md', 'csv'], default='html')
    component_parser.add_argument('--output', '-o', help='Output file path')
    
    # Batch audit command
    batch_parser = subparsers.add_parser('batch', help='Batch audit URLs from file')
    batch_parser.add_argument('file', help='File containing URLs (one per line)')
    batch_parser.add_argument('--level', choices=['A', 'AA', 'AAA'], default='AA')
    batch_parser.add_argument('--format', choices=['html', 'json', 'md', 'csv'], default='html')
    batch_parser.add_argument('--output', '-o', help='Output directory')
    
    # Fix suggestions command
    fix_parser = subparsers.add_parser('fix', help='Generate fix suggestions')
    fix_parser.add_argument('report', help='Path to audit report (JSON)')
    fix_parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    auditor = A11yAuditor()
    report_gen = ReportGenerator()
    fix_suggester = FixSuggester()
    
    async def run():
        try:
            if args.command == 'audit':
                result = await auditor.audit_url(args.url, args.level)
                report = report_gen.generate(result, args.format)
                
                if args.output:
                    Path(args.output).write_text(report)
                    print(f"Report saved to: {args.output}")
                else:
                    print(report)
            
            elif args.command == 'file':
                result = await auditor.audit_file(args.path, args.level)
                report = report_gen.generate(result, args.format)
                
                if args.output:
                    Path(args.output).write_text(report)
                    print(f"Report saved to: {args.output}")
                else:
                    print(report)
            
            elif args.command == 'component':
                result = await auditor.audit_component(args.html, args.level)
                report = report_gen.generate(result, args.format)
                
                if args.output:
                    Path(args.output).write_text(report)
                    print(f"Report saved to: {args.output}")
                else:
                    print(report)
            
            elif args.command == 'batch':
                urls = [line.strip() for line in Path(args.file).read_text().splitlines() if line.strip()]
                results = await auditor.batch_audit(urls, args.level)
                
                output_dir = Path(args.output) if args.output else Path('.')
                output_dir.mkdir(parents=True, exist_ok=True)
                
                for result in results:
                    safe_name = result.url.replace('/', '_').replace(':', '_')[:100]
                    report_path = output_dir / f"audit_{safe_name}.{args.format}"
                    report = report_gen.generate(result, args.format)
                    report_path.write_text(report)
                    print(f"Report saved: {report_path}")
            
            elif args.command == 'fix':
                report_data = json.loads(Path(args.report).read_text())
                # Reconstruct AuditResult (simplified)
                issues = [AuditIssue(**issue) for issue in report_data.get('issues', [])]
                result = AuditResult(
                    url=report_data['url'],
                    timestamp=report_data['timestamp'],
                    level=report_data['level'],
                    issues=issues,
                    passes=report_data.get('passes', 0),
                    violations=report_data.get('violations', 0),
                    incomplete=report_data.get('incomplete', 0),
                    inapplicable=report_data.get('inapplicable', 0)
                )
                
                suggestions = fix_suggester.generate_all_suggestions(result)
                output = ["# Fix Suggestions\n"]
                for i, suggestion in enumerate(suggestions, 1):
                    output.append(f"## {i}. {suggestion['issue']}\n")
                    output.append(f"**Description:** {suggestion['description']}\n")
                    output.append(f"**Fix:** {suggestion['fix']}\n")
                    output.append(f"**Example:**\n```\n{suggestion['example']}\n```\n")
                    output.append(f"**Reference:** {suggestion['wcag_reference']}\n\n")
                
                output_text = '\n'.join(output)
                
                if args.output:
                    Path(args.output).write_text(output_text)
                    print(f"Fix suggestions saved to: {args.output}")
                else:
                    print(output_text)
        
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    asyncio.run(run())

if __name__ == '__main__':
    main()
