//! Web Reader Channel - Local web content fetching
//! 
//! Uses system curl or wget binaries. No API keys required.
//! Falls back to simple HTTP client if neither is available.

use alloc::string::{String, ToString};
use alloc::vec::Vec;

use super::{CapabilityChannel, ChannelError, Request, RequestKind, Response};
use crate::capability::descriptor::CapabilityDescriptor;

/// Channel for reading web content
pub struct WebReaderChannel {
    backend: WebBackend,
}

#[derive(Debug, Clone, Copy)]
enum WebBackend {
    Curl,
    Wget,
    Ureq, // Fallback pure Rust
}

impl WebReaderChannel {
    pub fn new() -> Self {
        let backend = if Self::curl_available() {
            WebBackend::Curl
        } else if Self::wget_available() {
            WebBackend::Wget
        } else {
            WebBackend::Ureq
        };
        
        Self { backend }
    }

    fn curl_available() -> bool {
        std::process::Command::new("curl")
            .arg("--version")
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
    }

    fn wget_available() -> bool {
        std::process::Command::new("wget")
            .arg("--version")
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
    }

    fn fetch_with_curl(url: &str) -> Result<String, ChannelError> {
        let output = std::process::Command::new("curl")
            .args([
                "-s",           // Silent
                "-L",           // Follow redirects
                "--max-time", "30",
                "-A", "Rosetta-Bridge/1.0 (Sovereign Agent)",
                url,
            ])
            .output()
            .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?;

        if output.status.success() {
            String::from_utf8(output.stdout)
                .map_err(|e| ChannelError::ExecutionFailed(format!("Invalid UTF-8: {}", e)))
        } else {
            Err(ChannelError::ExecutionFailed(
                String::from_utf8_lossy(&output.stderr).to_string()
            ))
        }
    }

    fn fetch_with_wget(url: &str) -> Result<String, ChannelError> {
        let output = std::process::Command::new("wget")
            .args([
                "-q",           // Quiet
                "-O", "-",      // Output to stdout
                "--timeout=30",
                "--user-agent=Rosetta-Bridge/1.0 (Sovereign Agent)",
                url,
            ])
            .output()
            .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?;

        if output.status.success() {
            String::from_utf8(output.stdout)
                .map_err(|e| ChannelError::ExecutionFailed(format!("Invalid UTF-8: {}", e)))
        } else {
            Err(ChannelError::ExecutionFailed(
                String::from_utf8_lossy(&output.stderr).to_string()
            ))
        }
    }

    /// Extract main content using readability-style heuristics
    fn extract_content(html: &str) -> String {
        // Simple content extraction - strip tags, preserve structure
        let mut result = String::with_capacity(html.len() / 2);
        let mut in_tag = false;
        let mut in_script = false;
        let mut prev_was_space = true;

        for c in html.chars() {
            if in_script {
                if c == '<' {
                    in_script = false;
                }
                continue;
            }

            match c {
                '<' => {
                    in_tag = true;
                    // Check for script/style tags
                    if html[html.len().saturating_sub(result.len())..].starts_with("script")
                        || html[html.len().saturating_sub(result.len())..].starts_with("style") {
                        in_script = true;
                    }
                }
                '>' => {
                    in_tag = false;
                    if !prev_was_space {
                        result.push(' ');
                        prev_was_space = true;
                    }
                }
                _ if !in_tag && !in_script => {
                    if c.is_whitespace() {
                        if !prev_was_space {
                            result.push(' ');
                            prev_was_space = true;
                        }
                    } else {
                        result.push(c);
                        prev_was_space = false;
                    }
                }
                _ => {}
            }
        }

        result.trim().to_string()
    }
}

impl CapabilityChannel for WebReaderChannel {
    fn execute(&self, request: Request) -> Result<Response, ChannelError> {
        if request.kind != RequestKind::ReadWeb {
            return Err(ChannelError::InvalidRequest(
                "WebReaderChannel only handles ReadWeb requests".to_string()
            ));
        }

        let url = &request.target;
        
        // Validate URL scheme
        if !url.starts_with("http://") && !url.starts_with("https://") {
            return Err(ChannelError::InvalidRequest(
                "URL must use http or https scheme".to_string()
            ));
        }

        let html = match self.backend {
            WebBackend::Curl => Self::fetch_with_curl(url)?,
            WebBackend::Wget => Self::fetch_with_wget(url)?,
            WebBackend::Ureq => {
                // Fallback to blocking HTTP request
                ureq::get(url)
                    .set("User-Agent", "Rosetta-Bridge/1.0 (Sovereign Agent)")
                    .call()
                    .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?
                    .into_string()
                    .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?
            }
        };

        let content = Self::extract_content(&html);
        
        let mut response = Response::success(content);
        response.metadata.insert("source".to_string(), url.to_string());
        response.metadata.insert("backend".to_string(), format!("{:?}", self.backend));
        
        Ok(response)
    }

    fn descriptor(&self) -> CapabilityDescriptor {
        let mut desc = CapabilityDescriptor::local([0; 8]);
        desc.can_read_web = 1;
        desc.latency_estimate_ms = 1; // Local channel
        desc
    }

    fn is_available() -> bool
    where
        Self: Sized,
    {
        Self::curl_available() || Self::wget_available() || cfg!(feature = "ureq")
    }
}

impl Default for WebReaderChannel {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn extract_content_strips_tags() {
        let html = "<html><body><p>Hello World</p></body></html>";
        let content = WebReaderChannel::extract_content(html);
        assert!(content.contains("Hello World"));
        assert!(!content.contains("<html>"));
    }

    #[test]
    fn extract_content_handles_scripts() {
        let html = "<p>Text</p><script>alert('x')</script><p>More</p>";
        let content = WebReaderChannel::extract_content(html);
        assert!(!content.contains("alert"));
        assert!(content.contains("Text"));
        assert!(content.contains("More"));
    }
}
