#!/usr/bin/env python3
"""
Report Builder Demo - Quick examples for all templates and features.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from report_builder import create_report, add_chart, add_table, add_section, export


def demo_executive_report():
    """Demo executive summary template."""
    print("Creating Executive Report...")
    
    data = {
        "title": "Q1 2024 Executive Summary",
        "executive_summary": "Q1 2024 demonstrated exceptional performance across all business units. Revenue growth exceeded targets by 15%, driven by successful product launches and market expansion.",
        "key_findings": [
            "Total revenue reached $5.2M, representing 25% YoY growth",
            "Gross margin improved from 65% to 72%",
            "Customer retention increased to 94%",
            "Employee satisfaction reached 4.6/5.0"
        ],
        "recommendations": [
            "Accelerate hiring in sales department",
            "Expand customer success team",
            "Explore strategic partnerships in APAC"
        ]
    }
    
    report = create_report(data, template="executive", output_format="pdf")
    
    # Add revenue chart
    add_chart(report, "bar", {
        "x": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024"],
        "y": [4.16, 4.50, 4.80, 4.95, 5.20],
        "xlabel": "Quarter",
        "ylabel": "Revenue ($M)"
    }, "Quarterly Revenue Growth")
    
    # Add metrics table
    add_table(report, [
        ["Revenue", "$5.2M", "+25%"],
        ["Gross Margin", "72%", "+7pp"],
        ["Customer Retention", "94%", "+5pp"],
        ["Employee Satisfaction", "4.6/5.0", "+0.3"]
    ], ["Metric", "Value", "Change"])
    
    output = "/tmp/demo_executive_report.pdf"
    export(report, output)
    print(f"  Created: {output}")
    return output


def demo_technical_report():
    """Demo technical report template."""
    print("Creating Technical Report...")
    
    data = {
        "title": "System Performance Analysis",
        "overview": "Comprehensive analysis of system performance after Q1 architecture improvements including microservices migration and caching layer implementation.",
        "methodology": "Performance testing using JMeter with 10,000 concurrent users. Metrics collected over 30-day period with 99.9th percentile analysis.",
        "results": "API response times improved by 40%. Database query optimization reduced average query time from 120ms to 45ms. System availability reached 99.98%.",
        "conclusion": "Architecture improvements have positioned the platform for 3x scale growth. Remaining monolith services will be migrated in Q2."
    }
    
    report = create_report(data, template="technical", output_format="pdf")
    
    # Add latency chart
    add_chart(report, "line", {
        "x": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "y": [85, 75, 65, 55, 48, 45],
        "xlabel": "Month",
        "ylabel": "Latency (ms)"
    }, "API Latency Trend")
    
    # Add throughput chart
    add_chart(report, "bar", {
        "x": ["API Gateway", "Auth Service", "User Service", "Payment Service"],
        "y": [4500, 3200, 2800, 1200],
        "xlabel": "Service",
        "ylabel": "Requests/min"
    }, "Service Throughput")
    
    output = "/tmp/demo_technical_report.pdf"
    export(report, output)
    print(f"  Created: {output}")
    return output


def demo_financial_report():
    """Demo financial report template."""
    print("Creating Financial Report...")
    
    data = {
        "title": "Financial Report - Q1 2024",
        "period": "January 1, 2024 - March 31, 2024",
        "highlights": [
            "Record quarterly revenue of $5.2M (+25% YoY)",
            "Net profit margin increased to 18%",
            "Operating expenses reduced by 12%",
            "Cash reserves at $8.5M"
        ],
        "revenue": {
            "total": "$5.2M",
            "growth": "+25%",
            "breakdown": ["Subscriptions: $3.9M", "Services: $780K", "Licensing: $520K"]
        }
    }
    
    report = create_report(data, template="financial", output_format="pdf")
    
    # Add revenue breakdown pie chart
    add_chart(report, "pie", {
        "labels": ["Subscriptions", "Services", "Licensing"],
        "values": [75, 15, 10]
    }, "Revenue Breakdown")
    
    # Add P&L table
    add_table(report, [
        ["Revenue", "$5,200,000", "+25%"],
        ["Cost of Goods Sold", "$1,456,000", "+12%"],
        ["Gross Profit", "$3,744,000", "+30%"],
        ["Operating Expenses", "$2,808,000", "-5%"],
        ["Operating Income", "$936,000", "+85%"],
        ["Net Income", "$728,000", "+90%"]
    ], ["Item", "Amount", "YoY Change"])
    
    output = "/tmp/demo_financial_report.pdf"
    export(report, output)
    print(f"  Created: {output}")
    return output


def demo_word_output():
    """Demo Word document output."""
    print("Creating Word Document...")
    
    report = create_report({"title": "Project Status Report"}, output_format="docx")
    
    add_section(report, "Project Overview", 
        "The project is currently on track with 85% completion. Key milestones achieved include backend API development and database schema design.")
    
    add_section(report, "Current Status",
        "• Backend API: 100% complete\n• Frontend UI: 70% complete\n• Testing: 50% complete\n• Documentation: 30% complete")
    
    add_chart(report, "bar", {
        "x": ["Backend", "Frontend", "Testing", "Docs"],
        "y": [100, 70, 50, 30],
        "xlabel": "Component",
        "ylabel": "Completion %"
    }, "Completion by Component")
    
    output = "/tmp/demo_project_report.docx"
    export(report, output)
    print(f"  Created: {output}")
    return output


def demo_html_output():
    """Demo HTML output."""
    print("Creating HTML Report...")
    
    report = create_report({"title": "Analytics Dashboard Report"}, output_format="html")
    
    add_section(report, "Traffic Overview",
        "Website traffic increased by 45% compared to last month. Primary traffic sources include organic search (40%), direct (30%), and social media (20%).")
    
    add_chart(report, "pie", {
        "labels": ["Organic", "Direct", "Social", "Referral", "Email"],
        "values": [40, 30, 20, 7, 3]
    }, "Traffic Sources")
    
    add_table(report, [
        ["/home", "45%", "2:30"],
        ["/products", "25%", "3:45"],
        ["/pricing", "15%", "1:20"],
        ["/blog", "10%", "4:15"],
        ["/contact", "5%", "1:00"]
    ], ["Page", "Traffic %", "Avg Time"])
    
    output = "/tmp/demo_analytics_report.html"
    export(report, output)
    print(f"  Created: {output}")
    return output


def demo_csv_data():
    """Demo loading data from CSV."""
    print("Creating Report from CSV...")
    
    from report_builder import load_data_source
    
    # Load CSV data
    csv_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sales_data.csv")
    if os.path.exists(csv_path):
        data = load_data_source(csv_path)
        
        report = create_report({"title": "Sales Performance Report"})
        
        # Convert to table
        table_data = []
        for row in data:
            table_data.append([
                row.get("Product", ""),
                row.get("Category", ""),
                f"${int(row.get('Q1 Sales', 0)):,}",
                f"${int(row.get('Q2 Sales', 0)):,}",
                f"${int(row.get('Q3 Sales', 0)):,}",
                f"${int(row.get('Q4 Sales', 0)):,}"
            ])
        
        add_table(report, table_data, 
            ["Product", "Category", "Q1", "Q2", "Q3", "Q4"])
        
        # Calculate totals for chart
        products = [row.get("Product", "") for row in data]
        totals = [
            sum(int(row.get(col, 0)) for col in ["Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales"])
            for row in data
        ]
        
        add_chart(report, "bar", {
            "x": products,
            "y": [t/1000 for t in totals],
            "xlabel": "Product",
            "ylabel": "Total Sales ($K)"
        }, "Annual Sales by Product")
        
        output = "/tmp/demo_csv_report.pdf"
        export(report, output)
        print(f"  Created: {output}")
        return output
    else:
        print(f"  CSV not found: {csv_path}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("Report Builder Demo")
    print("=" * 60)
    print()
    
    # Run all demos
    demo_executive_report()
    print()
    demo_technical_report()
    print()
    demo_financial_report()
    print()
    demo_word_output()
    print()
    demo_html_output()
    print()
    demo_csv_data()
    
    print()
    print("=" * 60)
    print("All demos completed!")
    print("=" * 60)
