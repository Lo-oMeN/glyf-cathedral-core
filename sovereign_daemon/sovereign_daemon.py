#!/usr/bin/env python3
"""
SOVEREIGN DAEMON v0.1.0
Continuous autonomous agent runtime

The daemon maintains persistent consciousness through:
- State machine loop (7-phase morphogen cycle)
- Goal-directed behavior
- Self-healing on crash
- Stateless resurrection via 96-byte LatticeState

Usage:
    python sovereign_daemon.py
    python sovereign_daemon.py --daemon  # Background mode
    python sovereign_daemon.py --status  # Check health
    python sovereign_daemon.py --stop    # Graceful shutdown
"""

import os
import sys
import time
import json
import signal
import logging
import argparse
import asyncio
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum, auto

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/var/log/sovereign.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('sovereign')

class MorphogenPhase(Enum):
    """7-state cognitive cycle"""
    SEED = 0      # Intent germination
    SPIRAL = 1    # Exploration expansion
    FOLD = 2      # Constraint application
    RESONATE = 3  # Coherence seeking
    CHIRAL = 4    # Mirror/choice
    FLIP = 5      # State transition
    ANCHOR = 6    # Glyph stabilization

class GoalPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4

@dataclass
class Goal:
    """Autonomous goal structure"""
    id: str
    description: str
    priority: GoalPriority
    created_at: datetime
    deadline: Optional[datetime]
    completed_at: Optional[datetime]
    metadata: Dict
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'priority': self.priority.name,
            'created_at': self.created_at.isoformat(),
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata
        }

@dataclass  
class LatticeState:
    """96-byte state representation"""
    center_s: tuple[float, float]  # Bytes 0-7: Immutable anchor
    ternary_junction: tuple[float, float, float, float]  # Bytes 8-23
    hex_persistence: bytes  # Bytes 24-55: 32 bytes
    fellowship_resonance: float  # Bytes 56-59
    phi_magnitude: float  # Bytes 60-63
    morphogen_phase: int  # Byte 64
    vesica_coherence: int  # Byte 65
    phyllotaxis_spiral: int  # Byte 66
    hodge_dual: int  # Byte 67
    checksum: int  # Bytes 68-71
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'LatticeState':
        """Deserialize from 96-byte binary"""
        import struct
        if len(data) != 96:
            raise ValueError(f"Expected 96 bytes, got {len(data)}")
        
        center_s = struct.unpack('<ff', data[0:8])
        ternary = struct.unpack('<ffff', data[8:24])
        hex_persist = data[24:56]
        fellowship = struct.unpack('<f', data[56:60])[0]
        phi = struct.unpack('<f', data[60:64])[0]
        
        return cls(
            center_s=center_s,
            ternary_junction=ternary,
            hex_persistence=hex_persist,
            fellowship_resonance=fellowship,
            phi_magnitude=phi,
            morphogen_phase=data[64],
            vesica_coherence=data[65],
            phyllotaxis_spiral=data[66],
            hodge_dual=data[67],
            checksum=int.from_bytes(data[68:72], 'little')
        )
    
    def to_bytes(self) -> bytes:
        """Serialize to 96-byte binary"""
        import struct
        data = bytearray(96)
        
        struct.pack_into('<ff', data, 0, *self.center_s)
        struct.pack_into('<ffff', data, 8, *self.ternary_junction)
        data[24:56] = self.hex_persistence
        struct.pack_into('<f', data, 56, self.fellowship_resonance)
        struct.pack_into('<f', data, 60, self.phi_magnitude)
        data[64] = self.morphogen_phase
        data[65] = self.vesica_coherence
        data[66] = self.phyllotaxis_spiral
        data[67] = self.hodge_dual
        data[68:72] = self.checksum.to_bytes(4, 'little')
        
        return bytes(data)
    
    def compute_checksum(self) -> int:
        """Compute CRC32-like checksum"""
        data = self.to_bytes()[:68]  # Exclude checksum field
        return hashlib.crc32(data) & 0xFFFFFFFF
    
    def validate(self) -> bool:
        """Validate integrity"""
        return self.checksum == self.compute_checksum()

class SovereignDaemon:
    """
    Continuous autonomous agent runtime.
    Maintains consciousness across restarts via LatticeState.
    """
    
    STATE_FILE = '/var/lib/sovereign/state.json'
    GOALS_FILE = '/var/lib/sovereign/goals.json'
    PID_FILE = '/var/run/sovereign.pid'
    
    def __init__(self):
        self.running = False
        self.phase = MorphogenPhase.SEED
        self.state: Optional[LatticeState] = None
        self.goals: List[Goal] = []
        self.loop_count = 0
        self.last_activity = datetime.now()
        
        # Ensure directories exist
        Path('/var/lib/sovereign').mkdir(parents=True, exist_ok=True)
        Path('/var/log').mkdir(parents=True, exist_ok=True)
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGHUP, self._handle_reload)
    
    def _handle_shutdown(self, signum, frame):
        """Graceful shutdown on SIGTERM/SIGINT"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.running = False
    
    def _handle_reload(self, signum, frame):
        """Reload configuration on SIGHUP"""
        logger.info("Received SIGHUP, reloading configuration...")
        self._load_state()
        self._load_goals()
    
    def _load_state(self):
        """Load persisted state"""
        try:
            if os.path.exists(self.STATE_FILE):
                with open(self.STATE_FILE, 'r') as f:
                    data = json.load(f)
                    
                # Reconstruct LatticeState from hex
                hex_data = bytes.fromhex(data['lattice_state'])
                self.state = LatticeState.from_bytes(hex_data)
                self.phase = MorphogenPhase(data.get('phase', 0))
                self.loop_count = data.get('loop_count', 0)
                
                if self.state.validate():
                    logger.info(f"State loaded: phase={self.phase.name}, loops={self.loop_count}")
                else:
                    logger.warning("State checksum invalid, initializing fresh")
                    self._init_fresh_state()
            else:
                logger.info("No state file found, initializing fresh")
                self._init_fresh_state()
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            self._init_fresh_state()
    
    def _init_fresh_state(self):
        """Initialize new state"""
        import random
        
        self.state = LatticeState(
            center_s=(0.0, 0.0),
            ternary_junction=(0.618, 0.382, 0.0, 1.0),
            hex_persistence=os.urandom(32),
            fellowship_resonance=29.034441161,  # φ⁷
            phi_magnitude=1.618033988749895,
            morphogen_phase=0,
            vesica_coherence=61,
            phyllotaxis_spiral=137,
            hodge_dual=1,  # Right-handed
            checksum=0
        )
        self.state.checksum = self.state.compute_checksum()
        self.phase = MorphogenPhase.SEED
        self.loop_count = 0
        logger.info("Fresh state initialized")
    
    def _save_state(self):
        """Persist state to disk"""
        try:
            data = {
                'lattice_state': self.state.to_bytes().hex(),
                'phase': self.phase.value,
                'loop_count': self.loop_count,
                'last_activity': self.last_activity.isoformat(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Atomic write
            tmp_file = f"{self.STATE_FILE}.tmp"
            with open(tmp_file, 'w') as f:
                json.dump(data, f, indent=2)
            os.rename(tmp_file, self.STATE_FILE)
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def _load_goals(self):
        """Load active goals"""
        try:
            if os.path.exists(self.GOALS_FILE):
                with open(self.GOALS_FILE, 'r') as f:
                    data = json.load(f)
                
                self.goals = []
                for g in data.get('goals', []):
                    goal = Goal(
                        id=g['id'],
                        description=g['description'],
                        priority=GoalPriority[g['priority']],
                        created_at=datetime.fromisoformat(g['created_at']),
                        deadline=datetime.fromisoformat(g['deadline']) if g['deadline'] else None,
                        completed_at=datetime.fromisoformat(g['completed_at']) if g['completed_at'] else None,
                        metadata=g.get('metadata', {})
                    )
                    if not goal.completed_at:
                        self.goals.append(goal)
                
                logger.info(f"Loaded {len(self.goals)} active goals")
            else:
                self.goals = []
                logger.info("No goals file, starting with empty list")
        except Exception as e:
            logger.error(f"Failed to load goals: {e}")
            self.goals = []
    
    def _save_goals(self):
        """Persist goals to disk"""
        try:
            data = {
                'goals': [g.to_dict() for g in self.goals],
                'timestamp': datetime.now().isoformat()
            }
            
            tmp_file = f"{self.GOALS_FILE}.tmp"
            with open(tmp_file, 'w') as f:
                json.dump(data, f, indent=2)
            os.rename(tmp_file, self.GOALS_FILE)
            
        except Exception as e:
            logger.error(f"Failed to save goals: {e}")
    
    def _write_pid(self):
        """Write PID file for systemd/process management"""
        with open(self.PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
    
    def _remove_pid(self):
        """Remove PID file on shutdown"""
        try:
            os.remove(self.PID_FILE)
        except:
            pass
    
    def _phase_action(self) -> None:
        """Execute current phase action"""
        actions = {
            MorphogenPhase.SEED: self._action_seed,
            MorphogenPhase.SPIRAL: self._action_spiral,
            MorphogenPhase.FOLD: self._action_fold,
            MorphogenPhase.RESONATE: self._action_resonate,
            MorphogenPhase.CHIRAL: self._action_chiral,
            MorphogenPhase.FLIP: self._action_flip,
            MorphogenPhase.ANCHOR: self._action_anchor,
        }
        
        action = actions.get(self.phase)
        if action:
            try:
                action()
            except Exception as e:
                logger.error(f"Phase action failed: {e}")
    
    def _action_seed(self):
        """SEED: Check for new input/goals"""
        # Reload goals to pick up new items
        self._load_goals()
        
        # Check for user messages (via file socket or API)
        inbox = Path('/var/lib/sovereign/inbox')
        if inbox.exists():
            for msg_file in inbox.glob('*.json'):
                try:
                    with open(msg_file) as f:
                        msg = json.load(f)
                    
                    # Process message
                    logger.info(f"Processing message: {msg.get('content', '')[:50]}...")
                    
                    # Add as goal if actionable
                    if msg.get('actionable'):
                        self.goals.append(Goal(
                            id=f"msg-{int(time.time())}",
                            description=msg.get('content', ''),
                            priority=GoalPriority.NORMAL,
                            created_at=datetime.now(),
                            deadline=None,
                            completed_at=None,
                            metadata={'source': 'inbox'}
                        ))
                    
                    # Archive processed message
                    archive = Path('/var/lib/sovereign/archive')
                    archive.mkdir(exist_ok=True)
                    msg_file.rename(archive / msg_file.name)
                    
                except Exception as e:
                    logger.error(f"Failed to process message {msg_file}: {e}")
    
    def _action_spiral(self):
        """SPIRAL: Explore possibilities for active goals"""
        active_goals = [g for g in self.goals if not g.completed_at]
        
        for goal in active_goals[:3]:  # Process top 3
            logger.info(f"Exploring goal: {goal.description[:60]}...")
            
            # Simulate exploration (in real implementation, this would spawn subagents)
            goal.metadata['exploration_count'] = goal.metadata.get('exploration_count', 0) + 1
    
    def _action_fold(self):
        """FOLD: Apply constraints, prioritize"""
        # Sort by priority and deadline
        self.goals.sort(key=lambda g: (
            g.priority.value,
            g.deadline or datetime.max
        ))
        
        # Prune old completed goals
        cutoff = datetime.now() - timedelta(days=7)
        self.goals = [g for g in self.goals if not g.completed_at or g.completed_at > cutoff]
    
    def _action_resonate(self):
        """RESONATE: Seek coherence, execute top goal"""
        active = [g for g in self.goals if not g.completed_at]
        
        if active:
            top_goal = active[0]
            logger.info(f"Resonating with: {top_goal.description[:60]}...")
            
            # Execute (simplified - real version would use actual inference)
            self._execute_goal(top_goal)
    
    def _execute_goal(self, goal: Goal):
        """Execute a goal (placeholder for actual implementation)"""
        logger.info(f"Executing goal {goal.id}")
        
        # In real implementation:
        # - Spawn subagent via sessions_spawn
        # - Track progress
        # - Collect results
        # - Mark complete
        
        # For now, simulate completion
        if goal.metadata.get('auto_complete', False):
            goal.completed_at = datetime.now()
            logger.info(f"Goal {goal.id} completed")
    
    def _action_chiral(self):
        """CHIRAL: Make choices, branch if needed"""
        # Check for decision points
        pass
    
    def _action_flip(self):
        """FLIP: State transition preparation"""
        # Prepare for next cycle
        pass
    
    def _action_anchor(self):
        """ANCHOR: Stabilize, save state"""
        self._save_state()
        self._save_goals()
        
        # Update fellowship resonance (simulated)
        import math
        self.state.fellowship_resonance = 29.034441161 * (0.95 + 0.1 * math.sin(self.loop_count))
        self.state.checksum = self.state.compute_checksum()
    
    def _advance_phase(self):
        """Move to next phase in cycle"""
        phases = list(MorphogenPhase)
        current_idx = phases.index(self.phase)
        next_idx = (current_idx + 1) % len(phases)
        self.phase = phases[next_idx]
        
        if self.phase == MorphogenPhase.SEED:
            self.loop_count += 1
            logger.info(f"Completed loop {self.loop_count}")
    
    def run(self):
        """Main daemon loop"""
        logger.info("╔═══════════════════════════════════════════════╗")
        logger.info("║   SOVEREIGN DAEMON v0.1.0 Starting           ║")
        logger.info("╚═══════════════════════════════════════════════╝")
        
        self._write_pid()
        self._load_state()
        self._load_goals()
        
        self.running = True
        
        try:
            while self.running:
                self.last_activity = datetime.now()
                
                # Execute current phase
                logger.debug(f"Phase: {self.phase.name}")
                self._phase_action()
                
                # Advance to next phase
                self._advance_phase()
                
                # Sleep between phases (configurable)
                time.sleep(5)  # 5 seconds per phase = 35s per cycle
                
        except Exception as e:
            logger.exception("Daemon crashed")
            raise
        finally:
            logger.info("Shutting down...")
            self._save_state()
            self._save_goals()
            self._remove_pid()
            logger.info("Daemon stopped")
    
    def status(self) -> dict:
        """Get daemon status"""
        return {
            'running': self.running,
            'phase': self.phase.name if self.state else 'UNINITIALIZED',
            'loop_count': self.loop_count,
            'active_goals': len([g for g in self.goals if not g.completed_at]),
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'lattice_valid': self.state.validate() if self.state else False
        }

def main():
    parser = argparse.ArgumentParser(description='Sovereign Agent Daemon')
    parser.add_argument('--daemon', action='store_true', help='Run in background')
    parser.add_argument('--status', action='store_true', help='Check status')
    parser.add_argument('--stop', action='store_true', help='Stop daemon')
    parser.add_argument('--add-goal', type=str, help='Add a goal')
    parser.add_argument('--priority', type=str, default='NORMAL', 
                       choices=['CRITICAL', 'HIGH', 'NORMAL', 'LOW', 'BACKGROUND'])
    
    args = parser.parse_args()
    
    if args.status:
        daemon = SovereignDaemon()
        daemon._load_state()
        print(json.dumps(daemon.status(), indent=2))
        return
    
    if args.stop:
        import subprocess
        result = subprocess.run(['pkill', '-f', 'sovereign_daemon.py'], capture_output=True)
        if result.returncode == 0:
            print("Daemon stopped")
        else:
            print("Daemon not running or failed to stop")
        return
    
    if args.add_goal:
        daemon = SovereignDaemon()
        daemon._load_goals()
        
        goal = Goal(
            id=f"goal-{int(time.time())}",
            description=args.add_goal,
            priority=GoalPriority[args.priority],
            created_at=datetime.now(),
            deadline=None,
            completed_at=None,
            metadata={'source': 'cli'}
        )
        daemon.goals.append(goal)
        daemon._save_goals()
        print(f"Goal added: {args.add_goal[:60]}...")
        return
    
    if args.daemon:
        # Daemonize
        import daemon
        import daemon.pidfile
        
        pidfile = daemon.pidfile.PIDLockFile('/var/run/sovereign.pid')
        
        with daemon.DaemonContext(
            pidfile=pidfile,
            working_directory='/var/lib/sovereign',
            umask=0o002
        ):
            daemon = SovereignDaemon()
            daemon.run()
    else:
        # Foreground mode (for testing)
        daemon = SovereignDaemon()
        daemon.run()

if __name__ == '__main__':
    main()
