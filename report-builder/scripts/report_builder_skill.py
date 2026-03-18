#!/usr/bin/env python3
"""
Report Builder Skill Wrapper
OpenClaw skill interface for automated report generation.
"""

import json
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from report_builder import (
    create_report,
    add_chart,
    add_table,
    add_section,
    export,
    load_data_source,
    Report
)


def main():
    """Handle OpenClaw skill requests."""
    if len(sys.argv) < 2:
        print("Usage: report_builder_skill.py <command> [args]", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        # Create a new report
        data = {}
        template = "default"
        output_format = "pdf"
        
        if len(sys.argv) > 2:
            data_path = sys.argv[2]
            if os.path.exists(data_path):
                data = load_data_source(data_path)
            else:
                data = json.loads(data_path)
        
        if len(sys.argv) > 3:
            template = sys.argv[3]
        if len(sys.argv) > 4:
            output_format = sys.argv[4]
        
        report = create_report(data, template, output_format)
        
        # Save report state
        state = {
            "title": report.title,
            "template": report.template,
            "output_format": report.output_format,
            "sections": report.sections,
            "charts": report.charts,
            "tables": report.tables,
            "metadata": report.metadata
        }
        print(json.dumps(state))
    
    elif command == "add_section":
        # Add section to report (state passed via stdin)
        state = json.load(sys.stdin)
        title = sys.argv[2] if len(sys.argv) > 2 else "Section"
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        
        report = _state_to_report(state)
        add_section(report, title, content)
        print(json.dumps(_report_to_state(report)))
    
    elif command == "add_chart":
        # Add chart to report
        state = json.load(sys.stdin)
        chart_type = sys.argv[2] if len(sys.argv) > 2 else "bar"
        chart_data = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        title = sys.argv[4] if len(sys.argv) > 4 else ""
        
        report = _state_to_report(state)
        add_chart(report, chart_type, chart_data, title)
        print(json.dumps(_report_to_state(report)))
    
    elif command == "add_table":
        # Add table to report
        state = json.load(sys.stdin)
        table_data = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
        headers = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
        
        report = _state_to_report(state)
        add_table(report, table_data, headers)
        print(json.dumps(_report_to_state(report)))
    
    elif command == "export":
        # Export report
        state = json.load(sys.stdin)
        output_path = sys.argv[2] if len(sys.argv) > 2 else "report.pdf"
        fmt = sys.argv[3] if len(sys.argv) > 3 else None
        
        report = _state_to_report(state)
        result = export(report, output_path, fmt)
        print(json.dumps({"output_path": result}))
    
    elif command == "test":
        # Run a quick test
        _run_test()
    
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


def _state_to_report(state: dict) -> Report:
    """Convert state dict back to Report object."""
    report = Report(
        title=state.get("title", "Report"),
        template=state.get("template", "default"),
        output_format=state.get("output_format", "pdf")
    )
    report.sections = state.get("sections", [])
    report.charts = state.get("charts", [])
    report.tables = state.get("tables", [])
    report.metadata = state.get("metadata", {})
    return report


def _report_to_state(report: Report) -> dict:
    """Convert Report object to state dict."""
    return {
        "title": report.title,
        "template": report.template,
        "output_format": report.output_format,
        "sections": report.sections,
        "charts": report.charts,
        "tables": report.tables,
        "metadata": report.metadata
    }


def _run_test():
    """Run a quick test to verify the skill works."""
    print("Running Report Builder test...")
    
    # Create sample report
    data = {
        "title": "Q1 2024 Performance Report",
        "executive_summary": "Q1 2024 showed strong growth across all key metrics...",
        "key_findings": [
            "Revenue increased by 25% compared to Q4 2023",
            "Customer acquisition cost decreased by 15%",
            "User engagement metrics improved significantly"
        ],
        "recommendations": [
            "Continue investing in marketing channels that showed ROI",
            "Expand the product team to accelerate feature development",
            "Explore new market opportunities in APAC region"
        ]
    }
    
    report = create_report(data, template="executive", output_format="pdf")
    
    # Add a chart
    add_chart(report, "bar", {
        "x": ["Jan", "Feb", "Mar"],
        "y": [100, 150, 200],
        "xlabel": "Month",
        "ylabel": "Revenue ($K)"
    }, "Monthly Revenue")
    
    # Add a table
    add_table(report, [
        ["Product A", "$100K", "+20%"],
        ["Product B", "$80K", "+15%"],
        ["Product C", "$50K", "+10%"]
    ], ["Product", "Revenue", "Growth"])
    
    # Export
    output_path = "/tmp/test_report.pdf"
    result = export(report, output_path)
    print(f"Test report created: {result}")
    
    # Also test DOCX
    report_docx = create_report(data, template="executive", output_format="docx")
    add_chart(report_docx, "line", {
        "x": ["Q1", "Q2", "Q3", "Q4"],
        "y": [100, 120, 140, 180],
        "xlabel": "Quarter",
        "ylabel": "Users (K)"
    }, "User Growth")
    add_table(report_docx, [
        ["North America", "45%"],
        ["Europe", "30%"],
        ["Asia", "25%"]
    ], ["Region", "Market Share"])
    
    output_docx = "/tmp/test_report.docx"
    result_docx = export(report_docx, output_docx)
    print(f"Word report created: {result_docx}")
    
    # Test HTML
    report_html = create_report(data, template="executive", output_format="html")
    add_chart(report_html, "pie", {
        "labels": ["Direct", "Social", "Organic", "Referral"],
        "values": [35, 25, 30, 10]
    }, "Traffic Sources")
    
    output_html = "/tmp/test_report.html"
    result_html = export(report_html, output_html)
    print(f"HTML report created: {result_html}")
    
    print("All tests passed!")


if __name__ == "__main__":
    main()
