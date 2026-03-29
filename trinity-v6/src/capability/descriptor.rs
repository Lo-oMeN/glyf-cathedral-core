//! Capability Descriptor - 96-byte fellowship beacon
//! 
//! Each node broadcasts its capabilities via this compact structure.
//! Designed for zero-copy serialization and lattice-state alignment.

use core::fmt;

/// 96-byte capability descriptor
/// 
/// # Memory Layout
/// 
/// | Offset | Size | Field                |
/// |--------|------|---------------------|
/// | 0      | 8    | node_id             |
/// | 8      | 1    | can_read_web        |
/// | 9      | 1    | can_search          |
/// | 10     | 1    | can_video           |
/// | 11     | 1    | can_social_read     |
/// | 12     | 2    | latency_estimate_ms |
/// | 14     | 1    | reliability_score   |
/// | 15     | 4    | last_seen           |
/// | 19     | 77   | _padding (align 64) |
#[repr(C, align(64))]
pub struct CapabilityDescriptor {
    pub node_id: [u8; 8],
    pub can_read_web: u8,      // 0 or 1
    pub can_search: u8,
    pub can_video: u8,
    pub can_social_read: u8,
    pub latency_estimate_ms: u16,
    pub reliability_score: u8, // 0-255
    pub last_seen: u32,        // timestamp
    _pad: [u8; 77],            // Padding to reach 96 bytes with alignment
}

impl CapabilityDescriptor {
    /// Create a new descriptor with zeroed capabilities
    pub const fn new(node_id: [u8; 8]) -> Self {
        Self {
            node_id,
            can_read_web: 0,
            can_search: 0,
            can_video: 0,
            can_social_read: 0,
            latency_estimate_ms: 0,
            reliability_score: 0,
            last_seen: 0,
            _pad: [0; 77],
        }
    }

    /// Create a descriptor representing local capabilities
    pub const fn local(node_id: [u8; 8]) -> Self {
        Self {
            node_id,
            can_read_web: 1,
            can_search: 1,
            can_video: 1,
            can_social_read: 1,
            latency_estimate_ms: 1,  // Local is always 1ms
            reliability_score: 255,   // Maximum reliability
            last_seen: 0,
            _pad: [0; 77],
        }
    }

    /// Check if this descriptor satisfies a capability need
    pub fn satisfies(&self, need: CapabilityType) -> bool {
        match need {
            CapabilityType::ReadWeb => self.can_read_web != 0,
            CapabilityType::Search => self.can_search != 0,
            CapabilityType::Video => self.can_video != 0,
            CapabilityType::SocialRead => self.can_social_read != 0,
        }
    }

    /// Update the last_seen timestamp
    pub fn touch(&mut self, timestamp: u32) {
        self.last_seen = timestamp;
    }

    /// Serialize to bytes (zero-copy safe)
    pub fn as_bytes(&self) -> &[u8; 96] {
        // SAFETY: CapabilityDescriptor is repr(C) with fixed size
        unsafe { &*(self as *const _ as *const [u8; 96]) }
    }

    /// Deserialize from bytes
    pub fn from_bytes(bytes: &[u8; 96]) -> &Self {
        // SAFETY: CapabilityDescriptor is repr(C) with fixed size
        unsafe { &*(bytes.as_ptr() as *const Self) }
    }

    /// Calculate total capability score (for ranking)
    pub fn capability_count(&self) -> u8 {
        self.can_read_web.saturating_add(self.can_search)
            .saturating_add(self.can_video)
            .saturating_add(self.can_social_read)
    }
}

impl fmt::Debug for CapabilityDescriptor {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("CapabilityDescriptor")
            .field("node_id", &hex::encode(&self.node_id))
            .field("can_read_web", &(self.can_read_web != 0))
            .field("can_search", &(self.can_search != 0))
            .field("can_video", &(self.can_video != 0))
            .field("can_social_read", &(self.can_social_read != 0))
            .field("latency_ms", &self.latency_estimate_ms)
            .field("reliability", &self.reliability_score)
            .field("last_seen", &self.last_seen)
            .finish()
    }
}

impl Clone for CapabilityDescriptor {
    fn clone(&self) -> Self {
        Self {
            node_id: self.node_id,
            can_read_web: self.can_read_web,
            can_search: self.can_search,
            can_video: self.can_video,
            can_social_read: self.can_social_read,
            latency_estimate_ms: self.latency_estimate_ms,
            reliability_score: self.reliability_score,
            last_seen: self.last_seen,
            _pad: self._pad,
        }
    }
}

impl Copy for CapabilityDescriptor {}

/// Types of capabilities that can be requested
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CapabilityType {
    ReadWeb,
    Search,
    Video,
    SocialRead,
}

/// Simple hex encoding for no_std environments
mod hex {
    pub fn encode(bytes: &[u8]) -> heapless::String<16> {
        const HEX_CHARS: &[u8] = b"0123456789abcdef";
        let mut result = heapless::String::new();
        
        for &byte in bytes {
            let high = HEX_CHARS[(byte >> 4) as usize] as char;
            let low = HEX_CHARS[(byte & 0xf) as usize] as char;
            let _ = result.push(high);
            let _ = result.push(low);
        }
        
        result
    }
}

// Placeholder for heapless::String when heapless isn't available
// In a real implementation, you'd use the heapless crate
mod heapless {
    pub struct String<const N: usize> {
        buf: [u8; N],
        len: usize,
    }

    impl<const N: usize> String<N> {
        pub const fn new() -> Self {
            Self {
                buf: [0; N],
                len: 0,
            }
        }

        pub fn push(&mut self, c: char) -> Result<(), ()> {
            if self.len >= N {
                return Err(());
            }
            self.buf[self.len] = c as u8;
            self.len += 1;
            Ok(())
        }
    }

    impl<const N: usize> core::fmt::Debug for String<N> {
        fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
            write!(f, "{}", core::str::from_utf8(&self.buf[..self.len]).unwrap_or("???"))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::mem;

    #[test]
    fn size_is_exactly_96() {
        assert_eq!(mem::size_of::<CapabilityDescriptor>(), 96);
    }

    #[test]
    fn alignment_is_64() {
        assert_eq!(mem::align_of::<CapabilityDescriptor>(), 64);
    }

    #[test]
    fn satisfies_works() {
        let mut desc = CapabilityDescriptor::new([1, 2, 3, 4, 5, 6, 7, 8]);
        assert!(!desc.satisfies(CapabilityType::ReadWeb));
        
        desc.can_read_web = 1;
        assert!(desc.satisfies(CapabilityType::ReadWeb));
    }

    #[test]
    fn local_has_all_capabilities() {
        let desc = CapabilityDescriptor::local([0; 8]);
        assert!(desc.satisfies(CapabilityType::ReadWeb));
        assert!(desc.satisfies(CapabilityType::Search));
        assert!(desc.satisfies(CapabilityType::Video));
        assert!(desc.satisfies(CapabilityType::SocialRead));
    }

    #[test]
    fn bytes_roundtrip() {
        let desc = CapabilityDescriptor::local([0xde, 0xad, 0xbe, 0xef, 0, 0, 0, 1]);
        let bytes = desc.as_bytes();
        let restored = CapabilityDescriptor::from_bytes(bytes);
        
        assert_eq!(restored.node_id, desc.node_id);
        assert_eq!(restored.can_read_web, desc.can_read_web);
    }
}
