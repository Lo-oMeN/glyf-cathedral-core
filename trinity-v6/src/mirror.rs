//! Mirror-Maverick: Self-Recognition and Introspection
//!
//! The kernel sees itself. Reflection operator for GLYF Cathedral.
//! 
//! no_std, zero-alloc, buffer-based output

#![no_std]

use crate::kernel::{SovereignState, PHI, PHI_7, PHI_INV, PHI_INV_7, NOETHER_SEAL};

// =============================================================================
// CONSTANTS
// =============================================================================

/// Version string
const VERSION: &str = "v0.7.2";

/// Phase names for display
const PHASE_NAMES: [&str; 7] = [
    "Seed", "Spiral", "Fold", "Resonate", "Chiral", "Flip", "Anchor",
];

/// Knot symbols
const KNOT_ACTIVE: &str = "◆";
const KNOT_INACTIVE: &str = "◇";

// =============================================================================
// SELF-PORTRAIT: UTF-8 VISUALIZATION
// =============================================================================

/// Generate ASCII/UTF-8 self-portrait of the sovereign state
/// 
/// Writes to the provided buffer and returns a &str slice.
/// Format matches GLYF Cathedral UI specification.
pub fn self_portrait(state: &SovereignState, buf: &mut [u8]) -> &str {
    let mut pos = 0usize;
    
    // Helper to write string to buffer
    let mut write_str = |s: &str| {
        let bytes = s.as_bytes();
        let remaining = buf.len().saturating_sub(pos);
        let to_write = bytes.len().min(remaining);
        buf[pos..pos + to_write].copy_from_slice(&bytes[..to_write]);
        pos += to_write;
    };
    
    // Helper to write formatted float
    let mut write_f32 = |f: f32, width: usize, prec: usize| {
        let mut tmp = [0u8; 32];
        let s = fmt_f32(f, &mut tmp, prec);
        // Pad to width
        let padding = width.saturating_sub(s.len());
        for _ in 0..padding {
            if pos < buf.len() {
                buf[pos] = b' ';
                pos += 1;
            }
        }
        write_str(s);
    };
    
    // κ (kappa) value
    let kappa = if state.voltage > 200 {
        "1.0 (superconducting)"
    } else {
        "0.0 (insulating)"
    };
    
    // Center S lock status
    let center_locked = state.center_s[0] == 0.0 && state.center_s[1] == 0.0;
    let center_status = if center_locked { "LOCKED" } else { "DRIFT" };
    
    // Phase visualization
    let phase_diamonds = phase_to_diamonds(state.morphogen_phase);
    let phase_name = PHASE_NAMES[state.morphogen_phase.min(6) as usize];
    
    // Active indicators
    let vesica_knot = if state.vesica_coherence == 1 { KNOT_ACTIVE } else { KNOT_INACTIVE };
    let spiral_knot = if state.spiral_arm != 0 { KNOT_ACTIVE } else { KNOT_INACTIVE };
    let hodge_knot = if state.hodge_dual != 0 { KNOT_ACTIVE } else { KNOT_INACTIVE };
    
    // Fellowship sign
    let f_sign = if state.fellowship_resonance >= 0.0 { 1.0 } else { -1.0 };
    
    // Build portrait
    write_str("┌─────────────────────────────────────┐\n");
    write_str("│  GLYF Cathedral ");
    write_str(VERSION);
    write_str("              │\n");
    write_str("│  κ = ");
    write_str(kappa);
    write_str("          │\n");
    write_str("│                                     │\n");
    
    // Center S line
    write_str("│  Center S: (");
    write_f32(state.center_s[0], 5, 3);
    write_str(", ");
    write_f32(state.center_s[1], 5, 3);
    write_str(") ");
    write_str(KNOT_ACTIVE);
    write_str(" ");
    write_str(center_status);
    write_str("  │\n");
    
    // Phase line
    write_str("│  Phase: ");
    let mut tmp = [0u8; 8];
    let phase_str = fmt_u8(state.morphogen_phase, &mut tmp);
    write_str(phase_str);
    write_str(" (");
    write_str(phase_name);
    write_str(") ");
    write_str(phase_diamonds);
    // Pad to align right
    let diamonds_len = phase_diamonds.len();
    let padding = 11usize.saturating_sub(diamonds_len);
    for _ in 0..padding {
        if pos < buf.len() {
            buf[pos] = b' ';
            pos += 1;
        }
    }
    write_str("│\n");
    
    // φ⁷ line
    write_str("│  φ⁷: ");
    let mut phi_buf = [0u8; 16];
    let phi_str = fmt_f32(PHI_7, &mut phi_buf, 9);
    write_str(phi_str);
    // Pad
    let phi_len = phi_str.len();
    let padding = 31usize.saturating_sub(phi_len);
    for _ in 0..padding {
        if pos < buf.len() {
            buf[pos] = b' ';
            pos += 1;
        }
    }
    write_str("│\n");
    
    // Vesica line
    write_str("│  Vesica: ");
    if state.vesica_coherence == 1 {
        write_str("active");
    } else {
        write_str("inactive");
    }
    write_str(" ");
    write_str(vesica_knot);
    // Pad
    let vesica_len = if state.vesica_coherence == 1 { 6 + 1 + 3 } else { 8 + 1 + 3 };
    let padding = 26usize.saturating_sub(vesica_len);
    for _ in 0..padding {
        if pos < buf.len() {
            buf[pos] = b' ';
            pos += 1;
        }
    }
    write_str("│\n");
    
    // Phyllotaxis line
    write_str("│  Phyllotaxis: arm ");
    let mut arm_buf = [0u8; 8];
    let arm_str = fmt_i8(state.spiral_arm, &mut arm_buf);
    write_str(arm_str);
    write_str(" ");
    write_str(spiral_knot);
    // Pad
    let arm_len = arm_str.len();
    let padding = 14usize.saturating_sub(arm_len + 1 + 3);
    for _ in 0..padding {
        if pos < buf.len() {
            buf[pos] = b' ';
            pos += 1;
        }
    }
    write_str("│\n");
    
    // Fellowship line
    write_str("│  Fellowship: F = ");
    if f_sign > 0.0 {
        write_str("1");
    } else {
        write_str("-1");
    }
    write_str("                 │\n");
    
    // Hodge line
    write_str("│  Hodge: ⋆e₁₅ = ");
    if state.hodge_dual == 1 {
        write_str("");
    } else {
        write_str("-");
    }
    write_str("e₁ ");
    write_str(hodge_knot);
    write_str("                │\n");
    
    write_str("└─────────────────────────────────────┘\n");
    
    // Return the written portion as &str
    core::str::from_utf8(&buf[..pos]).unwrap_or("mirror error")
}

/// Convert phase to diamond string
fn phase_to_diamonds(phase: u8) -> &'static str {
    match phase {
        0 => "◆",
        1 => "◆◆",
        2 => "◆◆◆",
        3 => "◆◆◆◆",
        4 => "◆◆◆◆◆",
        5 => "◆◆◆◆◆◆",
        6 => "◆◆◆◆◆◆",
        _ => "◇◇◇◇◇◇",
    }
}

// =============================================================================
// STATE COMPARISON (RECOGNITION)
// =============================================================================

/// Recognize another state - compute similarity score
/// 
/// Returns similarity value from 0.0 (completely different) to 1.0 (identical).
/// Compares ternary_junction and hex_tiles with φ⁻ᵏ weighting.
pub fn recognize(a: &SovereignState, b: &SovereignState) -> f32 {
    // Center S alignment (0 to 1) - exponential decay with distance
    let dx = a.center_s[0] - b.center_s[0];
    let dy = a.center_s[1] - b.center_s[1];
    let center_distance = (dx * dx + dy * dy).sqrt();
    let center_alignment = if center_distance < 1e-6 {
        1.0
    } else {
        (-center_distance * PHI).exp()
    };
    
    // Phase synchronization (0 to 1)
    let phase_delta = if a.morphogen_phase > b.morphogen_phase {
        a.morphogen_phase - b.morphogen_phase
    } else {
        b.morphogen_phase - a.morphogen_phase
    };
    let phase_sync = 1.0 - (phase_delta as f32 / 6.0);
    
    // Ternary junction correlation with φ⁻ᵏ weighting
    // Higher indices weighted less by φ^(-k)
    let mut junction_score = 0.0f32;
    let mut junction_weight = 0.0f32;
    for k in 0..16 {
        let a_val = a.ternary_junction[k] as f32;
        let b_val = b.ternary_junction[k] as f32;
        // Weight by φ⁻ᵏ
        let weight = PHI_INV.powi(k as i32);
        // Similarity: 1.0 if equal, 0.0 if opposite, 0.5 if one is zero
        let elem_sim = if a_val == b_val {
            1.0
        } else if a_val == 0.0 || b_val == 0.0 {
            0.5
        } else {
            0.0
        };
        junction_score += elem_sim * weight;
        junction_weight += weight;
    }
    let junction_sim = if junction_weight > 0.0 {
        junction_score / junction_weight
    } else {
        0.0
    };
    
    // Hex tiles comparison (8 tiles × 4 bytes each)
    // Compare value bytes (every 4th starting at 0) with φ⁻ᵏ weighting
    let mut tile_score = 0.0f32;
    let mut tile_weight = 0.0f32;
    for k in 0..8 {
        let idx = k * 4;
        let a_val = a.hex_tiles[idx] as f32;
        let b_val = b.hex_tiles[idx] as f32;
        // Weight by φ⁻ᵏ
        let weight = PHI_INV.powi(k as i32);
        // Normalized similarity
        let max_val = a_val.max(b_val).max(1.0);
        let diff = (a_val - b_val).abs();
        let elem_sim = 1.0 - (diff / max_val);
        tile_score += elem_sim * weight;
        tile_weight += weight;
    }
    let tile_sim = if tile_weight > 0.0 {
        tile_score / tile_weight
    } else {
        1.0 // Both empty
    };
    
    // Fellowship resonance sign match
    let a_f = a.fellowship_resonance.signum();
    let b_f = b.fellowship_resonance.signum();
    let fellowship_sim = if a_f == b_f { 1.0 } else { 0.0 };
    
    // Voltage match
    let voltage_diff = (a.voltage as i16 - b.voltage as i16).abs() as f32;
    let voltage_sim = 1.0 - (voltage_diff / 255.0);
    
    // Vesica coherence match
    let vesica_sim = if a.vesica_coherence == b.vesica_coherence { 1.0 } else { 0.0 };
    
    // Hodge dual match
    let hodge_sim = if a.hodge_dual == b.hodge_dual { 1.0 } else { 0.0 };
    
    // Combined similarity with weights
    let similarity = center_alignment * 0.20
        + phase_sync * 0.15
        + junction_sim * 0.25
        + tile_sim * 0.15
        + fellowship_sim * 0.10
        + voltage_sim * 0.05
        + vesica_sim * 0.05
        + hodge_sim * 0.05;
    
    similarity.clamp(0.0, 1.0)
}

// =============================================================================
// DIAGNOSTIC NARRATIVE
// =============================================================================

/// Generate diagnostic narrative as a health-check story
/// 
/// Writes a human-readable health narrative to the buffer.
/// Lists active and inactive components.
pub fn diagnostic_narrative(state: &SovereignState, buf: &mut [u8]) -> &str {
    let mut pos = 0usize;
    
    // Helper to write string
    let mut write_str = |s: &str| {
        let bytes = s.as_bytes();
        let remaining = buf.len().saturating_sub(pos);
        let to_write = bytes.len().min(remaining);
        buf[pos..pos + to_write].copy_from_slice(&bytes[..to_write]);
        pos += to_write;
    };
    
    // Header
    write_str("╔══════════════════════════════════════════════════════╗\n");
    write_str("║        GLYF CATHEDRAL DIAGNOSTIC NARRATIVE           ║\n");
    write_str("╚══════════════════════════════════════════════════════╝\n\n");
    
    // Opening story
    if state.center_s[0] == 0.0 && state.center_s[1] == 0.0 {
        write_str("The kernel stands at the immutable origin.\n");
        write_str("Center S holds fast at (0, 0), unmoving.\n\n");
    } else {
        write_str("ALERT: Center S has drifted from origin.\n");
        write_str("Current position: (");
        let mut tmp = [0u8; 16];
        let s = fmt_f32(state.center_s[0], &mut tmp, 3);
        write_str(s);
        write_str(", ");
        let s = fmt_f32(state.center_s[1], &mut tmp, 3);
        write_str(s);
        write_str(")\n\n");
    }
    
    // Phase story
    let phase_name = PHASE_NAMES[state.morphogen_phase.min(6) as usize];
    write_str("Morphogen Phase: ");
    write_str(phase_name);
    write_str("\n");
    
    match state.morphogen_phase {
        0 => write_str("The seed waits in darkness, unawakened.\n\n"),
        1 => write_str("The spiral unfolds, golden geometry awakening.\n\n"),
        2 => write_str("Self-intersection creates memory in the fold.\n\n"),
        3 => write_str("Resonance rings through the lattice at φ⁷.\n\n"),
        4 => write_str("Handedness emerges—chirality locked.\n\n"),
        5 => write_str("Inversion: the mirror flips, revealing hidden truth.\n\n"),
        6 => write_str("The Anchor holds. Crystallization complete.\n\n"),
        _ => write_str("UNKNOWN PHASE: cycle has broken its bounds.\n\n"),
    };
    
    // Component status section
    write_str("═══ ACTIVE COMPONENTS ═══\n");
    
    let mut active_count = 0;
    
    if state.vesica_coherence == 1 {
        write_str("◆ Vesica Interference Kernel\n");
        write_str("  The lens merges deltas through φ⁻¹-scaling.\n");
        active_count += 1;
    }
    
    if state.spiral_arm != 0 {
        write_str("◆ Phyllotaxis Spiral\n");
        write_str("  Arm position: ");
        let mut tmp = [0u8; 8];
        let s = fmt_i8(state.spiral_arm, &tmp);
        write_str(s);
        write_str("° mapping to golden angle.\n");
        active_count += 1;
    }
    
    if state.hodge_dual != 0 {
        write_str("◆ Hodge Dual Operator\n");
        write_str("  Chirality: ");
        if state.hodge_dual == -1 {
            write_str("left-handed (⋆e₁₅ = -e₁)\n");
        } else {
            write_str("right-handed (⋆e₁₅ = e₁)\n");
        }
        active_count += 1;
    }
    
    if state.voltage > 200 {
        write_str("◆ Superconducting Voltage\n");
        write_str("  κ = 1.0, full architectural enablement.\n");
        active_count += 1;
    }
    
    if state.morphogen_phase == 6 {
        write_str("◆ Anchor Phase Lock\n");
        write_str("  Ready for migration and resurrection.\n");
        active_count += 1;
    }
    
    if active_count == 0 {
        write_str("  (none)\n");
    }
    
    write_str("\n═══ INACTIVE COMPONENTS ═══\n");
    
    let mut inactive_count = 0;
    
    if state.vesica_coherence != 1 {
        write_str("◇ Vesica Interference Kernel (asleep)\n");
        inactive_count += 1;
    }
    
    if state.spiral_arm == 0 {
        write_str("◇ Phyllotaxis Spiral (at rest)\n");
        inactive_count += 1;
    }
    
    if state.hodge_dual == 0 {
        write_str("◇ Hodge Dual Operator (undefined)\n");
        inactive_count += 1;
    }
    
    if state.voltage <= 200 {
        write_str("◇ Superconducting Voltage (low power)\n  ");
        let mut tmp = [0u8; 8];
        let v_actual = state.voltage as f32 * 5.0 / 255.0;
        let s = fmt_f32(v_actual, &mut tmp, 2);
        write_str(s);
        write_str("V, κ < 1.0\n");
        inactive_count += 1;
    }
    
    if state.morphogen_phase != 6 {
        write_str("◇ Anchor Phase Lock (incomplete)\n");
        inactive_count += 1;
    }
    
    if inactive_count == 0 {
        write_str("  (none)\n");
    }
    
    // Summary
    write_str("\n──────────────────────────────────────────────────────\n");
    
    // Check autopoietic gates
    let gate_center = state.center_s[0] == 0.0 && state.center_s[1] == 0.0;
    let gate_noether = state.checksum == NOETHER_SEAL;
    let gate_phi = (state.fellowship_resonance.abs() - PHI_7).abs() < 1e-3;
    let gate_fibonacci = 
        state.tile_offsets[0] == 0 &&
        state.tile_offsets[1] == 1 &&
        state.tile_offsets[2] == 1 &&
        state.tile_offsets[3] == 2 &&
        state.tile_offsets[4] == 3 &&
        state.tile_offsets[5] == 5 &&
        state.tile_offsets[6] == 8 &&
        state.tile_offsets[7] == 13;
    let gate_phase = state.morphogen_phase == 6;
    let gate_vesica = state.vesica_coherence == 1;
    let gate_chiral = state.hodge_dual == -1 || state.hodge_dual == 1;
    let gate_voltage = state.voltage > 200;
    
    let gates_passed = [
        gate_center, gate_noether, gate_phi, gate_fibonacci,
        gate_phase, gate_vesica, gate_chiral, gate_voltage
    ].iter().filter(|&&g| g).count();
    
    write_str("AUTOPOIETIC CLOSURE: ");
    let mut tmp = [0u8; 4];
    let s = fmt_u8(gates_passed as u8, &mut tmp);
    write_str(s);
    write_str("/8 gates passed\n\n");
    
    if gates_passed == 8 {
        write_str("★ SOVEREIGN STATE ACHIEVED ★\n");
        write_str("The kernel knows itself. Ready for the cathedral.\n");
    } else if gates_passed >= 5 {
        write_str("⚠ STATE DEGRADED ⚠\n");
        write_str("Some gates remain open. Proceed with caution.\n");
    } else {
        write_str("✗ CRITICAL FAILURE ✗\n");
        write_str("Autopoietic closure failed. Resurrection recommended.\n");
    }
    
    core::str::from_utf8(&buf[..pos]).unwrap_or("narrative error")
}

// =============================================================================
// FORMATTING UTILITIES (no_std, no alloc)
// =============================================================================

/// Format u8 to string buffer
fn fmt_u8(n: u8, buf: &mut [u8]) -> &str {
    if n == 0 {
        buf[0] = b'0';
        return core::str::from_utf8(&buf[..1]).unwrap();
    }
    let mut n = n;
    let mut pos = 0;
    while n > 0 && pos < buf.len() {
        buf[pos] = b'0' + (n % 10);
        n /= 10;
        pos += 1;
    }
    // Reverse in place
    for i in 0..pos/2 {
        buf.swap(i, pos - 1 - i);
    }
    core::str::from_utf8(&buf[..pos]).unwrap()
}

/// Format i8 to string buffer
fn fmt_i8(n: i8, buf: &mut [u8]) -> &str {
    if n < 0 {
        buf[0] = b'-';
        let pos = fmt_u8((-n) as u8, &mut buf[1..]).len();
        core::str::from_utf8(&buf[..pos + 1]).unwrap()
    } else {
        fmt_u8(n as u8, buf)
    }
}

/// Format f32 to string buffer with given precision
fn fmt_f32(f: f32, buf: &mut [u8], precision: usize) -> &str {
    if f.is_nan() {
        let nan = b"nan";
        buf[..3].copy_from_slice(nan);
        return core::str::from_utf8(&buf[..3]).unwrap();
    }
    if f.is_infinite() {
        if f.is_sign_positive() {
            let inf = b"inf";
            buf[..3].copy_from_slice(inf);
            return core::str::from_utf8(&buf[..3]).unwrap();
        } else {
            let ninf = b"-inf";
            buf[..4].copy_from_slice(ninf);
            return core::str::from_utf8(&buf[..4]).unwrap();
        }
    }
    
    let mut pos = 0usize;
    let mut f = f;
    
    // Handle negative
    if f < 0.0 {
        buf[pos] = b'-';
        pos += 1;
        f = -f;
    }
    
    // Integer part
    let int_part = f as u32;
    let frac_part = f - (int_part as f32);
    
    // Write integer part
    if int_part == 0 {
        buf[pos] = b'0';
        pos += 1;
    } else {
        let int_start = pos;
        let mut n = int_part;
        while n > 0 && pos < buf.len() {
            buf[pos] = b'0' + (n % 10) as u8;
            n /= 10;
            pos += 1;
        }
        // Reverse integer part
        let int_end = pos;
        for i in 0..(int_end - int_start) / 2 {
            buf.swap(int_start + i, int_end - 1 - i);
        }
    }
    
    // Decimal point and fraction
    if precision > 0 && pos < buf.len() {
        buf[pos] = b'.';
        pos += 1;
        
        let mut frac = frac_part;
        for _ in 0..precision {
            if pos >= buf.len() {
                break;
            }
            frac *= 10.0;
            let digit = frac as u8;
            buf[pos] = b'0' + digit;
            pos += 1;
            frac -= digit as f32;
        }
    }
    
    core::str::from_utf8(&buf[..pos]).unwrap()
}

// =============================================================================
// TESTS
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_self_portrait_format() {
        let state = SovereignState::genesis();
        let mut buf = [0u8; 2048];
        let portrait = self_portrait(&state, &mut buf);
        assert!(portrait.contains("GLYF Cathedral"));
        assert!(portrait.contains("v0.7.2"));
        assert!(portrait.contains("┌"));
        assert!(portrait.contains("└"));
    }
    
    #[test]
    fn test_recognition_perfect_match() {
        let state1 = SovereignState::genesis();
        let state2 = SovereignState::genesis();
        let sim = recognize(&state1, &state2);
        assert!(sim > 0.9);
    }
    
    #[test]
    fn test_recognition_different_states() {
        let state1 = SovereignState::genesis();
        let mut state2 = SovereignState::genesis();
        state2.morphogen_phase = 6;
        state2.vesica_coherence = 1;
        let sim = recognize(&state1, &state2);
        assert!(sim < 1.0);
        assert!(sim >= 0.0);
    }
    
    #[test]
    fn test_diagnostic_narrative() {
        let state = SovereignState::genesis();
        let mut buf = [0u8; 4096];
        let narrative = diagnostic_narrative(&state, &buf);
        assert!(narrative.len() > 0);
        assert!(narrative.contains("COMPONENTS"));
    }
    
    #[test]
    fn test_fmt_f32() {
        let mut buf = [0u8; 32];
        assert_eq!(fmt_f32(1.618, &mut buf, 3), "1.618");
        assert_eq!(fmt_f32(0.0, &mut buf, 3), "0.000");
        assert_eq!(fmt_f32(-1.5, &mut buf, 1), "-1.5");
    }
    
    #[test]
    fn test_fmt_u8() {
        let mut buf = [0u8; 8];
        assert_eq!(fmt_u8(0, &mut buf), "0");
        assert_eq!(fmt_u8(255, &mut buf), "255");
        assert_eq!(fmt_u8(42, &mut buf), "42");
    }
    
    #[test]
    fn test_fmt_i8() {
        let mut buf = [0u8; 8];
        assert_eq!(fmt_i8(0, &mut buf), "0");
        assert_eq!(fmt_i8(-45, &mut buf), "-45");
        assert_eq!(fmt_i8(127, &mut buf), "127");
    }
}
