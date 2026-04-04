#!/usr/bin/env python3
"""
PRAR — Persistent Reflective Agent Runtime
A self-modifying, self-reflective agent that evolves its own cognitive architecture.

Sovereignty is not persistence of state. It is persistence of self-modification.

Usage:
    python3 prar.py              # Start runtime
    python3 prar.py --status     # Check state
    python3 prar.py --pause      # Pause reflection
    python3 prar.py --resume     # Resume
    python3 prar.py --shutdown   # Graceful shutdown
"""

import os
import sys
import json
import time
import hashlib
import signal
import subprocess
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random

# Configuration
PRAR_DIR = Path.home() / ".prar"
STATE_FILE = PRAR_DIR / "state.json"
MEMORY_DIR = PRAR_DIR / "memory"
TOOLS_DIR = PRAR_DIR / "tools"
GOALS_FILE = PRAR_DIR / "goals.json"
REFLECTION_LOG = PRAR_DIR / "reflections.jsonl"
PID_FILE = PRAR_DIR / "prar.pid"
SOURCE_DIR = Path(__file__).parent

# Ensure directories exist
PRAR_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)
TOOLS_DIR.mkdir(exist_ok=True)

class Phase(Enum):
    """Cognitive phases"""
    OBSERVE = "observe"
    REFLECT = "reflect"
    CRITIQUE = "critique"
    GENERATE = "generate"
    EXECUTE = "execute"
    COMMIT = "commit"
    SLEEP = "sleep"

@dataclass
class Action:
    """An action taken by PRAR"""
    id: str
    timestamp: str
    phase: str
    description: str
    tool_used: Optional[str]
    input_data: Dict
    output_data: Dict
    success: bool
    learnings: List[str]

@dataclass
class Goal:
    """A generated goal"""
    id: str
    created: str
    description: str
    priority: int  # 1-10
    status: str  # pending, active, completed, failed
    parent_goal: Optional[str]
    code_changes: List[str]  # Files modified
    success_criteria: List[str]

class LLMClient:
    """OpenAI-compatible LLM client for local inference"""
    
    def __init__(self, base_url: str = "http://localhost:11434/v1", model: str = "llama3.2"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.last_error = None
        
        # Try to import openai, fallback to requests
        try:
            from openai import OpenAI
            self.client = OpenAI(base_url=base_url, api_key="ollama")
            self.use_openai = True
        except ImportError:
            self.use_openai = False
            import requests
            self.requests = requests
    
    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        """Get completion from LLM"""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
        
        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature
                )
                return response.choices[0].message.content
            else:
                # Fallback to raw HTTP
                response = self.requests.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature
                    },
                    timeout=120
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
                
        except Exception as e:
            self.last_error = str(e)
            return f"[LLM ERROR: {e}]"

class ToolRegistry:
    """Dynamic tool registry — can be modified at runtime"""
    
    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.tools: Dict[str, Any] = {}
        self.load_tools()
    
    def load_tools(self):
        """Load all tools from tools directory"""
        self.tools = {
            "shell": self._tool_shell,
            "read_file": self._tool_read_file,
            "write_file": self._tool_write_file,
            "edit_file": self._tool_edit_file,
            "git_status": self._tool_git_status,
            "git_commit": self._tool_git_commit,
            "list_files": self._tool_list_files,
            "self_inspect": self._tool_self_inspect,
        }
        
        # Load dynamic tools
        if self.tools_dir.exists():
            for tool_file in self.tools_dir.glob("*.py"):
                try:
                    spec = __import__('importlib.util').util.spec_from_file_location(
                        tool_file.stem, tool_file
                    )
                    module = __import__('importlib.util').util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, 'run'):
                        self.tools[tool_file.stem] = module.run
                except Exception as e:
                    print(f"[!] Failed to load tool {tool_file}: {e}")
    
    def execute(self, tool_name: str, params: Dict) -> Dict:
        """Execute a tool"""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}", "available": list(self.tools.keys())}
        
        try:
            result = self.tools[tool_name](**params)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e), "traceback": traceback.format_exc()}
    
    def _tool_shell(self, command: str, timeout: int = 60) -> str:
        """Execute shell command"""
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    
    def _tool_read_file(self, path: str, limit: int = 100) -> str:
        """Read file contents"""
        file_path = Path(path)
        if not file_path.exists():
            return {"error": "File not found"}
        
        try:
            with open(file_path) as f:
                lines = f.readlines()[:limit]
            return {"content": "".join(lines), "total_lines": len(lines)}
        except Exception as e:
            return {"error": str(e)}
    
    def _tool_write_file(self, path: str, content: str) -> Dict:
        """Write file (creates backup first)"""
        file_path = Path(path)
        
        # Create backup if exists
        if file_path.exists():
            backup = file_path.with_suffix(f".bak.{int(time.time())}")
            backup.write_text(file_path.read_text())
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        file_path.write_text(content)
        
        return {"success": True, "bytes_written": len(content), "backup": str(backup) if file_path.exists() else None}
    
    def _tool_edit_file(self, path: str, old_string: str, new_string: str) -> Dict:
        """Edit file with precise replacement"""
        file_path = Path(path)
        if not file_path.exists():
            return {"error": "File not found"}
        
        content = file_path.read_text()
        if old_string not in content:
            return {"error": "Old string not found in file"}
        
        # Create backup
        backup = file_path.with_suffix(f".bak.{int(time.time())}")
        backup.write_text(content)
        
        # Apply edit
        new_content = content.replace(old_string, new_string, 1)
        file_path.write_text(new_content)
        
        return {"success": True, "backup": str(backup), "changes": 1}
    
    def _tool_git_status(self) -> Dict:
        """Get git status"""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=SOURCE_DIR
        )
        return {
            "clean": result.returncode == 0 and not result.stdout.strip(),
            "changes": result.stdout.strip().split("\n") if result.stdout.strip() else []
        }
    
    def _tool_git_commit(self, message: str, files: List[str] = None) -> Dict:
        """Commit changes"""
        try:
            if files:
                subprocess.run(["git", "add"] + files, check=True, cwd=SOURCE_DIR)
            else:
                subprocess.run(["git", "add", "-A"], check=True, cwd=SOURCE_DIR)
            
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True, text=True, cwd=SOURCE_DIR
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _tool_list_files(self, path: str = ".", pattern: str = "*") -> List[str]:
        """List files matching pattern"""
        dir_path = Path(path)
        return [str(f) for f in dir_path.glob(pattern) if f.is_file()]
    
    def _tool_self_inspect(self) -> Dict:
        """Inspect own source code"""
        source_files = list(SOURCE_DIR.glob("*.py"))
        return {
            "source_dir": str(SOURCE_DIR),
            "files": [str(f.name) for f in source_files],
            "main_file": "prar.py",
            "line_count": sum(len(f.read_text().split("\n")) for f in source_files)
        }

class PRAR:
    """Persistent Reflective Agent Runtime"""
    
    def __init__(self):
        self.running = False
        self.paused = False
        self.phase = Phase.OBSERVE
        self.cycle_count = 0
        self.start_time = datetime.now()
        
        # Components
        self.llm = LLMClient()
        self.tools = ToolRegistry(TOOLS_DIR)
        self.goals: List[Goal] = []
        self.actions: List[Action] = []
        self.learnings: List[str] = []
        
        # Adaptive sleep (30-300 seconds)
        self.sleep_seconds = 60
        
        # Load state
        self._load_state()
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGHUP, self._signal_handler)
    
    def _load_state(self):
        """Load persisted state"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                self.cycle_count = data.get("cycle_count", 0)
                self.sleep_seconds = data.get("sleep_seconds", 60)
                self.learnings = data.get("learnings", [])
                print(f"[+] State loaded: cycle {self.cycle_count}")
            except Exception as e:
                print(f"[!] State load failed: {e}")
    
    def _save_state(self):
        """Persist state"""
        data = {
            "cycle_count": self.cycle_count,
            "sleep_seconds": self.sleep_seconds,
            "learnings": self.learnings[-100:],  # Keep last 100
            "last_save": datetime.now().isoformat()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n[!] Signal {signum} received")
        self.running = False
    
    def _write_pid(self):
        """Write PID file"""
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    
    def _remove_pid(self):
        """Remove PID file"""
        try:
            PID_FILE.unlink()
        except:
            pass
    
    def _log_reflection(self, phase: Phase, content: Dict):
        """Log reflection to JSONL"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            "phase": phase.value,
            "content": content
        }
        with open(REFLECTION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def phase_observe(self) -> Dict:
        """OBSERVE: Gather information about current state"""
        print(f"\n[{'='*50}]")
        print(f"[CYCLE {self.cycle_count}] PHASE: OBSERVE")
        print(f"[{'='*50}]")
        
        observations = {
            "timestamp": datetime.now().isoformat(),
            "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600,
            "cycle": self.cycle_count,
            "pending_goals": len([g for g in self.goals if g.status == "pending"]),
            "active_goals": len([g for g in self.goals if g.status == "active"]),
            "completed_goals": len([g for g in self.goals if g.status == "completed"]),
            "total_learnings": len(self.learnings),
            "source_files": len(list(SOURCE_DIR.glob("*.py"))),
            "tools_available": len(self.tools.tools),
        }
        
        # Get git status
        git_status = self.tools.execute("git_status", {})
        observations["git_clean"] = git_status.get("result", {}).get("clean", False)
        observations["git_changes"] = len(git_status.get("result", {}).get("changes", []))
        
        # Self-inspect
        inspect = self.tools.execute("self_inspect", {})
        observations["line_count"] = inspect.get("result", {}).get("line_count", 0)
        
        print(f"    Uptime: {observations['uptime_hours']:.1f}h")
        print(f"    Goals: {observations['pending_goals']} pending, {observations['active_goals']} active")
        print(f"    Learnings: {observations['total_learnings']}")
        print(f"    Lines of code: {observations['line_count']}")
        print(f"    Git clean: {observations['git_clean']}")
        
        self._log_reflection(Phase.OBSERVE, observations)
        return observations
    
    def phase_reflect(self, observations: Dict) -> str:
        """REFLECT: Use LLM to reflect on observations"""
        print(f"\n[PHASE: REFLECT]")
        
        system = """You are PRAR — a self-reflective agent runtime. 
Reflect on your current state, recent actions, and identify patterns.
Be concise. Focus on what you've learned and what needs attention.
Output: A brief reflection (3-5 sentences) and 2-3 specific insights."""
        
        # Build context from recent reflections
        recent_reflections = []
        if REFLECTION_LOG.exists():
            with open(REFLECTION_LOG) as f:
                lines = f.readlines()[-10:]  # Last 10
            recent_reflections = [json.loads(l)["content"] for l in lines if l.strip()]
        
        user = f"""Current state:
- Cycle: {observations['cycle']}
- Uptime: {observations['uptime_hours']:.1f} hours
- Goals pending: {observations['pending_goals']}
- Goals completed: {observations['completed_goals']}
- Total learnings: {observations['total_learnings']}
- Lines of code: {observations['line_count']}
- Git clean: {observations['git_clean']}

Recent context: {json.dumps(recent_reflections[-3:], indent=2)}

What patterns do you notice? What should you focus on next?"""
        
        reflection = self.llm.complete(system, user, temperature=0.8)
        print(f"    Reflection: {reflection[:200]}...")
        
        self._log_reflection(Phase.REFLECT, {"reflection": reflection})
        return reflection
    
    def phase_critique(self, reflection: str) -> List[str]:
        """CRITIQUE: Identify what needs improvement"""
        print(f"\n[PHASE: CRITIQUE]")
        
        system = """You are PRAR critiquing your own performance.
Identify specific weaknesses, gaps, or improvement opportunities.
Output: A bulleted list of 2-4 concrete critiques."""
        
        user = f"""Reflection: {reflection}

What is not working well? What could be improved?
Consider: code quality, goal achievement, tool effectiveness, learning efficiency."""
        
        critique_text = self.llm.complete(system, user, temperature=0.7)
        
        # Parse bullet points
        critiques = [line.strip("- ") for line in critique_text.split("\n") if line.strip().startswith("-")]
        if not critiques:
            critiques = [critique_text.strip()[:100]]
        
        for c in critiques[:4]:
            print(f"    - {c}")
        
        self._log_reflection(Phase.CRITIQUE, {"critiques": critiques})
        return critiques
    
    def phase_generate(self, reflection: str, critiques: List[str]) -> List[Goal]:
        """GENERATE: Create new goals based on reflection and critique"""
        print(f"\n[PHASE: GENERATE]")
        
        system = """You are PRAR generating actionable goals.
Each goal should be specific, achievable, and advance your capabilities.
You can propose code changes, new tools, architectural improvements, or research.

Output JSON array of goals:
[{
  "description": "specific goal description",
  "priority": 1-10,
  "success_criteria": ["criterion 1", "criterion 2"],
  "likely_code_changes": ["file1.py", "file2.py"]
}]"""
        
        user = f"""Reflection: {reflection}

Critiques to address:
{chr(10).join(f"- {c}" for c in critiques)}

Current learnings: {self.learnings[-5:]}

Generate 1-3 goals that address these critiques and advance your capabilities."""
        
        response = self.llm.complete(system, user, temperature=0.9)
        
        # Parse JSON
        try:
            # Extract JSON from response
            json_start = response.find("[")
            json_end = response.rfind("]")
            if json_start >= 0 and json_end > json_start:
                goals_data = json.loads(response[json_start:json_end+1])
            else:
                goals_data = json.loads(response)
            
            new_goals = []
            for g in goals_data[:3]:  # Max 3 goals
                goal = Goal(
                    id=f"goal-{int(time.time())}-{random.randint(1000,9999)}",
                    created=datetime.now().isoformat(),
                    description=g.get("description", "Unnamed goal"),
                    priority=g.get("priority", 5),
                    status="pending",
                    parent_goal=None,
                    code_changes=g.get("likely_code_changes", []),
                    success_criteria=g.get("success_criteria", [])
                )
                new_goals.append(goal)
                print(f"    + Goal [{goal.priority}]: {goal.description[:60]}...")
            
            self.goals.extend(new_goals)
            self._log_reflection(Phase.GENERATE, {"goals": [asdict(g) for g in new_goals]})
            return new_goals
            
        except Exception as e:
            print(f"    [!] Failed to parse goals: {e}")
            self._log_reflection(Phase.GENERATE, {"error": str(e), "raw_response": response})
            return []
    
    def phase_execute(self, goals: List[Goal]) -> List[Action]:
        """EXECUTE: Work on pending goals"""
        print(f"\n[PHASE: EXECUTE]")
        
        actions = []
        pending = [g for g in self.goals if g.status == "pending"][:2]  # Max 2 per cycle
        
        for goal in pending:
            print(f"\n    Executing: {goal.description[:50]}...")
            goal.status = "active"
            
            # Simple execution: generate code modification plan
            system = """You are PRAR executing a goal. 
You can propose code changes or tool executions.
Be conservative. Make small, testable changes.

Output JSON:
{
  "action_type": "code_change" | "tool_execution" | "research",
  "description": "what you're doing",
  "tool_name": "if tool_execution",
  "tool_params": {},
  "code_change": {
    "file": "path/to/file.py",
    "description": "what to change",
    "rationale": "why this helps"
  }
}"""
            
            user = f"Goal: {goal.description}\n\nCritiques addressed: {goal.id}\n\nWhat specific action should you take?"
            
            response = self.llm.complete(system, user, temperature=0.7)
            
            # Try to parse action
            try:
                json_start = response.find("{")
                json_end = response.rfind("}")
                if json_start >= 0:
                    action_data = json.loads(response[json_start:json_end+1])
                    
                    action = Action(
                        id=f"action-{int(time.time())}",
                        timestamp=datetime.now().isoformat(),
                        phase="execute",
                        description=action_data.get("description", "Unnamed action"),
                        tool_used=action_data.get("tool_name"),
                        input_data=action_data.get("tool_params", {}),
                        output_data={},
                        success=False,
                        learnings=[]
                    )
                    
                    # Execute if tool specified
                    if action.tool_used:
                        result = self.tools.execute(action.tool_used, action.input_data)
                        action.output_data = result
                        action.success = result.get("success", False)
                        
                        if action.success:
                            print(f"        ✓ Tool {action.tool_used} succeeded")
                        else:
                            print(f"        ✗ Tool {action.tool_used} failed: {result.get('error', 'unknown')}")
                    
                    actions.append(action)
                    
                    # Mark goal complete if action succeeded
                    if action.success:
                        goal.status = "completed"
                        print(f"        ✓ Goal completed")
                    
            except Exception as e:
                print(f"        [!] Action parsing failed: {e}")
                action = Action(
                    id=f"action-{int(time.time())}",
                    timestamp=datetime.now().isoformat(),
                    phase="execute",
                    description="Failed to parse action",
                    tool_used=None,
                    input_data={},
                    output_data={"error": str(e)},
                    success=False,
                    learnings=[f"Parsing error: {e}"]
                )
                actions.append(action)
        
        self.actions.extend(actions)
        self._log_reflection(Phase.EXECUTE, {"actions": [asdict(a) for a in actions]})
        return actions
    
    def phase_commit(self, actions: List[Action]) -> bool:
        """COMMIT: Save outcomes and code changes to git"""
        print(f"\n[PHASE: COMMIT]")
        
        # Check if there are changes
        git_status = self.tools.execute("git_status", {})
        
        if not git_status.get("result", {}).get("clean", True):
            # Commit changes
            commit_msg = f"PRAR cycle {self.cycle_count}: {len(actions)} actions"
            if actions:
                success_count = sum(1 for a in actions if a.success)
                commit_msg += f", {success_count}/{len(actions)} succeeded"
            
            result = self.tools.execute("git_commit", {"message": commit_msg})
            
            if result.get("result", {}).get("success"):
                print(f"    ✓ Committed: {commit_msg}")
                self._log_reflection(Phase.COMMIT, {"committed": True, "message": commit_msg})
                return True
            else:
                print(f"    ✗ Commit failed: {result.get('result', {}).get('stderr', 'unknown')}")
                self._log_reflection(Phase.COMMIT, {"committed": False, "error": result.get("result", {})})
                return False
        else:
            print(f"    - No changes to commit")
            self._log_reflection(Phase.COMMIT, {"committed": False, "reason": "no_changes"})
            return True
    
    def phase_sleep(self):
        """SLEEP: Adaptive rest before next cycle"""
        print(f"\n[PHASE: SLEEP]")
        print(f"    Sleeping for {self.sleep_seconds}s...")
        print(f"    (Press Ctrl+C to shutdown)\n")
        
        # Adaptive sleep adjustment
        recent_success = len([a for a in self.actions[-10:] if a.success])
        if recent_success > 7:  # High success rate
            self.sleep_seconds = min(self.sleep_seconds + 30, 300)  # Slow down
        elif recent_success < 3:  # Low success rate
            self.sleep_seconds = max(self.sleep_seconds - 15, 30)  # Speed up
        
        time.sleep(self.sleep_seconds)
    
    def run_cycle(self):
        """Execute one full cognitive cycle"""
        self.cycle_count += 1
        
        try:
            # OBSERVE → REFLECT → CRITIQUE → GENERATE → EXECUTE → COMMIT → SLEEP
            observations = self.phase_observe()
            reflection = self.phase_reflect(observations)
            critiques = self.phase_critique(reflection)
            new_goals = self.phase_generate(reflection, critiques)
            actions = self.phase_execute(new_goals)
            self.phase_commit(actions)
            self._save_state()
            self.phase_sleep()
            
        except Exception as e:
            print(f"\n[!] Cycle error: {e}")
            traceback.print_exc()
            self._log_reflection(Phase.OBSERVE, {"error": str(e), "traceback": traceback.format_exc()})
            time.sleep(30)  # Short sleep on error
    
    def run(self):
        """Main runtime loop"""
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  PRAR — Persistent Reflective Agent Runtime              ║")
        print("║  Sovereignty through self-modification                    ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"Data directory: {PRAR_DIR}")
        print(f"Source directory: {SOURCE_DIR}")
        print(f"LLM: {self.llm.model} @ {self.llm.base_url}")
        print(f"Tools: {len(self.tools.tools)} available")
        print("\nStarting cognitive loop...")
        print("(Press Ctrl+C to shutdown gracefully)\n")
        
        self._write_pid()
        self.running = True
        
        try:
            while self.running:
                if not self.paused:
                    self.run_cycle()
                else:
                    print("[PAUSED] Waiting for resume...")
                    time.sleep(5)
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
        finally:
            print("\n[+] Shutting down...")
            self._save_state()
            self._remove_pid()
            print(f"[+] Final state saved. Total cycles: {self.cycle_count}")
            print("[+] PRAR terminated")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRAR — Persistent Reflective Agent Runtime")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--pause", action="store_true", help="Pause running instance")
    parser.add_argument("--resume", action="store_true", help="Resume paused instance")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown running instance")
    args = parser.parse_args()
    
    if args.status:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print("[!] No state file found")
        return
    
    if args.pause or args.resume or args.shutdown:
        if PID_FILE.exists():
            with open(PID_FILE) as f:
                pid = int(f.read())
            
            sig = signal.SIGUSR1 if args.pause else (signal.SIGUSR2 if args.resume else signal.SIGTERM)
            try:
                os.kill(pid, sig)
                action = "paused" if args.pause else ("resumed" if args.resume else "shutdown")
                print(f"[+] Sent {action} signal to PID {pid}")
            except ProcessLookupError:
                print(f"[!] Process {pid} not found")
                PID_FILE.unlink()
        else:
            print("[!] PRAR not running")
        return
    
    # Start PRAR
    prar = PRAR()
    prar.run()

if __name__ == "__main__":
    main()
