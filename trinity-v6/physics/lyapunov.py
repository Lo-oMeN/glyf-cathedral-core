"""
Trinity v6.0: Lyapunov Stability Engine
Ensures geometric invariants hold under perturbation.
"""
import numpy as np
from typing import Tuple, Optional

def lyapunov_stability_check(
    state: np.ndarray, 
    P: Optional[np.ndarray] = None
) -> Tuple[bool, float]:
    """
    Check stability via Lyapunov function V = state^T @ P @ state.
    
    Returns:
        (is_stable, V) where is_stable = V_perturbed < V
    """
    if P is None:
        P = np.eye(len(state))
    
    # Current energy
    V = float(state.T @ P @ state)
    
    # Perturbed energy (random δ)
    delta = np.random.normal(0, 0.01, state.shape)
    V_pert = float((state + delta).T @ P @ (state + delta))
    
    # Stable if perturbation decreases energy
    is_stable = V_pert < V
    
    return is_stable, V

def lyapunov_drift_metric(
    trajectory: list[np.ndarray],
    P: Optional[np.ndarray] = None
) -> dict:
    """
    Measure drift over a trajectory.
    Returns dict with max drift, mean energy, stability ratio.
    """
    if not trajectory:
        return {'error': 'empty trajectory'}
    
    if P is None:
        P = np.eye(len(trajectory[0]))
    
    energies = []
    stabilities = []
    
    for state in trajectory:
        is_stable, V = lyapunov_stability_check(state, P)
        energies.append(V)
        stabilities.append(is_stable)
    
    return {
        'max_drift': max(energies) - min(energies),
        'mean_energy': np.mean(energies),
        'stability_ratio': sum(stabilities) / len(stabilities),
        'initial_energy': energies[0],
        'final_energy': energies[-1],
        'is_converging': energies[-1] < energies[0]
    }
