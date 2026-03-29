//! Video Subtitle Channel - Extract subtitles from videos
//! 
//! Uses yt-dlp (YouTube downloader) to extract subtitles without API keys.
//! Supports YouTube and hundreds of other video platforms.
//! 
//! # Requirements
//! 
/// - yt-dlp must be installed: https://github.com/yt-dlp/yt-dlp

use alloc::string::{String, ToString};
use alloc::vec::Vec;

use super::{CapabilityChannel, ChannelError, Request, RequestKind, Response};
use crate::capability::descriptor::CapabilityDescriptor;

/// Channel for extracting video subtitles
pub struct VideoSubtitleChannel;

impl VideoSubtitleChannel {
    pub fn new() -> Self {
        Self
    }

    pub fn is_available() -> bool {
        std::process::Command::new("yt-dlp")
            .arg("--version")
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
    }

    fn extract_subtitles(url: &str, lang: &str) -> Result<String, ChannelError> {
        // First, list available subtitles
        let list_output = std::process::Command::new("yt-dlp")
            .args([
                "--list-subs",
                "--no-warnings",
                url,
            ])
            .output()
            .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?;

        if !list_output.status.success() {
            return Err(ChannelError::ExecutionFailed(
                String::from_utf8_lossy(&list_output.stderr).to_string()
            ));
        }

        // Check if requested language is available
        let sub_list = String::from_utf8_lossy(&list_output.stdout);
        if !sub_list.contains(lang) {
            // Try auto-generated subtitles
            return Self::extract_auto_subs(url, lang);
        }

        // Download the subtitle
        let output = std::process::Command::new("yt-dlp")
            .args([
                "--skip-download",
                "--write-subs",
                "--sub-langs", lang,
                "--convert-subs", "srt",
                "--no-warnings",
                "-o", "-", // Output to stdout
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

    fn extract_auto_subs(url: &str, lang: &str) -> Result<String, ChannelError> {
        let output = std::process::Command::new("yt-dlp")
            .args([
                "--skip-download",
                "--write-auto-subs",
                "--sub-langs", lang,
                "--convert-subs", "srt",
                "--no-warnings",
                "-o", "-",
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

    /// Extract video metadata (title, duration, etc.)
    fn extract_metadata(url: &str) -> Result<BTreeMap<String, String>, ChannelError> {
        use alloc::collections::BTreeMap;
        
        let output = std::process::Command::new("yt-dlp")
            .args([
                "--dump-json",
                "--no-download",
                "--no-warnings",
                url,
            ])
            .output()
            .map_err(|e| ChannelError::ExecutionFailed(e.to_string()))?;

        if !output.status.success() {
            return Err(ChannelError::ExecutionFailed(
                String::from_utf8_lossy(&output.stderr).to_string()
            ));
        }

        let json_str = String::from_utf8_lossy(&output.stdout);
        let mut metadata = BTreeMap::new();

        // Parse basic fields from JSON (simple extraction)
        for line in json_str.lines() {
            if let Some(title) = extract_json_field(line, "title") {
                metadata.insert("title".to_string(), title);
            }
            if let Some(duration) = extract_json_field(line, "duration") {
                metadata.insert("duration".to_string(), duration);
            }
            if let Some(uploader) = extract_json_field(line, "uploader") {
                metadata.insert("uploader".to_string(), uploader);
            }
        }

        Ok(metadata)
    }

    /// Clean up SRT subtitle format (remove timing info, keep text)
    fn clean_srt(srt: &str) -> String {
        let mut result = String::with_capacity(srt.len() / 2);
        let mut lines = srt.lines().peekable();

        while let Some(line) = lines.next() {
            // Skip sequence numbers (just digits)
            if line.trim().parse::<u32>().is_ok() {
                continue;
            }
            
            // Skip timing lines (contain -->)
            if line.contains("-->") {
                continue;
            }

            // Skip empty lines
            if line.trim().is_empty() {
                continue;
            }

            // This is subtitle text
            result.push_str(line.trim());
            result.push(' ');
        }

        result.trim().to_string()
    }
}

fn extract_json_field(json: &str, field: &str) -> Option<String> {
    let pattern = format!("\"{}\":\"", field);
    if let Some(start) = json.find(&pattern) {
        let after_field = &json[start + pattern.len()..];
        if let Some(end) = after_field.find('"') {
            return Some(after_field[..end].to_string());
        }
    }
    None
}

impl CapabilityChannel for VideoSubtitleChannel {
    fn execute(&self, request: Request) -> Result<Response, ChannelError> {
        if request.kind != RequestKind::GetVideoSubtitles {
            return Err(ChannelError::InvalidRequest(
                "VideoSubtitleChannel only handles GetVideoSubtitles".to_string()
            ));
        }

        let url = &request.target;
        let lang = request.params.get("lang").map(|s| s.as_str()).unwrap_or("en");
        let raw = request.params.get("raw").map(|s| s == "true").unwrap_or(false);

        let srt_content = Self::extract_subtitles(url, lang)?;
        
        let body = if raw {
            srt_content
        } else {
            Self::clean_srt(&srt_content)
        };

        let mut response = Response::success(body);
        response.metadata.insert("source".to_string(), url.to_string());
        response.metadata.insert("language".to_string(), lang.to_string());

        // Try to add metadata
        if let Ok(meta) = Self::extract_metadata(url) {
            for (k, v) in meta {
                response.metadata.insert(k, v);
            }
        }

        Ok(response)
    }

    fn descriptor(&self) -> CapabilityDescriptor {
        let mut desc = CapabilityDescriptor::local([0; 8]);
        desc.can_video = 1;
        desc.latency_estimate_ms = 1;
        desc
    }

    fn is_available() -> bool
    where
        Self: Sized,
    {
        Self::is_available()
    }
}

impl Default for VideoSubtitleChannel {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clean_srt_removes_timing() {
        let srt = r#"1
00:00:01,000 --> 00:00:04,000
Hello world

2
00:00:05,000 --> 00:00:08,000
Second line
"#;
        
        let cleaned = VideoSubtitleChannel::clean_srt(srt);
        assert!(cleaned.contains("Hello world"));
        assert!(cleaned.contains("Second line"));
        assert!(!cleaned.contains("00:00"));
        assert!(!cleaned.contains("-->"));
    }

    #[test]
    fn extract_json_field_works() {
        let json = r#"{"title":"Test Video","duration":"123"}"#;
        assert_eq!(
            extract_json_field(json, "title"),
            Some("Test Video".to_string())
        );
        assert_eq!(
            extract_json_field(json, "duration"),
            Some("123".to_string())
        );
    }
}
