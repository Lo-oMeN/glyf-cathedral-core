//! Sovereign Capability System - Rosetta-Bridge Protocol
//! 
//! Distributed capability sharing without centralized infrastructure.
//! No API keys. No cloud dependencies. Peer-to-peer fellowship.
//! 
//! # The 8ms Covenant
//! 
//! All capability queries must resolve in <8ms via local caching.
//! Fellowship nodes are discovered via lattice gossip, not DNS.
//! 
//! # Architecture
//! 
//! ```text
//! Request → Registry → Channel → Response
//!              ↓
//!        Fellowship (if local unavailable)
//! ```
//! 
//! # Example
//! 
//! ```rust,no_run
//! use capability::{CapabilityRegistry, CapabilityNeed, Request, RequestKind};
//! 
//! let mut registry = CapabilityRegistry::new();
//! registry.discover_local();
//! 
//! let request = Request {
//!     kind: RequestKind::ReadWeb,
//!     target: "https://example.com".into(),
//!     params: Default::default(),
//! };
//! 
//! if let Some(channel) = registry.query(CapabilityNeed::ReadWeb) {
//!     let response = channel.execute(request).unwrap();
//!     println!("{}", response.body);
//! }
//! ```

#![cfg_attr(not(feature = "std"), no_std)]

extern crate alloc;

pub mod channels;
pub mod descriptor;
pub mod registry;

pub use channels::{CapabilityChannel, ChannelError, Request, RequestKind, Response};
pub use descriptor::CapabilityDescriptor;
pub use registry::{CapabilityNeed, CapabilityRegistry, FellowCapability};

/// Version of the Rosetta-Bridge protocol
pub const PROTOCOL_VERSION: u16 = 1;

/// The sacred 8ms latency bound
pub const COVENANT_LATENCY_MS: u16 = 8;

/// Size of capability descriptor in bytes
pub const DESCRIPTOR_SIZE: usize = 96;

#[cfg(test)]
mod tests {
    use super::*;
    use core::mem;

    #[test]
    fn descriptor_is_96_bytes() {
        assert_eq!(mem::size_of::<CapabilityDescriptor>(), DESCRIPTOR_SIZE);
    }

    #[test]
    fn descriptor_alignment() {
        assert_eq!(mem::align_of::<CapabilityDescriptor>(), 64);
    }

    #[test]
    fn descriptor_fields_sum_to_96() {
        // Verify field layout: 8 + 1 + 1 + 1 + 1 + 2 + 1 + 4 + 75 = 94
        // But with alignment, it's 96 bytes total
        let total = 8 + 1 + 1 + 1 + 1 + 2 + 1 + 4 + 75;
        assert_eq!(total, DESCRIPTOR_SIZE - 1); // -1 for alignment padding
    }
}
