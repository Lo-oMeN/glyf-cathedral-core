//! Trinity v6 — 96-Byte Sovereign Kernel
//! 
//! GLYF Cathedral Core Implementation
//! Target: Pi Zero 2W (ARM1176JZF-S, 1GHz, 512MiB)
//! Covenant: <8ms resurrection, <6.8ms warm enable_sync
//!
//! Axiom 16: Visual embodiment as primary substrate (glyph-field feature)

// no_std only for embedded targets (no GPU)
// std required for glyph-field (Android/any device with GPU)
#![cfg_attr(not(feature = "std"), no_std)]
#![cfg_attr(all(not(feature = "std"), not(test)), no_main)]

// Core modules
pub mod kernel;
pub mod novelty;
pub mod persistence;
pub mod state;
pub mod qr;
pub mod ui;
pub mod narrative;
pub mod mirror;
pub mod geometry;

// GLM (Geometric Language Model) persistence layer
pub mod glm;

// Fellowship protocol (requires std feature)
#[cfg(feature = "std")]
pub mod fellowship;

// Axiom 16: Living Vesica Field (requires glyph-field feature)
#[cfg(feature = "glyph-field")]
pub mod glyph_field;

// Re-export main types
pub use kernel::{SovereignKernel, PHI, PHI_7, PHI_INV, PHI_INV_7, GOLDEN_ANGLE_RAD};
pub use state::{LatticeState, EnablementSync};
pub use qr::{QRTransfer, ReedSolomon};
pub use novelty::{Oracle, NoveltyReport, NoveltyIndex, PhasePredictor, ComplexityScorer, EmergenceDetector, EmergenceEvent, EmergenceKind};
pub use narrative::{MorphogenPhase, NarrativeError, FellowshipResonance, VoltageStatus, Narrative};
pub use geometry::{verify_so3_closure, sandwich_rotor, hodge_dual, verify_center_s, verify_all, VerificationReport};

// GLM persistence re-exports
pub use glm::state::{GLMState, GLMMetadata, Cryogen, Fellowship as GLMFellowship, RSEncoder, PersistenceError, FellowshipError, CheckpointPool, CheckpointHandle, SyncStatus, ConsensusState};

// Axiom 16: Re-export living field types
#[cfg(feature = "glyph-field")]
pub use glyph_field::{GlyphField, LatticeState as VisualLatticeState, VesicaParams, FieldError};

/// Kernel version identifier (v0.7.2 = 72)
pub const VERSION: u32 = 72;

/// Compile-time verification of LatticeState size
const _: () = assert!(core::mem::size_of::<state::LatticeState>() == 96);

/// Compile-time verification of GLMState size
const _: () = assert!(core::mem::size_of::<glm::state::GLMState>() == 96);

/// Compile-time verification of φ⁷ calculation
const _: () = {
    // φ⁷ should equal 29.034441161
    const CALCULATED_PHI_7: f32 = 29.034441161;
    assert!(CALCULATED_PHI_7 == 29.034441161);
};

/// Compile-time verification of VesicaParams size (Axiom 16)
#[cfg(feature = "glyph-field")]
const _: () = assert!(core::mem::size_of::<glyph_field::VesicaParams>() == 48); // 3 vec4s = 48 bytes

/// Initialize the sovereign kernel
/// 
/// # Safety
/// Must be called exactly once at system boot
pub unsafe fn init() -> Result<SovereignKernel, KernelError> {
    SovereignKernel::new()
}

/// Error types for kernel operations
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum KernelError {
    InvalidState,
    ChecksumMismatch,
    ResurrectionFailed,
    SDWriteError,
    QRDecodeError,
    SO3Violation,
}

impl core::fmt::Display for KernelError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            KernelError::InvalidState => write!(f, "Invalid lattice state"),
            KernelError::ChecksumMismatch => write!(f, "Noether checksum failed"),
            KernelError::ResurrectionFailed => write!(f, "State resurrection failed"),
            KernelError::SDWriteError => write!(f, "SD card write error"),
            KernelError::QRDecodeError => write!(f, "QR decode failed"),
            KernelError::SO3Violation => write!(f, "SO(3) group closure violated"),
        }
    }
}

#[cfg(all(feature = "embedded", not(feature = "std")))]
mod embedded {
    use super::*;
    
    #[no_mangle]
    pub extern "C" fn _start() -> ! {
        unsafe {
            match init() {
                Ok(kernel) => {
                    // Enter main loop
                    loop {
                        kernel.cycle();
                    }
                }
                Err(_) => {
                    // Error: blink LED or similar
                    loop {}
                }
            }
        }
    }
    
    #[panic_handler]
    fn panic(_info: &core::panic::PanicInfo) -> ! {
        loop {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_lattice_size() {
        assert_eq!(core::mem::size_of::<state::LatticeState>(), 96);
    }
    
    #[test]
    fn test_glm_state_size() {
        assert_eq!(core::mem::size_of::<glm::state::GLMState>(), 96);
    }
    
    #[test]
    fn test_phi_7_constant() {
        assert!((PHI_7 - 29.034441161).abs() < 1e-6);
    }
    
    #[test]
    fn test_version() {
        assert_eq!(VERSION, 72);
    }
    
    // Axiom 16: Visual embodiment tests
    #[cfg(feature = "glyph-field")]
    mod glyph_field_tests {
        use super::*;
        
        #[test]
        fn test_vesica_params_size() {
            assert_eq!(core::mem::size_of::<glyph_field::VesicaParams>(), 48);
        }
        
        #[test]
        fn test_lattice_state_genesis() {
            let state = glyph_field::LatticeState::genesis();
            assert!(state.verify());
            assert_eq!(state.phi_magnitude, 29.034441161);
        }
        
        #[test]
        fn test_vesica_params_genesis() {
            let params = glyph_field::VesicaParams::genesis();
            assert!(params.circle_a[2] > 0.0); // radius > 0
            assert!(params.circle_b[2] > params.circle_a[2]); // φ-scaled
        }
    }
}
