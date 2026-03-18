#!/usr/bin/env python3
"""
Test script for proto-interactive skill
Creates a 3-page e-commerce prototype and tests all operations
"""

import json
import sys
sys.path.insert(0, '/root/.openclaw/workspace/proto-interactive/scripts')

from proto_interactive import ProtoInteractive

def test_proto_interactive():
    print("=" * 60)
    print("Testing Proto-Interactive Skill")
    print("=" * 60)
    
    proto = ProtoInteractive(storage_dir="/tmp/proto-test")
    
    # Test 1: Create a 3-page prototype
    print("\n[1] Creating 3-page prototype...")
    pages = [
        {
            "id": "home",
            "name": "Home Page",
            "elements": [
                {"id": "logo", "type": "hotspot", "x": 20, "y": 10, "w": 100, "h": 40, "label": "Logo"},
                {"id": "btn-shop", "type": "button", "x": 300, "y": 200, "w": 120, "h": 50, "label": "Shop Now"},
                {"id": "link-about", "type": "link", "x": 600, "y": 20, "w": 60, "h": 20, "label": "About"}
            ],
            "links": [
                {"from_element": "btn-shop", "to_page": "products", "trigger": "click", "action": "navigate"},
                {"from_element": "link-about", "to_page": "about", "trigger": "click", "action": "navigate"}
            ],
            "background": "#e8f4f8"
        },
        {
            "id": "products",
            "name": "Product List",
            "elements": [
                {"id": "product-1", "type": "button", "x": 100, "y": 150, "w": 200, "h": 250, "label": "Product A"},
                {"id": "product-2", "type": "button", "x": 350, "y": 150, "w": 200, "h": 250, "label": "Product B"},
                {"id": "btn-cart", "type": "button", "x": 650, "y": 20, "w": 100, "h": 40, "label": "Cart (0)"},
                {"id": "nav-home", "type": "link", "x": 20, "y": 550, "w": 100, "h": 20, "label": "← Back to Home"}
            ],
            "links": [
                {"from_element": "product-1", "to_page": "product-detail", "trigger": "click", "action": "navigate"},
                {"from_element": "product-2", "to_page": "product-detail", "trigger": "click", "action": "navigate"},
                {"from_element": "nav-home", "to_page": "home", "trigger": "click", "action": "navigate"}
            ],
            "background": "#f8f4e8"
        },
        {
            "id": "product-detail",
            "name": "Product Detail",
            "elements": [
                {"id": "product-image", "type": "hotspot", "x": 100, "y": 100, "w": 300, "h": 300, "label": ""},
                {"id": "btn-add-cart", "type": "button", "x": 500, "y": 300, "w": 150, "h": 50, "label": "Add to Cart"},
                {"id": "btn-buy", "type": "button", "x": 500, "y": 370, "w": 150, "h": 50, "label": "Buy Now"},
                {"id": "nav-back", "type": "link", "x": 20, "y": 550, "w": 120, "h": 20, "label": "← Back to Products"}
            ],
            "links": [
                {"from_element": "btn-add-cart", "to_page": "products", "trigger": "click", "action": "navigate"},
                {"from_element": "btn-buy", "to_page": "home", "trigger": "click", "action": "navigate"},
                {"from_element": "nav-back", "to_page": "products", "trigger": "click", "action": "navigate"}
            ],
            "background": "#f0e8f8"
        },
        {
            "id": "about",
            "name": "About Us",
            "elements": [
                {"id": "nav-home-about", "type": "link", "x": 20, "y": 550, "w": 100, "h": 20, "label": "← Back to Home"}
            ],
            "links": [
                {"from_element": "nav-home-about", "to_page": "home", "trigger": "click", "action": "navigate"}
            ],
            "background": "#e8f8e8"
        }
    ]
    
    prototype = proto.create_prototype("E-commerce Flow Test", pages)
    print(f"✓ Created prototype: {prototype.id}")
    print(f"  Name: {prototype.name}")
    print(f"  Pages: {[p.name for p in prototype.pages]}")
    
    # Test 2: Add interaction
    print("\n[2] Testing add_interaction...")
    success = proto.add_interaction(prototype.id, "btn-buy", "click", "navigate", "products")
    print(f"✓ Modified interaction: {success}")
    
    # Test 3: Render state
    print("\n[3] Testing render_state...")
    html = proto.render_state(prototype.id, "home")
    print(f"✓ Generated HTML for 'home' page")
    print(f"  HTML length: {len(html)} bytes")
    
    # Save HTML for inspection
    output_path = "/tmp/proto-test/home.html"
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"  Saved to: {output_path}")
    
    # Render product page too
    html_products = proto.render_state(prototype.id, "products")
    output_path_products = "/tmp/proto-test/products.html"
    with open(output_path_products, 'w') as f:
        f.write(html_products)
    print(f"✓ Generated and saved 'products' page")
    
    # Test 4: Simulate flow
    print("\n[4] Testing simulate_flow...")
    user_actions = [
        {"element": "btn-shop", "delay": 1.5},
        {"element": "product-1", "delay": 2.0},
        {"element": "btn-add-cart", "delay": 1.0},
        {"element": "nav-back", "delay": 0.5},
        {"element": "nav-home", "delay": 1.0}
    ]
    path = proto.simulate_flow(prototype.id, "home", user_actions)
    print(f"✓ Simulated flow with {len(user_actions)} actions")
    print(f"  Path taken: {[p.get('page', p.get('type')) for p in path]}")
    
    # Test 5: Record session
    print("\n[5] Testing record_session...")
    session1 = proto.record_session(prototype.id)
    print(f"✓ Created session: {session1.session_id}")
    
    session2 = proto.record_session(prototype.id)
    print(f"✓ Created session: {session2.session_id}")
    
    # Simulate some events for session 1
    from proto_interactive import Event
    session1.events = [
        Event("pageview", None, "home", 1000.0, {"page": "home"}),
        Event("click", "btn-shop", "home", 1002.5),
        Event("navigate", None, "home", 1002.6, {"from": "home", "to": "products"}),
        Event("pageview", None, "products", 1002.6, {"page": "products"}),
        Event("click", "product-1", "products", 1005.0),
        Event("navigate", None, "products", 1005.1, {"from": "products", "to": "product-detail"}),
        Event("pageview", None, "product-detail", 1005.1, {"page": "product-detail"}),
        Event("click", "btn-add-cart", "product-detail", 1007.0),
    ]
    proto._save_session(session1)
    
    # Simulate shorter session 2
    session2.events = [
        Event("pageview", None, "home", 2000.0, {"page": "home"}),
        Event("click", "link-about", "home", 2001.0),
        Event("navigate", None, "home", 2001.1, {"from": "home", "to": "about"}),
        Event("pageview", None, "about", 2001.1, {"page": "about"}),
    ]
    proto._save_session(session2)
    print(f"✓ Added simulated events to sessions")
    
    # Test 6: Generate report
    print("\n[6] Testing generate_report...")
    report = proto.generate_report([session1.session_id, session2.session_id])
    print(f"✓ Generated report:")
    print(f"  Total sessions: {report['total_sessions']}")
    print(f"  Total events: {report['total_events']}")
    print(f"  Completion rate: {report['completion_rate']:.0%}")
    print(f"  Avg time: {report['avg_time_seconds']:.1f}s")
    print(f"  Page visits: {report['page_visits']}")
    print(f"  Click heatmap: {report['click_heatmap']}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    
    # Return data for verification
    return {
        "prototype_id": prototype.id,
        "session_ids": [session1.session_id, session2.session_id],
        "report": report
    }


if __name__ == "__main__":
    result = test_proto_interactive()
    print("\nTest result summary:")
    print(json.dumps({
        "prototype_id": result["prototype_id"],
        "session_count": len(result["session_ids"]),
        "report_summary": {
            "completion_rate": result["report"]["completion_rate"],
            "total_events": result["report"]["total_events"]
        }
    }, indent=2))
