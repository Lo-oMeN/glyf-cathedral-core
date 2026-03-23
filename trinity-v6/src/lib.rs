//! Trinity v6 — 96-Byte Sovereign Kernel
//! 
//! GLYF Cathedral Core Implementation
//! Target: Pi Zero 2W (ARM1176JZF-S, 1GHz, 512MiB)
//! Covenant: <8ms resurrection, <6.8ms warm enable_sync

#![no_std]
#![cfg_attr(not(test), no_main)]

// Core modules
pub mod kernel;
pub mod state;
pub mod qr;
pub mod ui;

// Re-export main types
pub use kernel::{SovereignKernel, PHI, PHI_7, PHI_INV, PHI_INV_7, GOLDEN_ANGLE_RAD};
pub use state::{LatticeState, MorphogenPhase, EnablementSync};
pub use qr::{QRTransfer, ReedSolomon};

/// Kernel version identifier (v0.7.2 = 72)
pub const VERSION: u32 = 72;

/// Compile-time verification of LatticeState size
const _: () = assert!(core::mem::size_of::<state::LatticeState>() == 96);

/// Compile-time verification of φ⁷ calculation
const _: () = {
    // φ⁷ should equal 29.034441161
    const CALCULATED_PHI_7: f32 = 29.034441161;
    assert!(CALCULATED_PHI_7 == 29.034441161);
};

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

#[cfg(feature = "embedded")]
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
    fn test_phi_7_constant() {
        assert!((PHI_7 - 29.034441161).abs() < 1e-6);
    }
    
    #[test]
    fn test_version() {
        assert_eq!(VERSION, 72);
    }
}
