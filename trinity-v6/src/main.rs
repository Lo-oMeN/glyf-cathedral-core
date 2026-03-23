//! Trinity v6 — Kernel Binary Entry Point
//! 
//! For Pi Zero 2W bare metal or Linux userspace

#![no_std]
#![no_main]

use trinity_v6::{init, KernelError, LatticeState};

#[no_mangle]
pub extern "C" fn main() -> i32 {
    unsafe {
        match init() {
            Ok(kernel) => {
                // Main sovereign loop
                loop {
                    kernel.cycle();
                }
            }
            Err(e) => {
                // Return error code
                match e {
                    KernelError::InvalidState => 1,
                    KernelError::ChecksumMismatch => 2,
                    KernelError::ResurrectionFailed => 3,
                    KernelError::SDWriteError => 4,
                    KernelError::QRDecodeError => 5,
                    KernelError::SO3Violation => 6,
                }
            }
        }
    }
}

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}
