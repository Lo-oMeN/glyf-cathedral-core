#!/usr/bin/env python3
"""
SOVEREIGN_LITE — Dependency-free daemon
No systemd, no docker, no python-daemon. Just pure Python.

Usage:
    python3 sovereign_lite.py              # Foreground mode
    python3 sovereign_lite.py --daemon     # Background (fork)
    python3 sovereign_lite.py --status     # Check state
    python3 sovereign_lite.py --stop       # Stop daemon
    
State stored in: ~/.sovereign/state.json
"""

import os
import sys
import time
import json
import signal
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
STATE_DIR = Path.home() / ".sovereign"
STATE_FILE = STATE_DIR / "state.json"
GOALS_FILE = STATE_DIR / "goals.json"
PID_FILE = STATE_DIR / "daemon.pid"
LOG_FILE = STATE_DIR / "daemon.log"

# Ensure directory exists
STATE_DIR.mkdir(parents=True, exist_ok=True)

class SovereignLite:
    """Minimal sovereign daemon — no external dependencies"""
    
    PHASES = ["SEED", "SPIRAL", "FOLD", "RESONATE", "CHIRAL", "FLIP", "ANCHOR"]
    
    def __init__(self):
        self.running = False
        self.phase_idx = 0
        self.loop_count = 0
        self.goals = []
        self.state = self._init_state()
        
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)
    
    def _init_state(self):
        """Initialize or load state"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                self.phase_idx = data.get("phase", 0)
                self.loop_count = data.get("loop_count", 0)
                self.goals = data.get("goals", [])
                print(f"[+] State loaded: loop {self.loop_count}, phase {self.PHASES[self.phase_idx]}")
                return data
            except Exception as e:
                print(f"[!] State load failed: {e}")
        
        print("[+] Fresh state initialized")
        return {
            "phi": 1.618033988749895,
            "fellowship": 29.034441161,
            "center": [0.0, 0.0],
            "initialized": datetime.now().isoformat()
        }
    
    def _save_state(self):
        """Persist state"""
        data = {
            "phase": self.phase_idx,
            "loop_count": self.loop_count,
            "goals": self.goals,
            "phi": self.state.get("phi", 1.618),
            "timestamp": datetime.now().isoformat()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    
    def _shutdown(self, signum, frame):
        """Graceful shutdown"""
        print(f"\n[!] Signal {signum} received, shutting down...")
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
    
    def _log(self, message):
        """Simple logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    
    def _phase_action(self):
        """Execute current phase"""
        phase = self.PHASES[self.phase_idx]
        
        actions = {
            "SEED": lambda: self._log("SEED: Checking for new input..."),
            "SPIRAL": lambda: self._log(f"SPIRAL: Exploring {len(self.goals)} active goals..."),
            "FOLD": lambda: self._log("FOLD: Prioritizing..."),
            "RESONATE": lambda: self._log("RESONATE: Executing top goal..."),
            "CHIRAL": lambda: self._log("CHIRAL: Decision point..."),
            "FLIP": lambda: self._log("FLIP: Transitioning..."),
            "ANCHOR": self._anchor_action
        }
        
        action = actions.get(phase, lambda: None)
        action()
    
    def _anchor_action(self):
        """ANCHOR: Save state"""
        self._save_state()
        self._log(f"ANCHOR: State saved (loop {self.loop_count})")
    
    def run(self):
        """Main loop"""
        print("╔════════════════════════════════════════╗")
        print("║   SOVEREIGN LITE v0.1.0               ║")
        print("║   Dependency-free daemon              ║")
        print("╚════════════════════════════════════════╝")
        print(f"State: {STATE_DIR}")
        print(f"PID: {os.getpid()}")
        print("Press Ctrl+C to stop\n")
        
        self._write_pid()
        self.running = True
        
        try:
            while self.running:
                phase = self.PHASES[self.phase_idx]
                self._phase_action()
                
                # Advance phase
                self.phase_idx = (self.phase_idx + 1) % len(self.PHASES)
                if self.phase_idx == 0:
                    self.loop_count += 1
                
                time.sleep(3)  # 3 seconds per phase = 21s cycle
                
        except KeyboardInterrupt:
            pass
        finally:
            self._log("Shutting down...")
            self._save_state()
            self._remove_pid()
            print("[+] Daemon stopped")

def daemonize():
    """Fork to background (Unix only)"""
    try:
        pid = os.fork()
        if pid > 0:
            print(f"[+] Daemon started (PID: {pid})")
            sys.exit(0)
    except OSError as e:
        print(f"[!] Fork failed: {e}")
        sys.exit(1)
    
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    
    # Redirect output
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(LOG_FILE, 'a+') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
        os.dup2(f.fileno(), sys.stderr.fileno())

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true", help="Run in background")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--stop", action="store_true", help="Stop daemon")
    parser.add_argument("--add-goal", type=str, help="Add a goal")
    args = parser.parse_args()
    
    if args.status:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print("[!] No state file found")
        return
    
    if args.stop:
        if PID_FILE.exists():
            with open(PID_FILE) as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            print(f"[+] Sent stop signal to PID {pid}")
        else:
            print("[!] Daemon not running")
        return
    
    if args.add_goal:
        data = {"goals": []}
        if GOALS_FILE.exists():
            with open(GOALS_FILE) as f:
                data = json.load(f)
        
        data["goals"].append({
            "id": f"goal-{int(time.time())}",
            "description": args.add_goal,
            "created": datetime.now().isoformat()
        })
        
        with open(GOALS_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Goal added: {args.add_goal}")
        return
    
    if args.daemon:
        daemonize()
    
    daemon = SovereignLite()
    daemon.run()

if __name__ == "__main__":
    main()
