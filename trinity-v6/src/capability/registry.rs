//! Capability Registry - Fellowship-based discovery
//! 
//! The registry maintains a view of capabilities in the fellowship.
//! Local channels are checked first (1ms latency), then fellow nodes.
//! 
//! # Discovery Strategy
//! 
//! 1. Local binary available? Use it (1ms)
//! 2. Fellow node has capability? Request via lattice (2-8ms)
//! 3. No fellowship match? Fail closed (sovereign default)

use alloc::vec::Vec;
use core::time::Duration;

use super::descriptor::{CapabilityDescriptor, CapabilityType};
use super::channels::{CapabilityChannel, Request, Response, ChannelError};

/// What capability do we need?
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CapabilityNeed {
    ReadWeb,
    Search,
    Video,
    SocialRead,
}

impl CapabilityNeed {
    fn to_type(&self) -> CapabilityType {
        match self {
            CapabilityNeed::ReadWeb => CapabilityType::ReadWeb,
            CapabilityNeed::Search => CapabilityType::Search,
            CapabilityNeed::Video => CapabilityType::Video,
            CapabilityNeed::SocialRead => CapabilityType::SocialRead,
        }
    }
}

/// A fellow node's capability offering
pub struct FellowCapability {
    pub descriptor: CapabilityDescriptor,
    channel: Option<alloc::boxed::Box<dyn CapabilityChannel>>,
    is_local: bool,
}

impl FellowCapability {
    /// Create from a remote descriptor (fellowship node)
    pub fn from_descriptor(descriptor: CapabilityDescriptor) -> Self {
        Self {
            descriptor,
            channel: None,
            is_local: false,
        }
    }

    /// Create from a local channel
    pub fn from_local(
        descriptor: CapabilityDescriptor,
        channel: alloc::boxed::Box<dyn CapabilityChannel>,
    ) -> Self {
        Self {
            descriptor,
            channel: Some(channel),
            is_local: true,
        }
    }

    /// Execute a request on this capability
    pub fn execute(&self, request: Request) -> Result<Response, ChannelError> {
        if let Some(ref channel) = self.channel {
            channel.execute(request)
        } else {
            // Remote execution - would go through lattice protocol
            Err(ChannelError::RemoteNotImplemented)
        }
    }

    /// Check if this capability can satisfy a need
    pub fn satisfies(&self, need: CapabilityNeed) -> bool {
        self.descriptor.satisfies(need.to_type())
    }

    /// Get latency estimate for this capability
    pub fn latency_ms(&self) -> u16 {
        self.descriptor.latency_estimate_ms
    }
}

/// Registry of all known capabilities in the fellowship
pub struct CapabilityRegistry {
    fellows: Vec<FellowCapability>,
    local_node_id: [u8; 8],
}

impl CapabilityRegistry {
    /// Create a new empty registry
    pub fn new(local_node_id: [u8; 8]) -> Self {
        Self {
            fellows: Vec::new(),
            local_node_id,
        }
    }

    /// Register a local capability channel
    pub fn register_local(&mut self, fellow: FellowCapability) {
        self.fellows.push(fellow);
    }

    /// Register a remote fellow's capabilities
    pub fn register_fellow(&mut self, descriptor: CapabilityDescriptor) {
        // Don't register ourselves
        if descriptor.node_id == self.local_node_id {
            return;
        }
        self.fellows.push(FellowCapability::from_descriptor(descriptor));
    }

    /// Remove stale entries (last_seen too old)
    pub fn prune_stale(&mut self, max_age_secs: u32, current_time: u32) {
        self.fellows.retain(|f| {
            let age = current_time.saturating_sub(f.descriptor.last_seen);
            f.is_local || age < max_age_secs
        });
    }

    /// Query for a capability, returning the lowest-latency match
    /// 
    /// # The 8ms Covenant
    /// 
    /// This method filters to only return capabilities with latency < 8ms.
    /// Local channels always satisfy this (they report 1ms).
    pub fn query(&self, need: CapabilityNeed) -> Option<&FellowCapability> {
        let max_latency = super::COVENANT_LATENCY_MS;

        self.fellows
            .iter()
            .filter(|f| f.satisfies(need))
            .filter(|f| f.latency_ms() < max_latency)
            .min_by_key(|f| f.latency_ms())
    }

    /// Query with relaxed latency constraints (for fallback)
    pub fn query_any_latency(&self, need: CapabilityNeed) -> Option<&FellowCapability> {
        self.fellows
            .iter()
            .filter(|f| f.satisfies(need))
            .min_by_key(|f| f.latency_ms())
    }

    /// Get all capabilities sorted by latency
    pub fn ranked_by_latency(&self, need: CapabilityNeed) -> Vec<&FellowCapability> {
        let mut matches: Vec<_> = self.fellows
            .iter()
            .filter(|f| f.satisfies(need))
            .collect();
        
        matches.sort_by_key(|f| f.latency_ms());
        matches
    }

    /// Get count of registered fellows (excluding local)
    pub fn fellow_count(&self) -> usize {
        self.fellows.iter().filter(|f| !f.is_local).count()
    }

    /// Get count of local channels
    pub fn local_count(&self) -> usize {
        self.fellows.iter().filter(|f| f.is_local).count()
    }

    /// Discover local capabilities by checking for available binaries
    #[cfg(feature = "std")]
    pub fn discover_local(&mut self) {
        use super::channels::{WebReaderChannel, SearchChannel, VideoSubtitleChannel};

        // Check for curl/wget
        if WebReaderChannel::is_available() {
            let desc = CapabilityDescriptor::local(self.local_node_id);
            self.register_local(FellowCapability::from_local(
                desc,
                alloc::boxed::Box::new(WebReaderChannel::new()),
            ));
        }

        // Check for searx/searxng
        if SearchChannel::is_available() {
            let desc = CapabilityDescriptor::local(self.local_node_id);
            // Update descriptor for search specifically
            self.register_local(FellowCapability::from_local(
                desc,
                alloc::boxed::Box::new(SearchChannel::new()),
            ));
        }

        // Check for yt-dlp
        if VideoSubtitleChannel::is_available() {
            let desc = CapabilityDescriptor::local(self.local_node_id);
            self.register_local(FellowCapability::from_local(
                desc,
                alloc::boxed::Box::new(VideoSubtitleChannel::new()),
            ));
        }
    }

    /// Update latency estimates based on recent measurements
    pub fn update_latency(&mut self, node_id: [u8; 8], latency_ms: u16) {
        for fellow in &mut self.fellows {
            if fellow.descriptor.node_id == node_id {
                // Exponential moving average: new = 0.7 * old + 0.3 * measured
                let old = fellow.descriptor.latency_estimate_ms as u32;
                let new = latency_ms as u32;
                let smoothed = (old * 7 + new * 3) / 10;
                fellow.descriptor.latency_estimate_ms = smoothed as u16;
            }
        }
    }
}

impl Default for CapabilityRegistry {
    fn default() -> Self {
        Self::new([0; 8])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_descriptor(node_id: u8, latency: u16) -> CapabilityDescriptor {
        CapabilityDescriptor {
            node_id: [node_id, 0, 0, 0, 0, 0, 0, 0],
            can_read_web: 1,
            can_search: 0,
            can_video: 0,
            can_social_read: 0,
            latency_estimate_ms: latency,
            reliability_score: 128,
            last_seen: 1000,
            _pad: [0; 77],
        }
    }

    #[test]
    fn query_returns_lowest_latency() {
        let mut registry = CapabilityRegistry::new([0xff; 8]);
        
        registry.register_fellow(test_descriptor(1, 5));
        registry.register_fellow(test_descriptor(2, 3));
        registry.register_fellow(test_descriptor(3, 7));
        
        let result = registry.query(CapabilityNeed::ReadWeb);
        assert!(result.is_some());
        assert_eq!(result.unwrap().descriptor.node_id[0], 2); // Lowest latency
    }

    #[test]
    fn query_respects_8ms_covenant() {
        let mut registry = CapabilityRegistry::new([0xff; 8]);
        
        registry.register_fellow(test_descriptor(1, 5));
        registry.register_fellow(test_descriptor(2, 10)); // Too slow
        
        let result = registry.query(CapabilityNeed::ReadWeb);
        assert!(result.is_some());
        assert_eq!(result.unwrap().descriptor.node_id[0], 1);
        
        // Remove the fast one
        registry.fellows.retain(|f| f.descriptor.node_id[0] != 1);
        
        // Now should return None (covenant violated)
        let result = registry.query(CapabilityNeed::ReadWeb);
        assert!(result.is_none());
    }

    #[test]
    fn prunes_stale_entries() {
        let mut registry = CapabilityRegistry::new([0xff; 8]);
        
        let mut old = test_descriptor(1, 5);
        old.last_seen = 0;
        
        registry.register_fellow(old);
        assert_eq!(registry.fellow_count(), 1);
        
        registry.prune_stale(100, 200);
        assert_eq!(registry.fellow_count(), 0);
    }
}
