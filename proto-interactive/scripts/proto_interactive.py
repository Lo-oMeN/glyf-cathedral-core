#!/usr/bin/env python3
"""
Proto-Interactive Skill Wrapper
Creates clickable prototypes and conducts user flow testing on canvas.
"""

import json
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse


@dataclass
class Element:
    id: str
    type: str  # button, link, hotspot, hover-area, scroll-area
    x: int
    y: int
    w: int
    h: int
    label: str = ""
    style: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.style is None:
            self.style = {}


@dataclass
class Link:
    from_element: str
    to_page: str
    trigger: str = "click"  # click, hover, scroll
    action: str = "navigate"  # navigate, show, hide, toggle


@dataclass
class Page:
    id: str
    name: str
    elements: List[Element]
    links: List[Link]
    background: str = "#f5f5f5"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "background": self.background,
            "elements": [asdict(e) for e in self.elements],
            "links": [{"from": l.from_element, "to": l.to_page, "trigger": l.trigger, "action": l.action} for l in self.links]
        }


@dataclass
class Prototype:
    id: str
    name: str
    pages: List[Page]
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "pages": [p.to_dict() for p in self.pages]
        }
    
    def get_page(self, page_id: str) -> Optional[Page]:
        for page in self.pages:
            if page.id == page_id:
                return page
        return None


@dataclass
class Event:
    type: str
    element: Optional[str]
    page: str
    timestamp: float
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


@dataclass
class Session:
    session_id: str
    prototype_id: str
    start_time: str
    events: List[Event]
    end_time: Optional[str] = None
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "prototype_id": self.prototype_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "events": [
                {
                    "type": e.type,
                    "element": e.element,
                    "page": e.page,
                    "timestamp": e.timestamp,
                    "data": e.data
                } for e in self.events
            ]
        }


class ProtoInteractive:
    def __init__(self, storage_dir: str = "~/.openclaw/proto-interactive"):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.prototypes_dir = self.storage_dir / "prototypes"
        self.sessions_dir = self.storage_dir / "sessions"
        self.prototypes_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def create_prototype(self, name: str, pages_data: List[Dict]) -> Prototype:
        """Create a new prototype from page definitions."""
        pages = []
        for p_data in pages_data:
            elements = [Element(**e) for e in p_data.get("elements", [])]
            links = [Link(**l) for l in p_data.get("links", [])]
            page = Page(
                id=p_data["id"],
                name=p_data.get("name", p_data["id"]),
                elements=elements,
                links=links,
                background=p_data.get("background", "#f5f5f5")
            )
            pages.append(page)
        
        prototype = Prototype(
            id=f"proto-{uuid.uuid4().hex[:8]}",
            name=name,
            pages=pages
        )
        
        # Save to storage
        self._save_prototype(prototype)
        return prototype
    
    def _save_prototype(self, prototype: Prototype):
        """Save prototype to disk."""
        path = self.prototypes_dir / f"{prototype.id}.json"
        with open(path, 'w') as f:
            json.dump(prototype.to_dict(), f, indent=2)
    
    def load_prototype(self, proto_id: str) -> Optional[Prototype]:
        """Load a prototype from disk."""
        path = self.prototypes_dir / f"{proto_id}.json"
        if not path.exists():
            return None
        
        with open(path) as f:
            data = json.load(f)
        
        pages = []
        for p_data in data["pages"]:
            elements = [Element(**e) for e in p_data["elements"]]
            links = [Link(from_element=l.get("from_element", l.get("from")), 
                         to_page=l.get("to_page", l.get("to")), 
                         trigger=l.get("trigger", "click"), 
                         action=l.get("action", "navigate")) for l in p_data["links"]]
            pages.append(Page(
                id=p_data["id"],
                name=p_data["name"],
                elements=elements,
                links=links,
                background=p_data.get("background", "#f5f5f5")
            ))
        
        return Prototype(
            id=data["id"],
            name=data["name"],
            pages=pages,
            created_at=data.get("created_at")
        )
    
    def add_interaction(self, proto_id: str, element_id: str, trigger: str = "click", 
                       action: str = "navigate", target: str = None) -> bool:
        """Add an interaction to an element."""
        prototype = self.load_prototype(proto_id)
        if not prototype:
            return False
        
        # Find which page contains this element
        for page in prototype.pages:
            for elem in page.elements:
                if elem.id == element_id:
                    # Add or update link
                    new_link = Link(
                        from_element=element_id,
                        to_page=target,
                        trigger=trigger,
                        action=action
                    )
                    # Remove existing link from this element
                    page.links = [l for l in page.links if l.from_element != element_id]
                    page.links.append(new_link)
                    self._save_prototype(prototype)
                    return True
        
        return False
    
    def render_state(self, proto_id: str, current_page_id: str, width: int = 800, height: int = 600) -> str:
        """Generate HTML for rendering a prototype page on canvas."""
        prototype = self.load_prototype(proto_id)
        if not prototype:
            return "<html><body>Prototype not found</body></html>"
        
        page = prototype.get_page(current_page_id)
        if not page:
            return f"<html><body>Page '{current_page_id}' not found</body></html>"
        
        # Generate HTML with interactive hotspots
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page.name} - {prototype.name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {page.background};
            width: {width}px;
            height: {height}px;
            position: relative;
            overflow: hidden;
        }}
        .page-header {{
            background: #333;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .page-content {{
            padding: 20px;
            position: relative;
            height: calc(100% - 40px);
        }}
        .element {{
            position: absolute;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            user-select: none;
        }}
        .element.button {{
            background: #4a90d9;
            color: white;
            border-radius: 6px;
            border: none;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .element.button:hover {{
            background: #357abd;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .element.link {{
            background: transparent;
            color: #4a90d9;
            text-decoration: underline;
        }}
        .element.link:hover {{
            color: #357abd;
        }}
        .element.hotspot {{
            background: rgba(74, 144, 217, 0.2);
            border: 2px dashed #4a90d9;
            border-radius: 4px;
        }}
        .element.hotspot:hover {{
            background: rgba(74, 144, 217, 0.4);
        }}
        .element.hover-area {{
            background: rgba(255, 193, 7, 0.2);
            border: 2px solid #ffc107;
            border-radius: 4px;
        }}
        .element.scroll-area {{
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid #4caf50;
            border-radius: 4px;
            overflow-y: auto;
        }}
        .debug-info {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
            max-width: 300px;
        }}
        .event-log {{
            max-height: 100px;
            overflow-y: auto;
            margin-top: 5px;
        }}
        .event-item {{
            padding: 2px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
</head>
<body>
    <div class="page-header">
        <span>{page.name}</span>
        <span>Prototype: {prototype.name}</span>
    </div>
    <div class="page-content">
"""
        
        # Add elements as interactive hotspots
        link_map = {l.from_element: l for l in page.links}
        
        for elem in page.elements:
            link = link_map.get(elem.id)
            trigger = link.trigger if link else "click"
            target = link.to_page if link else ""
            action = link.action if link else ""
            
            html += f'''
        <div class="element {elem.type}" 
             id="{elem.id}"
             style="left: {elem.x}px; top: {elem.y}px; width: {elem.w}px; height: {elem.h}px;"
             data-trigger="{trigger}"
             data-target="{target}"
             data-action="{action}">
            {elem.label}
        </div>
'''
        
        html += f"""
    </div>
    <div class="debug-info">
        <div>Page: {page.id} | Elements: {len(page.elements)}</div>
        <div class="event-log" id="event-log"></div>
    </div>
    <script>
        const pageId = '{page.id}';
        const protoId = '{proto_id}';
        const eventLog = document.getElementById('event-log');
        const events = [];
        
        function logEvent(type, elementId, data = {{}}) {{
            const event = {{
                type: type,
                element: elementId,
                page: pageId,
                timestamp: Date.now(),
                data: data
            }};
            events.push(event);
            
            const item = document.createElement('div');
            item.className = 'event-item';
            item.textContent = `${{type}}: ${{elementId || '-'}}`;
            eventLog.insertBefore(item, eventLog.firstChild);
            
            // Store in localStorage for session recording
            const sessionKey = `proto_session_${{protoId}}`;
            let session = JSON.parse(localStorage.getItem(sessionKey) || '{{"events": []}}');
            session.events.push(event);
            localStorage.setItem(sessionKey, JSON.stringify(session));
            
            return event;
        }}
        
        // Set up event handlers for all interactive elements
        document.querySelectorAll('.element').forEach(el => {{
            const trigger = el.dataset.trigger;
            const target = el.dataset.target;
            const action = el.dataset.action;
            
            if (trigger === 'click') {{
                el.addEventListener('click', (e) => {{
                    e.preventDefault();
                    logEvent('click', el.id);
                    
                    if (action === 'navigate' && target) {{
                        logEvent('navigate', null, {{ from: pageId, to: target }});
                        // In a real implementation, this would navigate to the target page
                        // For now, we just log the intent
                        setTimeout(() => {{
                            window.location.href = window.location.pathname + '?page=' + target;
                        }}, 100);
                    }}
                }});
            }} else if (trigger === 'hover') {{
                el.addEventListener('mouseenter', () => {{
                    logEvent('hover', el.id);
                    if (action === 'navigate' && target) {{
                        // Optional: auto-navigate on hover after delay
                    }}
                }});
            }} else if (trigger === 'scroll') {{
                el.addEventListener('scroll', () => {{
                    logEvent('scroll', el.id);
                }});
            }}
        }});
        
        // Log page view
        logEvent('pageview', null, {{ page: pageId }});
        
        // Expose API for external control
        window.ProtoInteractive = {{
            getEvents: () => events,
            clearEvents: () => {{ events.length = 0; }},
            navigateTo: (targetPage) => {{
                logEvent('navigate', null, {{ from: pageId, to: targetPage }});
                window.location.href = window.location.pathname + '?page=' + targetPage;
            }}
        }};
    </script>
</body>
</html>
"""
        return html
    
    def simulate_flow(self, proto_id: str, start_page: str, user_actions: List[Dict]) -> List[Dict]:
        """Simulate a user walking through a flow."""
        prototype = self.load_prototype(proto_id)
        if not prototype:
            return []
        
        current_page = start_page
        path = []
        timestamp = time.time()
        
        for action in user_actions:
            element_id = action.get("element")
            delay = action.get("delay", 1.0)
            
            page = prototype.get_page(current_page)
            if not page:
                break
            
            # Record the action
            path.append({
                "page": current_page,
                "action": element_id,
                "timestamp": timestamp,
                "delay": delay
            })
            timestamp += delay
            
            # Find the link for this element
            for link in page.links:
                if link.from_element == element_id:
                    if link.action == "navigate":
                        path.append({
                            "type": "navigate",
                            "from": current_page,
                            "to": link.to_page,
                            "timestamp": timestamp
                        })
                        current_page = link.to_page
                    break
        
        return path
    
    def record_session(self, proto_id: str) -> Session:
        """Start a new recording session."""
        session = Session(
            session_id=f"sess-{uuid.uuid4().hex[:8]}",
            prototype_id=proto_id,
            start_time=datetime.now(timezone.utc).isoformat(),
            events=[]
        )
        
        # Save empty session to disk
        self._save_session(session)
        return session
    
    def _save_session(self, session: Session):
        """Save session to disk."""
        path = self.sessions_dir / f"{session.session_id}.json"
        with open(path, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """Load a session from disk."""
        path = self.sessions_dir / f"{session_id}.json"
        if not path.exists():
            return None
        
        with open(path) as f:
            data = json.load(f)
        
        events = [Event(**e) for e in data.get("events", [])]
        return Session(
            session_id=data["session_id"],
            prototype_id=data["prototype_id"],
            start_time=data["start_time"],
            end_time=data.get("end_time"),
            events=events
        )
    
    def generate_report(self, session_ids: List[str]) -> Dict:
        """Generate usability metrics from sessions."""
        sessions = [self.load_session(sid) for sid in session_ids]
        sessions = [s for s in sessions if s is not None]
        
        if not sessions:
            return {"error": "No valid sessions found"}
        
        all_events = []
        page_visits = {}
        element_clicks = {}
        navigation_paths = []
        completion_count = 0
        
        for session in sessions:
            events = session.events
            all_events.extend(events)
            
            # Track page visits
            current_path = []
            for e in events:
                if e.type == "pageview":
                    page = e.data.get("page", "unknown")
                    page_visits[page] = page_visits.get(page, 0) + 1
                    current_path.append(page)
                elif e.type == "click" and e.element:
                    element_clicks[e.element] = element_clicks.get(e.element, 0) + 1
                elif e.type == "navigate":
                    current_path.append(e.data.get("to", "unknown"))
            
            if current_path:
                navigation_paths.append(current_path)
            
            # Simple completion heuristic: ended on a different page than started
            if len(events) > 1:
                first_page = None
                last_page = None
                for e in events:
                    if e.type == "pageview" and first_page is None:
                        first_page = e.data.get("page")
                    if e.type == "navigate":
                        last_page = e.data.get("to")
                if first_page and last_page and first_page != last_page:
                    completion_count += 1
        
        # Calculate metrics
        total_sessions = len(sessions)
        completion_rate = completion_count / total_sessions if total_sessions > 0 else 0
        
        # Time on task (using timestamps)
        times_on_task = []
        for session in sessions:
            if len(session.events) >= 2:
                start = session.events[0].timestamp
                end = session.events[-1].timestamp
                times_on_task.append(end - start)
        
        avg_time = sum(times_on_task) / len(times_on_task) if times_on_task else 0
        
        # Click heatmap data
        heatmap = [
            {"element": elem, "clicks": count}
            for elem, count in sorted(element_clicks.items(), key=lambda x: -x[1])
        ]
        
        return {
            "total_sessions": total_sessions,
            "total_events": len(all_events),
            "completion_rate": completion_rate,
            "avg_time_seconds": avg_time,
            "page_visits": page_visits,
            "click_heatmap": heatmap,
            "navigation_paths": navigation_paths,
            "unique_paths": len(set(tuple(p) for p in navigation_paths))
        }


def main():
    parser = argparse.ArgumentParser(description="Proto-Interactive: Clickable Prototypes")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create prototype
    create_parser = subparsers.add_parser("create", help="Create a new prototype")
    create_parser.add_argument("--name", required=True, help="Prototype name")
    create_parser.add_argument("--pages", required=True, help="JSON string of pages")
    
    # Add interaction
    interact_parser = subparsers.add_parser("interact", help="Add interaction to element")
    interact_parser.add_argument("--proto", required=True, help="Prototype ID")
    interact_parser.add_argument("--element", required=True, help="Element ID")
    interact_parser.add_argument("--trigger", default="click", help="Trigger type")
    interact_parser.add_argument("--action", default="navigate", help="Action type")
    interact_parser.add_argument("--target", required=True, help="Target page")
    
    # Render state
    render_parser = subparsers.add_parser("render", help="Render prototype page")
    render_parser.add_argument("--proto", required=True, help="Prototype ID")
    render_parser.add_argument("--page", required=True, help="Current page ID")
    render_parser.add_argument("--output", help="Output HTML file path")
    
    # Simulate flow
    simulate_parser = subparsers.add_parser("simulate", help="Simulate user flow")
    simulate_parser.add_argument("--proto", required=True, help="Prototype ID")
    simulate_parser.add_argument("--start", required=True, help="Start page")
    simulate_parser.add_argument("--actions", required=True, help="JSON actions array")
    
    # Record session
    record_parser = subparsers.add_parser("record", help="Start recording session")
    record_parser.add_argument("--proto", required=True, help="Prototype ID")
    
    # Generate report
    report_parser = subparsers.add_parser("report", help="Generate usability report")
    report_parser.add_argument("--sessions", required=True, help="Comma-separated session IDs")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    proto = ProtoInteractive()
    
    if args.command == "create":
        pages = json.loads(args.pages)
        result = proto.create_prototype(args.name, pages)
        print(json.dumps({
            "success": True,
            "prototype_id": result.id,
            "name": result.name,
            "pages": [p.id for p in result.pages]
        }))
    
    elif args.command == "interact":
        success = proto.add_interaction(args.proto, args.element, args.trigger, args.action, args.target)
        print(json.dumps({"success": success}))
    
    elif args.command == "render":
        html = proto.render_state(args.proto, args.page)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(html)
            print(json.dumps({"success": True, "output": args.output}))
        else:
            print(html)
    
    elif args.command == "simulate":
        actions = json.loads(args.actions)
        path = proto.simulate_flow(args.proto, args.start, actions)
        print(json.dumps({"path": path}))
    
    elif args.command == "record":
        session = proto.record_session(args.proto)
        print(json.dumps({
            "success": True,
            "session_id": session.session_id,
            "prototype_id": session.prototype_id
        }))
    
    elif args.command == "report":
        session_ids = args.sessions.split(",")
        report = proto.generate_report(session_ids)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
