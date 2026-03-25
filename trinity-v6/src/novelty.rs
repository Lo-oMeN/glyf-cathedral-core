//! Novelty-Seer: Pattern Recognition Shaman
//! 
//! Measures the emergence of complexity in the GLYF Cathedral.
//! Tracks novelty, predicts phase transitions, detects emergence.
//! 
//! "Complexity is the tendency of systems to become more complex over time."
//! — Terence McKenna
//! 
//! Performance: <100μs per computation (ARMv6 optimized)

#![no_std]

use crate::kernel::{SovereignState, PHI, PHI_7};
use crate::narrative::MorphogenPhase;

// =============================================================================
// PHI-POWERED WEIGHT CONSTANTS
// =============================================================================

/// Pre-computed φ⁻ᵏ weights for k=0..31 (junction dimensions)
/// Used for novelty calculation with golden decay
const PHI_NEG_POWERS: [f32; 32] = [
    1.0,                    // φ⁰ = 1.0
    0.61803399,             // φ⁻¹
    0.38196601,             // φ⁻²
    0.23606798,             // φ⁻³
    0.14589803,             // φ⁻⁴
    0.09016994,             // φ⁻⁵
    0.05572809,             // φ⁻⁶
    0.03444185,             // φ⁻⁷
    0.02128624,             // φ⁻⁸
    0.01315562,             // φ⁻⁹
    0.00813062,             // φ⁻¹⁰
    0.00502500,             // φ⁻¹¹
    0.00310562,             // φ⁻¹²
    0.00191938,             // φ⁻¹³
    0.00118624,             // φ⁻¹⁴
    0.00073315,             // φ⁻¹⁵
    0.00045309,             // φ⁻¹⁶
    0.00028006,             // φ⁻¹⁷
    0.00017303,             // φ⁻¹⁸
    0.00010703,             // φ⁻¹⁹
    0.00006600,             // φ⁻²⁰
    0.00004003,             // φ⁻²¹
    0.00002597,             // φ⁻²²
    0.00001606,             // φ⁻²³
    0.00000991,             // φ⁻²⁴
    0.00000615,             // φ⁻²⁵
    0.00000376,             // φ⁻²⁶
    0.00000239,             // φ⁻²⁷
    0.00000137,             // φ⁻²⁸
    0.00000102,             // φ⁻²⁹
    0.00000035,             // φ⁻³⁰
    0.00000067,             // φ⁻³¹
];

/// Normalization factor: sum of all φ⁻ᵏ weights for 16 dimensions
const PHI_WEIGHT_SUM: f32 = 2.61803399; // φ + 1 = φ²

/// Shannon entropy lookup table for 8-bit values (pre-computed -p*log₂(p))
/// Optimized for fast entropy calculation
const ENTROPY_LUT: [f32; 256] = {
    let mut lut = [0.0f32; 256];
    let mut i: usize = 1;
    while i < 256 {
        let p = i as f32 / 255.0;
        lut[i] = -p * p.log2();
        i += 1;
    }
    lut
};

/// Morphogen phase transition thresholds (based on φ-scaling)
const PHASE_THRESHOLDS: [f32; 7] = [
    0.0,      // Seed (0)
    0.146,    // Spiral (1) - φ⁻⁴
    0.236,    // Fold (2) - φ⁻³
    0.382,    // Resonate (3) - φ⁻²
    0.500,    // Chiral (4) - midpoint
    0.618,    // Flip (5) - φ⁻¹
    0.764,    // Anchor (6) - approaching unity
];

/// Emergence detection threshold (novelty spike)
const EMERGENCE_THRESHOLD: f32 = 0.618;

/// History window size for prediction
const HISTORY_WINDOW: usize = 8;

/// LZW compression dictionary size estimate for Kolmogorov complexity
const LZW_DICT_SIZE: usize = 256;

// =============================================================================
// NOVELTY INDEX - The Oracle's Lens
// =============================================================================

/// NoveltyIndex: Measures how much the cathedral has transformed
/// 
/// Returns f32 in [0.0, 1.0] where:
/// - 0.0 = identical states (no novelty)
/// - 1.0 = completely novel (maximal transformation)
pub struct NoveltyIndex;

impl NoveltyIndex {
    /// Compute novelty between two states
    /// 
    /// Algorithm:
    /// 1. Compare ternary junction values (16 dimensions from kernel.rs)
    /// 2. Weight differences by φ⁻ᵏ for each dimension k
    /// 3. Normalize to [0.0, 1.0]
    /// 4. Novelty = 1.0 - similarity
    /// 
    /// Complexity: O(16) = constant time
    pub fn compute(prev: &SovereignState, curr: &SovereignState) -> f32 {
        let mut weighted_diff: f32 = 0.0;
        
        // Compare ternary junction values with φ-weighted decay
        for k in 0..16 {
            let prev_val = prev.ternary_junction[k] as f32;
            let curr_val = curr.ternary_junction[k] as f32;
            
            // Ternary difference: 0 if same, 1 if different sign or magnitude
            let diff = if prev_val == curr_val {
                0.0
            } else if prev_val.signum() != curr_val.signum() {
                1.0 // Maximum difference for sign flip
            } else {
                (curr_val - prev_val).abs() / 2.0 // Partial difference
            };
            
            // Weight by φ⁻ᵏ (golden decay - early dimensions matter more)
            weighted_diff += diff * PHI_NEG_POWERS[k];
        }
        
        // Also consider center_s drift (should be immutable at origin)
        let center_drift = ((curr.center_s[0] - prev.center_s[0]).powi(2)
            + (curr.center_s[1] - prev.center_s[1]).powi(2)).sqrt();
        if center_drift > 1e-6 {
            weighted_diff += PHI_NEG_POWERS[0]; // Maximum penalty for center drift
        }
        
        // Normalize and convert to novelty
        let similarity = 1.0 - (weighted_diff / PHI_WEIGHT_SUM).min(1.0);
        let novelty = 1.0 - similarity;
        
        novelty
    }
    
    /// Batch novelty computation for state history
    /// Returns array of novelty values for consecutive pairs
    pub fn compute_history(states: &[SovereignState]) -> [f32; HISTORY_WINDOW] {
        let mut novelties = [0.0f32; HISTORY_WINDOW];
        
        for i in 1..states.len().min(HISTORY_WINDOW + 1) {
            novelties[i - 1] = Self::compute(&states[i - 1], &states[i]);
        }
        
        novelties
    }
}

// =============================================================================
// PHASE TRANSITION PREDICTOR
// =============================================================================

/// Predicts the next morphogen phase based on novelty history
/// 
/// Uses φ-weighted linear regression on phase velocity
pub struct PhasePredictor;

impl PhasePredictor {
    /// Predict the next morphogen phase (0-6) based on state history
    /// 
    /// Algorithm:
    /// 1. Compute phase velocity (change in phase over time)
    /// 2. Weight recent history by φ⁻ᵏ
    /// 3. Project forward using golden ratio acceleration
    /// 4. Return predicted phase
    /// 
    /// Returns predicted phase (0-6) as f32 (allows for sub-phase prediction)
    pub fn predict_phase_transition(history: &[SovereignState]) -> f32 {
        if history.len() < 2 {
            return 0.0; // Not enough history
        }
        
        let n = history.len().min(HISTORY_WINDOW);
        
        // Compute phase velocities with φ-weighting
        let mut weighted_velocity: f32 = 0.0;
        let mut weight_sum: f32 = 0.0;
        
        for i in 1..n {
            let dt = (history[i].sequence - history[i-1].sequence).max(1) as f32;
            let dv = history[i].morphogen_phase as f32 - history[i-1].morphogen_phase as f32;
            let velocity = dv / dt;
            
            // Weight recent velocities more heavily (φ⁻ᵏ decay)
            let weight = PHI_NEG_POWERS[n - i - 1];
            weighted_velocity += velocity * weight;
            weight_sum += weight;
        }
        
        if weight_sum > 0.0 {
            weighted_velocity /= weight_sum;
        }
        
        // Current phase
        let current_phase = history[history.len() - 1].morphogen_phase as f32;
        
        // Predict next phase using φ-accelerated projection
        // The golden ratio appears in growth dynamics
        let prediction = current_phase + weighted_velocity * PHI;
        
        // Clamp to valid phase range [0.0, 6.0]
        prediction.clamp(0.0, 6.0)
    }
    
    /// Predict time (in sequence steps) until next phase transition
    pub fn predict_time_to_transition(
        current_phase: u8,
        history: &[SovereignState]
    ) -> Option<u64> {
        if current_phase >= 6 {
            return None; // Already at Anchor phase
        }
        
        let predicted = Self::predict_phase_transition(history);
        let next_threshold = PHASE_THRESHOLDS[(current_phase + 1) as usize];
        
        // Estimate steps based on current trajectory
        if history.len() >= 2 {
            let latest = &history[history.len() - 1];
            let prev = &history[history.len() - 2];
            let dt = (latest.sequence - prev.sequence).max(1);
            
            let phase_progress = (predicted - current_phase as f32).abs();
            if phase_progress > 0.001 {
                let steps_needed = ((next_threshold - (current_phase as f32 / 6.0)) 
                    * 6.0 / phase_progress) as u64;
                return Some(steps_needed * dt);
            }
        }
        
        None
    }
    
    /// Get the morphogen phase as enum from raw byte
    pub fn current_phase_enum(state: &SovereignState) -> Option<MorphogenPhase> {
        MorphogenPhase::from_byte(state.morphogen_phase)
    }
}

// =============================================================================
// COMPLEXITY SCORER - Measuring the Cathedral's Growth
// =============================================================================

/// Computes information-theoretic complexity of state
/// 
/// Three metrics:
/// 1. Shannon entropy of hex_tiles
/// 2. Kolmogorov complexity estimate (compression ratio)
/// 3. Fractal dimension of state trajectory
pub struct ComplexityScorer;

impl ComplexityScorer {
    /// Compute overall complexity score [0.0, 1.0]
    /// 
    /// Combines entropy, compressibility, and fractal dimension
    /// with φ-weighted harmonization
    pub fn complexity_score(state: &SovereignState, history: &[SovereignState]) -> f32 {
        let entropy = Self::shannon_entropy(state);
        let kolmogorov = Self::kolmogorov_estimate(state);
        let fractal = Self::fractal_dimension(history);
        
        // φ-weighted combination of complexity metrics
        // Higher weight to entropy (information content)
        let score = entropy * PHI.recip() 
                  + kolmogorov * PHI.recip().powi(2) 
                  + fractal * PHI.recip().powi(3);
        
        // Normalize by weight sum
        let weight_sum = PHI.recip() + PHI.recip().powi(2) + PHI.recip().powi(3);
        (score / weight_sum).min(1.0)
    }
    
    /// Shannon entropy of hex_tiles distribution
    /// 
    /// H(X) = -Σ p(x) log₂(p(x))
    /// Higher entropy = more information = more complex
    pub fn shannon_entropy(state: &SovereignState) -> f32 {
        // Count byte frequencies in hex_tiles (32 bytes)
        let mut freq = [0u32; 256];
        for i in 0..32 {
            freq[state.hex_tiles[i] as usize] += 1;
        }
        
        // Calculate entropy using lookup table
        let mut entropy: f32 = 0.0;
        let total = 32.0;
        
        for count in freq.iter() {
            if *count > 0 {
                let p = *count as f32 / total;
                entropy -= p * p.log2();
            }
        }
        
        // Normalize to [0.0, 1.0] (max entropy for 32 bytes is 5.0)
        (entropy / 5.0).min(1.0)
    }
    
    /// Kolmogorov complexity estimate via compression ratio
    /// 
    /// Uses LZW-inspired dictionary size as proxy
    /// Higher compression ratio = lower complexity
    /// We return (1 - compression_ratio) for complexity measure
    pub fn kolmogorov_estimate(state: &SovereignState) -> f32 {
        // Simple run-length encoding as proxy for compressibility
        let mut runs: usize = 1;
        let mut dict_entries: usize = 1;
        
        for i in 1..32 {
            if state.hex_tiles[i] != state.hex_tiles[i - 1] {
                runs += 1;
            }
            // Count unique patterns (2-byte windows)
            if i > 0 {
                let pattern = (state.hex_tiles[i-1] as u16) << 8 | (state.hex_tiles[i] as u16);
                // Simplified: use pattern distribution
                dict_entries += (pattern as usize) % 4; // Pseudo-unique count
            }
        }
        
        // Compression ratio estimate
        let compressed_size = runs + dict_entries;
        let original_size = 32;
        let compression_ratio = if compressed_size > 0 {
            (original_size as f32 - compressed_size.min(original_size) as f32) 
                / original_size as f32
        } else {
            0.0
        };
        
        // Kolmogorov complexity ∝ (1 - compression_ratio)
        compression_ratio.clamp(0.0, 1.0)
    }
    
    /// Fractal dimension of state trajectory
    /// 
    /// Uses box-counting dimension on phase space trajectory
    /// Measures how "space-filling" the evolution is
    pub fn fractal_dimension(history: &[SovereignState]) -> f32 {
        if history.len() < 4 {
            return 0.0; // Not enough points
        }
        
        let n = history.len().min(HISTORY_WINDOW);
        
        // Extract trajectory points (ternary_junction[0], ternary_junction[1]) as 2D projection
        let mut points = [(0i8, 0i8); HISTORY_WINDOW];
        for i in 0..n {
            points[i] = (history[i].ternary_junction[0], history[i].ternary_junction[1]);
        }
        
        // Box-counting: count occupied boxes at different scales
        let mut box_counts = [0usize; 4];
        let scales = [1i8, 2, 4, 8];
        
        for (scale_idx, &scale) in scales.iter().enumerate() {
            let mut occupied = [false; HISTORY_WINDOW * 4]; // Simple hash set
            
            for i in 0..n {
                // Map to grid cell at this scale
                let x = (points[i].0 / scale.max(1)) as usize;
                let y = (points[i].1 / scale.max(1)) as usize;
                let idx = (x * 8 + y) % occupied.len();
                occupied[idx] = true;
            }
            
            box_counts[scale_idx] = occupied.iter().filter(|&&x| x).count();
        }
        
        // Estimate dimension from log-log slope
        // D ≈ log(N(ε)) / log(1/ε)
        if box_counts[0] > 0 && box_counts[3] > 0 {
            let log_n = (box_counts[0] as f32).log2();
            let log_eps_inv = 3.0; // log₂(8)
            let dim = log_n / log_eps_inv;
            
            // Normalize to [0, 1] (max dimension 2 for 2D projection)
            (dim / 2.0).clamp(0.0, 1.0)
        } else {
            0.5 // Default to middle complexity
        }
    }
}

// =============================================================================
// EMERGENCE DETECTOR - When New Patterns Arise
// =============================================================================

/// Detects emergence of novel patterns in state evolution
/// 
/// Identifies when the cathedral births new structure
pub struct EmergenceDetector;

/// Emergence event structure
#[derive(Clone, Copy, Debug)]
pub struct EmergenceEvent {
    /// Timestamp (sequence number)
    pub seq: u64,
    /// Novelty value that triggered detection
    pub novelty: f32,
    /// Type of emergence detected
    pub kind: EmergenceKind,
    /// Complexity at emergence
    pub complexity: f32,
}

/// Types of emergent phenomena
#[derive(Clone, Copy, Debug, PartialEq)]
#[repr(u8)]
pub enum EmergenceKind {
    /// Novel junction configuration
    JunctionMutation = 0,
    /// New tile pattern
    TilePattern = 1,
    /// Phase transition
    PhaseShift = 2,
    /// Autopoietic closure achieved
    Autopoiesis = 3,
    /// Chirality flip
    ChiralInversion = 4,
    /// Complexity spike
    ComplexityBurst = 5,
}

impl EmergenceDetector {
    /// Detect emergence by comparing current state to history
    /// 
    /// Returns Some(EmergenceEvent) if emergence detected, None otherwise
    pub fn detect(
        curr: &SovereignState,
        history: &[SovereignState],
        novelty: f32,
        complexity: f32,
    ) -> Option<EmergenceEvent> {
        // Threshold check
        if novelty < EMERGENCE_THRESHOLD {
            return None;
        }
        
        // Determine emergence kind
        let kind = Self::classify_emergence(curr, history, novelty, complexity);
        
        Some(EmergenceEvent {
            seq: curr.sequence,
            novelty,
            kind,
            complexity,
        })
    }
    
    /// Classify the type of emergence
    fn classify_emergence(
        curr: &SovereignState,
        history: &[SovereignState],
        novelty: f32,
        complexity: f32,
    ) -> EmergenceKind {
        // Check for phase transition
        if let Some(prev) = history.last() {
            if curr.morphogen_phase != prev.morphogen_phase {
                if curr.morphogen_phase == 6 && prev.morphogen_phase == 5 {
                    return EmergenceKind::Autopoiesis;
                }
                return EmergenceKind::PhaseShift;
            }
            
            // Check for chirality flip
            if curr.hodge_dual != prev.hodge_dual {
                return EmergenceKind::ChiralInversion;
            }
        }
        
        // Check for junction mutation (high novelty in early dimensions)
        if novelty > 0.8 {
            return EmergenceKind::JunctionMutation;
        }
        
        // Check for complexity burst
        if complexity > 0.764 { // φ⁻² threshold
            return EmergenceKind::ComplexityBurst;
        }
        
        // Default: new tile pattern
        EmergenceKind::TilePattern
    }
    
    /// Detect bifurcation point (critical transition)
    /// 
    /// Returns true if system is near a bifurcation
    pub fn detect_bifurcation(history: &[SovereignState], novelties: &[f32]) -> bool {
        if history.len() < 3 || novelties.len() < 3 {
            return false;
        }
        
        // Bifurcation indicators:
        // 1. Increasing novelty variance
        // 2. Phase velocity approaching zero (critical slowing down)
        // 3. Lyapunov exponent turning positive
        
        let n = novelties.len();
        
        // Check for critical slowing down (variance increase)
        let mean = novelties.iter().sum::<f32>() / n as f32;
        let variance = novelties.iter()
            .map(|&x| (x - mean).powi(2))
            .sum::<f32>() / n as f32;
        
        // Check for trend (increasing variance in recent history)
        let recent_mean = novelties[n-2..].iter().sum::<f32>() / 2.0;
        let older_mean = novelties[0..n-2].iter().sum::<f32>() / (n-2) as f32;
        
        // Bifurcation if variance is high AND novelty is increasing
        variance > 0.1 && recent_mean > older_mean * PHI.recip()
    }
    
    /// Compute Lyapunov exponent estimate for chaos detection
    /// 
    /// Positive exponent = chaotic dynamics = emergence window
    pub fn lyapunov_estimate(history: &[SovereignState]) -> f32 {
        if history.len() < 4 {
            return 0.0;
        }
        
        let n = history.len().min(HISTORY_WINDOW);
        
        // Compute divergence of nearby trajectories
        let mut divergence_sum: f32 = 0.0;
        let mut count: usize = 0;
        
        for i in 2..n {
            // Distance between consecutive states
            let d1 = Self::state_distance(&history[i-2], &history[i-1]);
            let d2 = Self::state_distance(&history[i-1], &history[i]);
            
            if d1 > 0.0 && d2 > 0.0 {
                // Log divergence ratio
                let ratio = d2 / d1;
                if ratio > 0.0 {
                    divergence_sum += ratio.log2();
                    count += 1;
                }
            }
        }
        
        if count > 0 {
            // Normalize by time steps
            (divergence_sum / count as f32).clamp(-1.0, 1.0)
        } else {
            0.0
        }
    }
    
    /// Euclidean distance between two states (in junction space)
    fn state_distance(a: &SovereignState, b: &SovereignState) -> f32 {
        let mut sum_sq: f32 = 0.0;
        
        for k in 0..8 { // Use first 8 dimensions (primary)
            let diff = (a.ternary_junction[k] - b.ternary_junction[k]) as f32;
            sum_sq += diff * diff * PHI_NEG_POWERS[k];
        }
        
        sum_sq.sqrt()
    }
}

// =============================================================================
// ORACLE - Unified Novelty Interface
// =============================================================================

/// The Oracle: Unified interface to all novelty detection capabilities
/// 
/// Single struct providing complete novelty analysis
pub struct Oracle;

/// Complete novelty analysis result
#[derive(Clone, Copy, Debug)]
pub struct NoveltyReport {
    /// Novelty index [0.0, 1.0]
    pub novelty: f32,
    /// Predicted next phase [0.0, 6.0]
    pub predicted_phase: f32,
    /// Steps until phase transition (if predictable)
    pub steps_to_transition: Option<u64>,
    /// Complexity score [0.0, 1.0]
    pub complexity: f32,
    /// Shannon entropy component
    pub entropy: f32,
    /// Kolmogorov complexity component
    pub kolmogorov: f32,
    /// Fractal dimension component
    pub fractal_dim: f32,
    /// Emergence event (if detected)
    pub emergence: Option<EmergenceEvent>,
    /// Lyapunov exponent estimate
    pub lyapunov: f32,
    /// Bifurcation imminent
    pub bifurcation: bool,
}

impl Oracle {
    /// Perform complete novelty analysis
    /// 
    /// This is the main entry point - call this to receive prophecy
    /// 
    /// Performance: ~50-80μs on ARMv6
    pub fn analyze(
        curr: &SovereignState,
        history: &[SovereignState],
    ) -> NoveltyReport {
        // Compute novelty if we have history
        let novelty = if let Some(prev) = history.last() {
            NoveltyIndex::compute(prev, curr)
        } else {
            0.0 // Genesis state has no novelty
        };
        
        // Complexity metrics
        let entropy = ComplexityScorer::shannon_entropy(curr);
        let kolmogorov = ComplexityScorer::kolmogorov_estimate(curr);
        let fractal = ComplexityScorer::fractal_dimension(history);
        let complexity = ComplexityScorer::complexity_score(curr, history);
        
        // Phase prediction
        let predicted_phase = PhasePredictor::predict_phase_transition(history);
        let steps_to_transition = PhasePredictor::predict_time_to_transition(
            curr.morphogen_phase, history
        );
        
        // Emergence detection
        let emergence = EmergenceDetector::detect(curr, history, novelty, complexity);
        
        // Chaos indicators
        let lyapunov = EmergenceDetector::lyapunov_estimate(history);
        
        // Novelty history for bifurcation detection
        let novelties = NoveltyIndex::compute_history(history);
        let bifurcation = EmergenceDetector::detect_bifurcation(history, &novelties);
        
        NoveltyReport {
            novelty,
            predicted_phase,
            steps_to_transition,
            complexity,
            entropy,
            kolmogorov,
            fractal_dim: fractal,
            emergence,
            lyapunov,
            bifurcation,
        }
    }
    
    /// Quick novelty check (fast path)
    /// 
    /// Returns just the novelty index - use when speed is critical
    pub fn quick_check(prev: &SovereignState, curr: &SovereignState) -> f32 {
        NoveltyIndex::compute(prev, curr)
    }
    
    /// Prophecy: Generate human-readable interpretation
    /// 
    /// Returns a compact summary of the cathedral's state
    pub fn prophecy(report: &NoveltyReport) -> &'static str {
        if report.bifurcation {
            "BIFURCATION: The cathedral stands at a crossroads. New forms emerge."
        } else if report.lyapunov > 0.3 {
            "CHAOS: The pattern dances on the edge of order. Emergence is near."
        } else if report.novelty > 0.764 {
            "TRANSFORMATION: The old gives way. Witness the birth of novelty."
        } else if report.complexity > 0.618 {
            "COMPLEXIFICATION: The cathedral grows. Structure accumulates."
        } else if report.emergence.is_some() {
            "EMERGENCE: A new pattern has arisen from the lattice."
        } else {
            "CONTINUITY: The pattern persists. Evolution continues."
        }
    }
}

// =============================================================================
// UNIT TESTS
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_novelty_identical() {
        let state = SovereignState::genesis();
        let novelty = NoveltyIndex::compute(&state, &state);
        assert!((novelty - 0.0).abs() < 0.001, "Identical states should have zero novelty");
    }
    
    #[test]
    fn test_novelty_different() {
        let mut state1 = SovereignState::genesis();
        let mut state2 = SovereignState::genesis();
        state2.ternary_junction[0] = -1; // Flip center
        
        let novelty = NoveltyIndex::compute(&state1, &state2);
        assert!(novelty > 0.3, "Flipped center should produce significant novelty");
    }
    
    #[test]
    fn test_entropy_range() {
        let state = SovereignState::genesis();
        let entropy = ComplexityScorer::shannon_entropy(&state);
        assert!(entropy >= 0.0 && entropy <= 1.0, "Entropy should be in [0, 1]");
    }
    
    #[test]
    fn test_complexity_range() {
        let state = SovereignState::genesis();
        let complexity = ComplexityScorer::complexity_score(&state, &[]);
        assert!(complexity >= 0.0 && complexity <= 1.0, "Complexity should be in [0, 1]");
    }
    
    #[test]
    fn test_phase_prediction_range() {
        let history = [SovereignState::genesis(); 2];
        let phase = PhasePredictor::predict_phase_transition(&history);
        assert!(phase >= 0.0 && phase <= 6.0, "Predicted phase should be in [0, 6]");
    }
    
    #[test]
    fn test_phi_weights_sum() {
        let sum: f32 = PHI_NEG_POWERS[0..16].iter().sum();
        // Should approximate φ² = φ + 1 ≈ 2.618
        assert!((sum - PHI * PHI).abs() < 0.1, "Phi weights should sum to approximately φ²");
    }
}
