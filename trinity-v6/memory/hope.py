"""
Trinity v6.0: Layer IV — HOPE Memory
Holographic Ordered Preference Engine
4 parallel SSMs with multi-timescale paradox retention.
"""
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class MemoryPacket:
    """Single memory packet in hexagonal ring structure."""
    state: np.ndarray
    timestamp: int
    coherence: float  # κ at time of storage
    ring_level: int   # 0=Immediate, 1=Extended, 2=Community, 3=Archive

class HOPERing:
    """
    Single HOPE ring at a specific timescale.
    
    Rings:
    - Immediate (Δt=1): Neighbor interactions, real-time
    - Extended (Δt=4): Next-nearest neighbors, short-term
    - Community (Δt=16): Cluster dynamics, medium-term  
    - Archive (Δt=64): Cold storage, long-term
    """
    
    def __init__(self, timescale: int, capacity: int = 100):
        self.timescale = timescale
        self.capacity = capacity
        self.packets: List[MemoryPacket] = []
        self.access_count = 0
    
    def write(self, state: np.ndarray, coherence: float) -> bool:
        """Write state to ring. Returns True if successful."""
        packet = MemoryPacket(
            state=state.copy(),
            timestamp=self.access_count,
            coherence=coherence,
            ring_level=self._get_ring_level()
        )
        
        self.packets.append(packet)
        
        # Evict oldest if over capacity
        if len(self.packets) > self.capacity:
            self.packets.pop(0)
        
        self.access_count += 1
        return True
    
    def read(self, query_state: np.ndarray, k: int = 5) -> List[MemoryPacket]:
        """
        Read k most relevant packets based on state similarity.
        Uses resonance (geometric coherence) as retrieval metric.
        """
        if not self.packets:
            return []
        
        # Compute resonance scores
        scores = []
        for packet in self.packets:
            # Geometric coherence: dot product of normalized states
            q_norm = query_state / (np.linalg.norm(query_state) + 1e-10)
            p_norm = packet.state / (np.linalg.norm(packet.state) + 1e-10)
            coherence = np.dot(q_norm, p_norm)
            scores.append((coherence, packet))
        
        # Sort by coherence, return top k
        scores.sort(reverse=True)
        return [packet for _, packet in scores[:k]]
    
    def _get_ring_level(self) -> int:
        """Map timescale to ring level."""
        mapping = {1: 0, 4: 1, 16: 2, 64: 3}
        return mapping.get(self.timescale, 0)
    
    def get_paradox_rate(self) -> float:
        """
        Measure paradox retention: % of contradictory state pairs.
        Two states are contradictory if their dot product is negative.
        """
        if len(self.packets) < 2:
            return 0.0
        
        contradictions = 0
        total_pairs = 0
        
        for i in range(len(self.packets)):
            for j in range(i + 1, len(self.packets)):
                p1 = self.packets[i].state / (np.linalg.norm(self.packets[i].state) + 1e-10)
                p2 = self.packets[j].state / (np.linalg.norm(self.packets[j].state) + 1e-10)
                
                if np.dot(p1, p2) < 0:
                    contradictions += 1
                total_pairs += 1
        
        return contradictions / total_pairs if total_pairs > 0 else 0.0

class HOPEMemory:
    """
    Holographic Ordered Preference Engine.
    
    4 parallel SSMs with linearly spaced discretization.
    Paradox retention target: 66%
    """
    
    TIMESCALES = [1, 4, 16, 64]
    PARADOX_TARGET = 0.66
    
    def __init__(self, state_dim: int = 16):
        self.state_dim = state_dim
        self.rings: Dict[int, HOPERing] = {
            dt: HOPERing(dt) for dt in self.TIMESCALES
        }
        self.cycle_count = 0
    
    def write(self, state: np.ndarray, coherence: float) -> None:
        """
        Write state to all rings.
        Each ring samples at its own timescale.
        """
        for dt, ring in self.rings.items():
            # Write if cycle aligns with timescale
            if self.cycle_count % dt == 0:
                ring.write(state, coherence)
        
        self.cycle_count += 1
    
    def read(self, query_state: np.ndarray, ring_level: int = None) -> List[MemoryPacket]:
        """
        Read from memory. If ring_level specified, only that ring.
        Otherwise, aggregate across all rings.
        """
        if ring_level is not None:
            timescale = self.TIMESCALES[ring_level]
            return self.rings[timescale].read(query_state)
        
        # Aggregate across all rings
        all_packets = []
        for ring in self.rings.values():
            all_packets.extend(ring.read(query_state))
        
        # Re-sort by coherence
        all_packets.sort(key=lambda p: p.coherence, reverse=True)
        return all_packets[:10]  # Return top 10 across all rings
    
    def measure_paradox_retention(self) -> Dict:
        """
        Measure paradox retention across all rings.
        Target: 66% contradictory state pairs survive.
        """
        results = {}
        total_contradictions = 0
        total_pairs = 0
        
        for dt, ring in self.rings.items():
            rate = ring.get_paradox_rate()
            results[f"ring_{dt}"] = rate
            
            # Weight by number of packets
            n = len(ring.packets)
            total_contradictions += rate * n
            total_pairs += n
        
        overall = total_contradictions / total_pairs if total_pairs > 0 else 0.0
        results['overall'] = overall
        results['target'] = self.PARADOX_TARGET
        results['status'] = 'PASS' if abs(overall - self.PARADOX_TARGET) < 0.1 else 'ADJUST'
        
        return results
    
    def get_superposition(self, state_a: np.ndarray, state_b: np.ndarray) -> np.ndarray:
        """
        Create superposition of two potentially contradictory states.
        Returns weighted combination preserving both.
        """
        # Normalize
        a_norm = state_a / (np.linalg.norm(state_a) + 1e-10)
        b_norm = state_b / (np.linalg.norm(state_b) + 1e-10)
        
        # Superposition: equal weight (Schrödinger-style)
        superposed = (a_norm + b_norm) / 2
        
        # Renormalize
        return superposed / (np.linalg.norm(superposed) + 1e-10)
    
    def status(self) -> dict:
        """Return memory system status."""
        return {
            'cycle_count': self.cycle_count,
            'ring_sizes': {dt: len(ring.packets) for dt, ring in self.rings.items()},
            'paradox_retention': self.measure_paradox_retention(),
            'total_packets': sum(len(ring.packets) for ring in self.rings.values())
        }

if __name__ == '__main__':
    print("=== HOPE MEMORY: Multi-Timescale Paradox Retention ===\n")
    
    # Initialize HOPE
    hope = HOPEMemory(state_dim=16)
    
    # Simulate 100 cycles with alternating contradictory states
    print("Simulating 100 cycles with paradoxical states...")
    
    state_a = np.random.randn(16)  # "Silence"
    state_b = -state_a * 0.8       # "Fire" (contradictory)
    
    for i in range(100):
        # Alternate between contradictory states
        state = state_a if i % 2 == 0 else state_b
        coherence = 0.8 + 0.1 * np.sin(i * 0.1)
        
        hope.write(state, coherence)
    
    # Measure paradox retention
    print("\nParadox Retention Measurement:")
    retention = hope.measure_paradox_retention()
    
    for ring, rate in retention.items():
        if ring not in ['overall', 'target', 'status']:
            print(f"  Ring {ring}: {rate:.1%} contradictory pairs")
    
    print(f"\n  Overall: {retention['overall']:.1%}")
    print(f"  Target:  {retention['target']:.1%}")
    print(f"  Status:  {retention['status']}")
    
    print("\nMemory Status:")
    status = hope.status()
    for dt, size in status['ring_sizes'].items():
        print(f"  Ring Δt={dt}: {size} packets")
    
    print(f"\nTotal packets: {status['total_packets']}")
    print("\n✓ HOPE Memory: Paradox treated as sacred, not error.")
