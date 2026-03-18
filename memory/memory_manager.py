"""
Memory Manager for Geo-AI Engineering
JSON-based comprehensive memory storage
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List

MEMORY_FILE = "/root/.openclaw/workspace/memory/comprehensive_state.json"

def load_memory() -> Dict[str, Any]:
    """Load comprehensive memory from JSON"""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory: Dict[str, Any]):
    """Save memory to JSON"""
    memory['last_updated'] = datetime.now().isoformat()
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def get_component_status(component_name: str) -> Dict[str, Any]:
    """Get status of specific component"""
    mem = load_memory()
    return mem.get('components', {}).get(component_name, {})

def update_component_status(component_name: str, updates: Dict[str, Any]):
    """Update component status"""
    mem = load_memory()
    if 'components' not in mem:
        mem['components'] = {}
    if component_name not in mem['components']:
        mem['components'][component_name] = {}
    
    mem['components'][component_name].update(updates)
    save_memory(mem)

def add_milestone(date: str, milestone: str, deliverables: List[str]):
    """Add new milestone to lineage"""
    mem = load_memory()
    if 'lineage_milestones' not in mem:
        mem['lineage_milestones'] = []
    
    mem['lineage_milestones'].append({
        'date': date,
        'milestone': milestone,
        'deliverables': deliverables
    })
    save_memory(mem)

def get_next_actions() -> List[Dict[str, Any]]:
    """Get prioritized next actions"""
    mem = load_memory()
    return sorted(mem.get('next_actions', []), key=lambda x: x.get('priority', 99))

def complete_action(action_name: str):
    """Mark action as complete"""
    mem = load_memory()
    actions = mem.get('next_actions', [])
    mem['next_actions'] = [a for a in actions if a['action'] != action_name]
    
    # Add to completed
    if 'completed_actions' not in mem:
        mem['completed_actions'] = []
    mem['completed_actions'].append({
        'action': action_name,
        'completed_at': datetime.now().isoformat()
    })
    
    save_memory(mem)

def print_status():
    """Print human-readable status"""
    mem = load_memory()
    
    print("🜁 Geo-AI Engineering — Comprehensive Status")
    print("=" * 60)
    print(f"Last Updated: {mem.get('last_updated', 'Unknown')}")
    print(f"Current Focus: {mem.get('project', {}).get('current_focus', 'Unknown')}")
    print()
    
    # Components
    print("Components:")
    for name, comp in mem.get('components', {}).items():
        status = comp.get('status', 'Unknown')
        icon = "✓" if status in ['COMPLETE', 'READY'] else "⏸" if status == 'PAUSED' else "○"
        print(f"  {icon} {name}: {status}")
    
    print()
    
    # Next actions
    print("Next Actions:")
    for action in get_next_actions()[:5]:
        print(f"  {action['priority']}. {action['action']}")
    
    print()
    
    # Invariants
    print("Invariants Maintained:")
    for inv, val in mem.get('invariants', {}).items():
        if isinstance(val, (int, float, bool, str)) and len(str(val)) < 50:
            print(f"  • {inv}: {val}")

if __name__ == "__main__":
    print_status()
