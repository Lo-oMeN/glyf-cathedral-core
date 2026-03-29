//! Capability Channels - The wire protocol implementation
//! 
//! Channels are the concrete implementations of capabilities.
//! Each channel represents one way to fulfill a request.

use alloc::string::String;
use alloc::vec::Vec;
use alloc::collections::BTreeMap;

/// A request to be executed by a capability channel
#[derive(Debug, Clone)]
pub struct Request {
    pub kind: RequestKind,
    pub target: String,
    pub params: BTreeMap<String, String>,
}

impl Request {
    pub fn new(kind: RequestKind, target: impl Into<String>) -> Self {
        Self {
            kind,
            target: target.into(),
            params: BTreeMap::new(),
        }
    }

    pub fn with_param(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.params.insert(key.into(), value.into());
        self
    }
}

/// Types of requests that can be made
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RequestKind {
    ReadWeb,
    Search,
    GetVideoSubtitles,
    ReadSocial,
}

/// Response from a capability channel
#[derive(Debug, Clone)]
pub struct Response {
    pub status: ResponseStatus,
    pub body: String,
    pub metadata: BTreeMap<String, String>,
}

impl Response {
    pub fn success(body: impl Into<String>) -> Self {
        Self {
            status: ResponseStatus::Success,
            body: body.into(),
            metadata: BTreeMap::new(),
        }
    }

    pub fn error(message: impl Into<String>) -> Self {
        Self {
            status: ResponseStatus::Error,
            body: message.into(),
            metadata: BTreeMap::new(),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResponseStatus {
    Success,
    Error,
    Timeout,
    RateLimited,
}

/// Errors that can occur when executing a channel
#[derive(Debug, Clone)]
pub enum ChannelError {
    NotAvailable,
    ExecutionFailed(String),
    Timeout,
    RemoteNotImplemented,
    InvalidRequest(String),
}

impl core::fmt::Display for ChannelError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            ChannelError::NotAvailable => write!(f, "Channel not available"),
            ChannelError::ExecutionFailed(msg) => write!(f, "Execution failed: {}", msg),
            ChannelError::Timeout => write!(f, "Request timed out"),
            ChannelError::RemoteNotImplemented => write!(f, "Remote execution not implemented"),
            ChannelError::InvalidRequest(msg) => write!(f, "Invalid request: {}", msg),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for ChannelError {}

/// Core trait for all capability channels
/// 
/// # Contract
/// 
/// - `execute` must complete within 8ms for cached/local operations
/// - `descriptor` must return accurate capability information
/// - Channels must be thread-safe (Send + Sync)
pub trait CapabilityChannel: Send + Sync {
    /// Execute a request and return a response
    /// 
    /// # Errors
    /// 
    /// Returns `ChannelError::NotAvailable` if the channel's binary/tool
    /// is not installed on the system.
    fn execute(&self, request: Request) -> Result<Response, ChannelError>;

    /// Get the capability descriptor for this channel
    fn descriptor(&self) -> super::descriptor::CapabilityDescriptor;

    /// Check if this channel is available on the current system
    fn is_available() -> bool
    where
        Self: Sized;
}

// Export channel implementations
#[cfg(feature = "std")]
pub mod fellowship_bridge;
#[cfg(feature = "std")]
pub mod search;
#[cfg(feature = "std")]
pub mod social_read;
#[cfg(feature = "std")]
pub mod video_subtitles;
#[cfg(feature = "std")]
pub mod web_reader;

#[cfg(feature = "std")]
pub use fellowship_bridge::FellowshipBridgeChannel;
#[cfg(feature = "std")]
pub use search::SearchChannel;
#[cfg(feature = "std")]
pub use social_read::SocialReadChannel;
#[cfg(feature = "std")]
pub use video_subtitles::VideoSubtitleChannel;
#[cfg(feature = "std")]
pub use web_reader::WebReaderChannel;
