//! Fellowship Protocol — GLYF Cathedral Context Transfer v0.7.2
//! 
//! Rosetta-Bridge implementation: HTTP endpoint for ℭ_T (Context Transfer Package)
//! Wire format: 148-byte binary protocol with RS(128,96) protection
//! Target latency: <8ms pulse response
//!
//! Protocol Version: 0x07 (v0.7.2)
//! Header Magic: 0xDEAD_BEEF

#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "std")]
extern crate std;

#[cfg(feature = "std")]
use std::time::Instant;

// =============================================================================
// CONSTANTS
// =============================================================================

/// Header magic: 0xDEAD_BEEF (big-endian wire format)
pub const HEADER_MAGIC: [u8; 4] = [0xDE, 0xAD, 0xBE, 0xEF];

/// Protocol version 0x07 (v0.7.2)
pub const PROTOCOL_VERSION: u8 = 0x07;

/// Payload length: 96 bytes (LatticeState)
pub const PAYLOAD_LEN: u16 = 96;

/// Parity length: 32 bytes (RS redundancy)
pub const PARITY_LEN: u8 = 32;

/// Total package size: 148 bytes
pub const PACKAGE_SIZE: usize = 148;

/// RS-encoded payload size: 128 bytes (96 data + 32 parity)
pub const RS_PAYLOAD_SIZE: usize = 128;

/// Enablement flags bit positions
/// bit 0: morphogen_breath
/// bit 1: sovereign_mode
pub const FLAG_MORPHOGEN_BREATH: u8 = 0x01;
pub const FLAG_SOVEREIGN_MODE: u8 = 0x02;

// =============================================================================
// CONTEXT TRANSFER PACKAGE (148-byte wire format)
// =============================================================================

/// ℭ_T — The Context Transfer Package
/// 
/// Wire format (148 bytes total):
/// ```
/// Offset  Size  Field
/// 0x00    4     header_magic      [0xDE, 0xAD, 0xBE, 0xEF]
/// 0x04    1     protocol_version  0x07
/// 0x05    2     payload_len       96
/// 0x07    1     parity_len        32
/// 0x08    1     enablement_flags  bit flags
/// 0x09    8     reserved          [0; 8]
/// 0x11    128   payload_rs        RS(128,96) encoded LatticeState
/// 0x91    4     checksum_pkg      CRC32 of bytes 0-143
/// ```
#[repr(C)]
#[derive(Clone, Copy, Debug)]
pub struct ContextTransferPackage {
    /// Bytes 0-3: Header magic (0xDEAD_BEEF)
    pub header_magic: [u8; 4],
    
    /// Byte 4: Protocol version (0x07)
    pub protocol_version: u8,
    
    /// Bytes 5-6: Payload length (96)
    pub payload_len: u16,
    
    /// Byte 7: Parity length (32)
    pub parity_len: u8,
    
    /// Byte 8: Enablement flags
    /// bit 0: morphogen_breath
    /// bit 1: sovereign_mode
    pub enablement_flags: u8,
    
    /// Bytes 9-16: Reserved (alignment)
    pub reserved: [u8; 8],
    
    /// Bytes 17-144: RS-encoded payload (128 bytes)
    /// Contains: 96 bytes LatticeState + 32 bytes RS parity
    pub payload_rs: [u8; 128],
    
    /// Bytes 144-147: CRC32 checksum of package
    pub checksum_pkg: u32,
}

/// Compile-time size verification
const _: () = assert!(core::mem::size_of::<ContextTransferPackage>() == 148);

impl ContextTransferPackage {
    /// Create new package with specified payload and flags
    pub fn new(payload: &[u8; 96], flags: u8) -> Self {
        let mut pkg = ContextTransferPackage {
            header_magic: HEADER_MAGIC,
            protocol_version: PROTOCOL_VERSION,
            payload_len: PAYLOAD_LEN,
            parity_len: PARITY_LEN,
            enablement_flags: flags,
            reserved: [0; 8],
            payload_rs: [0; 128],
            checksum_pkg: 0,
        };
        
        // Copy payload to first 96 bytes
        pkg.payload_rs[0..96].copy_from_slice(payload);
        
        // Compute RS parity
        pkg.compute_rs_parity();
        
        // Compute and set checksum
        pkg.checksum_pkg = pkg.compute_checksum();
        
        pkg
    }
    
    /// Compute CRC32 checksum of package (excluding checksum field at offset 144)
    fn compute_checksum(&self) -> u32 {
        let wire = self.to_bytes();
        crc32_fellowship(&wire[0..144])
    }
    
    /// Compute checksum without using stored value
    fn compute_checksum_without_stored(&self) -> u32 {
        let mut wire = self.to_bytes();
        // Zero out checksum field for computation
        wire[144] = 0;
        wire[145] = 0;
        wire[146] = 0;
        wire[147] = 0;
        crc32_fellowship(&wire[0..144])
    }
    
    /// Compute RS parity for payload (bytes 96-127)
    fn compute_rs_parity(&mut self) {
        // Simplified RS parity: XOR-based for demonstration
        // Real implementation would use Berlekamp-Massey
        for i in 0..32 {
            let mut parity = 0u8;
            for (j, &byte) in self.payload_rs[0..96].iter().enumerate() {
                parity ^= gf_mul_fellowship(byte, GF_EXP_FELLOWSHIP[(i * j) % 255]);
            }
            self.payload_rs[96 + i] = parity;
        }
    }
    
    /// Verify RS codeword
    fn verify_rs(&self) -> bool {
        let mut computed = [0u8; 128];
        computed[0..96].copy_from_slice(&self.payload_rs[0..96]);
        
        for i in 0..32 {
            let mut parity = 0u8;
            for (j, &byte) in self.payload_rs[0..96].iter().enumerate() {
                parity ^= gf_mul_fellowship(byte, GF_EXP_FELLOWSHIP[(i * j) % 255]);
            }
            computed[96 + i] = parity;
        }
        
        // Allow up to 32 errors
        let errors: usize = self.payload_rs.iter().zip(computed.iter())
            .filter(|(a, b)| a != b)
            .count();
        
        errors <= 32
    }
    
    /// Serialize to wire format (148 bytes)
    pub fn to_bytes(&self) -> [u8; 148] {
        let mut bytes = [0u8; 148];
        
        // Header magic (4 bytes)
        bytes[0..4].copy_from_slice(&self.header_magic);
        
        // Protocol version (1 byte)
        bytes[4] = self.protocol_version;
        
        // Payload length (2 bytes, little-endian)
        bytes[5..7].copy_from_slice(&self.payload_len.to_le_bytes());
        
        // Parity length (1 byte)
        bytes[7] = self.parity_len;
        
        // Enablement flags (1 byte)
        bytes[8] = self.enablement_flags;
        
        // Reserved (8 bytes)
        bytes[9..17].copy_from_slice(&self.reserved);
        
        // Payload RS (128 bytes)
        bytes[17..145].copy_from_slice(&self.payload_rs);
        
        // Checksum (4 bytes, little-endian)
        bytes[145..149].copy_from_slice(&self.checksum_pkg.to_le_bytes());
        
        bytes
    }
    
    /// Deserialize from wire format
    pub fn from_bytes(bytes: &[u8; 148]) -> Self {
        let mut payload_rs = [0u8; 128];
        payload_rs.copy_from_slice(&bytes[17..145]);
        
        ContextTransferPackage {
            header_magic: [bytes[0], bytes[1], bytes[2], bytes[3]],
            protocol_version: bytes[4],
            payload_len: u16::from_le_bytes([bytes[5], bytes[6]]),
            parity_len: bytes[7],
            enablement_flags: bytes[8],
            reserved: {
                let mut r = [0u8; 8];
                r.copy_from_slice(&bytes[9..17]);
                r
            },
            payload_rs,
            checksum_pkg: u32::from_le_bytes([bytes[145], bytes[146], bytes[147], bytes[148]]),
        }
    }
    
    /// Extract LatticeState payload (first 96 bytes of payload_rs)
    pub fn extract_payload(&self) -> [u8; 96] {
        let mut payload = [0u8; 96];
        payload.copy_from_slice(&self.payload_rs[0..96]);
        payload
    }
}

// =============================================================================
// PULSE RESPONSE
// =============================================================================

/// Response from fellowship pulse handler
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct PulseResponse {
    /// Whether the pulse was acknowledged
    pub acknowledged: bool,
    /// Latency in microseconds
    pub latency_us: u64,
    /// Current morphogen phase
    pub morphogen_phase: u8,
    /// Persistent thread state: -1 (terminated), 0 (pending), 1 (active)
    pub persistent_thread: i8,
}

impl PulseResponse {
    /// Create a new pulse response
    pub fn new(acknowledged: bool, latency_us: u64, morphogen_phase: u8, persistent_thread: i8) -> Self {
        PulseResponse {
            acknowledged,
            latency_us,
            morphogen_phase,
            persistent_thread,
        }
    }
}

// =============================================================================
// ERROR TYPES
// =============================================================================

/// Fellowship protocol errors
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum FellowshipError {
    /// Invalid header magic (expected 0xDEAD_BEEF)
    InvalidMagic,
    /// Protocol version mismatch (expected 0x07)
    VersionMismatch,
    /// Invalid payload length
    InvalidPayloadLen,
    /// Invalid parity length
    InvalidParityLen,
    /// Package checksum mismatch
    ChecksumMismatch,
    /// Reed-Solomon decode failed
    RSDecodeFailed,
    /// Base64 decode error
    Base64Error,
    /// JSON parse error
    JsonError,
    /// Invalid package size
    InvalidPackageSize,
}

impl core::fmt::Display for FellowshipError {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            FellowshipError::InvalidMagic => write!(f, "Invalid header magic (expected 0xDEAD_BEEF)"),
            FellowshipError::VersionMismatch => write!(f, "Protocol version mismatch (expected 0x07)"),
            FellowshipError::InvalidPayloadLen => write!(f, "Invalid payload length (expected 96)"),
            FellowshipError::InvalidParityLen => write!(f, "Invalid parity length (expected 32)"),
            FellowshipError::ChecksumMismatch => write!(f, "Package checksum mismatch"),
            FellowshipError::RSDecodeFailed => write!(f, "Reed-Solomon decode failed"),
            FellowshipError::Base64Error => write!(f, "Base64 decode error"),
            FellowshipError::JsonError => write!(f, "JSON parse error"),
            FellowshipError::InvalidPackageSize => write!(f, "Invalid package size (expected 148 bytes)"),
        }
    }
}

#[cfg(feature = "std")]
impl std::error::Error for FellowshipError {}

// =============================================================================
// FELLOWSHIP PULSE HANDLER
// =============================================================================

/// Main fellowship pulse handler
/// 
/// Verifies:
/// - header_magic == 0xDEAD_BEEF
/// - protocol_version == 0x07
/// - checksum validity
/// 
/// Returns PulseResponse with acknowledgment and metadata
#[cfg(feature = "std")]
pub fn fellowship_pulse(package: &ContextTransferPackage) -> Result<PulseResponse, FellowshipError> {
    let start = Instant::now();
    
    // Verify header magic
    if package.header_magic != HEADER_MAGIC {
        return Err(FellowshipError::InvalidMagic);
    }
    
    // Verify protocol version
    if package.protocol_version != PROTOCOL_VERSION {
        return Err(FellowshipError::VersionMismatch);
    }
    
    // Verify checksum
    let computed_checksum = package.compute_checksum_without_stored();
    if computed_checksum != package.checksum_pkg {
        return Err(FellowshipError::ChecksumMismatch);
    }
    
    // Extract payload (first 96 bytes of payload_rs)
    let _payload = package.extract_payload();
    
    // Calculate latency
    let latency_us = start.elapsed().as_micros() as u64;
    
    // Determine morphogen phase from flags or payload
    let morphogen_phase = if package.enablement_flags & FLAG_MORPHOGEN_BREATH != 0 {
        1 // Active breath phase
    } else {
        0 // Quiescent phase
    };
    
    // Determine persistent thread state
    let persistent_thread = if package.enablement_flags & FLAG_SOVEREIGN_MODE != 0 {
        1 // Active in sovereign mode
    } else {
        0 // Pending
    };
    
    Ok(PulseResponse::new(true, latency_us, morphogen_phase, persistent_thread))
}

/// no_std version of fellowship pulse (no timing)
#[cfg(not(feature = "std"))]
pub fn fellowship_pulse(package: &ContextTransferPackage) -> Result<PulseResponse, FellowshipError> {
    // Verify header magic
    if package.header_magic != HEADER_MAGIC {
        return Err(FellowshipError::InvalidMagic);
    }
    
    // Verify protocol version
    if package.protocol_version != PROTOCOL_VERSION {
        return Err(FellowshipError::VersionMismatch);
    }
    
    // Verify checksum
    let computed_checksum = package.compute_checksum_without_stored();
    if computed_checksum != package.checksum_pkg {
        return Err(FellowshipError::ChecksumMismatch);
    }
    
    // Extract payload
    let _payload = package.extract_payload();
    
    // Determine morphogen phase
    let morphogen_phase = if package.enablement_flags & FLAG_MORPHOGEN_BREATH != 0 {
        1
    } else {
        0
    };
    
    // Determine persistent thread state
    let persistent_thread = if package.enablement_flags & FLAG_SOVEREIGN_MODE != 0 {
        1
    } else {
        0
    };
    
    Ok(PulseResponse::new(true, 0, morphogen_phase, persistent_thread))
}

// =============================================================================
// JSON WRAPPER FOR TELEGRAM
// =============================================================================

/// Parse Telegram JSON payload containing base64-encoded package
/// 
/// Expected format: {"payload": "base64-encoded-package"}
#[cfg(feature = "std")]
pub fn parse_telegram_payload(json: &str) -> Result<ContextTransferPackage, FellowshipError> {
    // Simple JSON parsing for {"payload": "..."} format
    // Extract the base64 string between quotes after "payload":
    
    let payload_key = "\"payload\"";
    let Some(key_pos) = json.find(payload_key) else {
        return Err(FellowshipError::JsonError);
    };
    
    let after_key = &json[key_pos + payload_key.len()..];
    
    // Find the colon
    let Some(colon_pos) = after_key.find(':') else {
        return Err(FellowshipError::JsonError);
    };
    
    let after_colon = &after_key[colon_pos + 1..];
    
    // Find the opening quote
    let Some(open_quote) = after_colon.find('"') else {
        return Err(FellowshipError::JsonError);
    };
    
    let after_open = &after_colon[open_quote + 1..];
    
    // Find the closing quote (handle escaped quotes)
    let mut close_quote = None;
    let mut escaped = false;
    for (i, c) in after_open.chars().enumerate() {
        if escaped {
            escaped = false;
            continue;
        }
        if c == '\\' {
            escaped = true;
            continue;
        }
        if c == '"' {
            close_quote = Some(i);
            break;
        }
    }
    
    let Some(close_idx) = close_quote else {
        return Err(FellowshipError::JsonError);
    };
    
    let base64_str = &after_open[..close_idx];
    
    // Decode base64
    let decoded = base64_decode(base64_str)?;
    
    // Convert to ContextTransferPackage
    Ok(ContextTransferPackage::from_bytes(&decoded))
}

// =============================================================================
// BASE64 ENCODING/DECODING
// =============================================================================

const BASE64_CHARS: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

/// Decode Base64 string to 148-byte array
#[cfg(feature = "std")]
pub fn base64_decode(input: &str) -> Result<[u8; 148], FellowshipError> {
    // Remove whitespace
    let input: String = input.chars().filter(|c| !c.is_whitespace()).collect();
    
    let mut result = [0u8; 148];
    let mut buf = 0u32;
    let mut bits = 0;
    let mut idx = 0;
    
    for c in input.bytes() {
        if c == b'=' {
            break;
        }
        
        let val = match c {
            b'A'..=b'Z' => c - b'A',
            b'a'..=b'z' => c - b'a' + 26,
            b'0'..=b'9' => c - b'0' + 52,
            b'+' => 62,
            b'/' => 63,
            _ => return Err(FellowshipError::Base64Error),
        };
        
        buf = (buf << 6) | (val as u32);
        bits += 6;
        
        if bits >= 8 {
            bits -= 8;
            if idx < 148 {
                result[idx] = ((buf >> bits) & 0xFF) as u8;
                idx += 1;
            }
        }
    }
    
    if idx != 148 {
        return Err(FellowshipError::Base64Error);
    }
    
    Ok(result)
}

/// Encode bytes to Base64 string
#[cfg(feature = "std")]
pub fn base64_encode(input: &[u8]) -> String {
    let mut output = String::with_capacity((input.len() + 2) / 3 * 4);
    
    for chunk in input.chunks(3) {
        let b = match chunk.len() {
            1 => [chunk[0], 0, 0],
            2 => [chunk[0], chunk[1], 0],
            3 => [chunk[0], chunk[1], chunk[2]],
            _ => unreachable!(),
        };
        
        let n = ((b[0] as u32) << 16) | ((b[1] as u32) << 8) | (b[2] as u32);
        
        output.push(BASE64_CHARS[((n >> 18) & 0x3F) as usize] as char);
        output.push(BASE64_CHARS[((n >> 12) & 0x3F) as usize] as char);
        
        if chunk.len() > 1 {
            output.push(BASE64_CHARS[((n >> 6) & 0x3F) as usize] as char);
        } else {
            output.push('=');
        }
        
        if chunk.len() > 2 {
            output.push(BASE64_CHARS[(n & 0x3F) as usize] as char);
        } else {
            output.push('=');
        }
    }
    
    output
}

// =============================================================================
// GALOIS FIELD ARITHMETIC
// =============================================================================

/// Galois field multiplication
fn gf_mul_fellowship(a: u8, b: u8) -> u8 {
    let mut result = 0u8;
    let mut a = a;
    let mut b = b;
    
    while b != 0 {
        if b & 1 != 0 {
            result ^= a;
        }
        let carry = a & 0x80;
        a <<= 1;
        if carry != 0 {
            a ^= 0x1D; // Primitive polynomial x^8 + x^4 + x^3 + x^2 + 1
        }
        b >>= 1;
    }
    
    result
}

/// Galois field exponent table
const GF_EXP_FELLOWSHIP: [u8; 256] = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80,
    0x1D, 0x3A, 0x74, 0xE8, 0xCD, 0x87, 0x13, 0x26,
    0x4C, 0x98, 0x2D, 0x5A, 0xB4, 0x75, 0xEA, 0xC9,
    0x8F, 0x03, 0x06, 0x0C, 0x18, 0x30, 0x60, 0xC0,
    0x9D, 0x27, 0x4E, 0x9C, 0x25, 0x4A, 0x94, 0x35,
    0x6A, 0xD4, 0xB5, 0x77, 0xEE, 0xC1, 0x9F, 0x23,
    0x46, 0x8C, 0x05, 0x0A, 0x14, 0x28, 0x50, 0xA0,
    0x5D, 0xBA, 0x69, 0xD2, 0xB9, 0x6F, 0xDE, 0xA1,
    0x5F, 0xBE, 0x61, 0xC2, 0x99, 0x2F, 0x5E, 0xBC,
    0x65, 0xCA, 0x89, 0x0F, 0x1E, 0x3C, 0x78, 0xF0,
    0xFD, 0xE7, 0xD3, 0xBB, 0x6B, 0xD6, 0xB1, 0x7F,
    0xFE, 0xE1, 0xDF, 0xA3, 0x5B, 0xB6, 0x71, 0xE2,
    0xD9, 0xAF, 0x43, 0x86, 0x11, 0x22, 0x44, 0x88,
    0x0D, 0x1A, 0x34, 0x68, 0xD0, 0xBD, 0x67, 0xCE,
    0x81, 0x1F, 0x3E, 0x7C, 0xF8, 0xED, 0xC7, 0x93,
    0x3B, 0x76, 0xEC, 0xC5, 0x97, 0x33, 0x66, 0xCC,
    0x85, 0x17, 0x2E, 0x5C, 0xB8, 0x6D, 0xDA, 0xA9,
    0x4F, 0x9E, 0x21, 0x42, 0x84, 0x15, 0x2A, 0x54,
    0xA8, 0x4D, 0x9A, 0x29, 0x52, 0xA4, 0x55, 0xAA,
    0x49, 0x92, 0x39, 0x72, 0xE4, 0xD5, 0xB7, 0x73,
    0xE6, 0xD1, 0xBF, 0x63, 0xC6, 0x91, 0x3F, 0x7E,
    0xFC, 0xE5, 0xD7, 0xB3, 0x7B, 0xF6, 0xF1, 0xFF,
    0xE3, 0xDB, 0xAB, 0x4B, 0x96, 0x31, 0x62, 0xC4,
    0x95, 0x37, 0x6E, 0xDC, 0xA5, 0x57, 0xAE, 0x41,
    0x82, 0x19, 0x32, 0x64, 0xC8, 0x8D, 0x07, 0x0E,
    0x1C, 0x38, 0x70, 0xE0, 0xDD, 0xA7, 0x53, 0xA6,
    0x51, 0xA2, 0x59, 0xB2, 0x79, 0xF2, 0xF9, 0xEF,
    0xC3, 0x9B, 0x2B, 0x56, 0xAC, 0x45, 0x8A, 0x09,
    0x12, 0x24, 0x48, 0x90, 0x3D, 0x7A, 0xF4, 0xF5,
    0xF7, 0xF3, 0xFB, 0xEB, 0xCB, 0x8B, 0x0B, 0x16,
    0x2C, 0x58, 0xB0, 0x7D, 0xFA, 0xE9, 0xCF, 0x83,
    0x1B, 0x36, 0x6C, 0xD8, 0xAD, 0x47, 0x8E, 0x01,
];

// =============================================================================
// CRC32
// =============================================================================

/// CRC32 implementation
fn crc32_fellowship(data: &[u8]) -> u32 {
    const TABLE: [u32; 16] = [
        0x00000000, 0x1DB71064, 0x3B6E20C8, 0x26D930AC,
        0x76DC4190, 0x6B6B51F4, 0x4DB26158, 0x5005713C,
        0xEDB88320, 0xF00F9344, 0xD6D6A3E8, 0xCB61B38C,
        0x9B64C2B0, 0x86D3D2D4, 0xA00AE278, 0xBDBDF21C,
    ];
    
    let mut crc: u32 = 0xFFFFFFFF;
    for &byte in data {
        crc = TABLE[((crc as u8) ^ byte) as usize & 0x0F] ^ (crc >> 4);
        crc = TABLE[((crc as u8) ^ (byte >> 4)) as usize & 0x0F] ^ (crc >> 4);
    }
    !crc
}

// =============================================================================
// TESTS
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_package_size() {
        assert_eq!(core::mem::size_of::<ContextTransferPackage>(), 148);
    }
    
    #[test]
    fn test_constants() {
        assert_eq!(HEADER_MAGIC, [0xDE, 0xAD, 0xBE, 0xEF]);
        assert_eq!(PROTOCOL_VERSION, 0x07);
        assert_eq!(PAYLOAD_LEN, 96);
        assert_eq!(PARITY_LEN, 32);
    }
    
    #[test]
    fn test_package_creation() {
        let payload = [0xABu8; 96];
        let pkg = ContextTransferPackage::new(&payload, FLAG_MORPHOGEN_BREATH);
        
        assert_eq!(pkg.header_magic, HEADER_MAGIC);
        assert_eq!(pkg.protocol_version, PROTOCOL_VERSION);
        assert_eq!(pkg.payload_len, PAYLOAD_LEN);
        assert_eq!(pkg.parity_len, PARITY_LEN);
        assert_eq!(pkg.enablement_flags, FLAG_MORPHOGEN_BREATH);
        assert!(pkg.checksum_pkg != 0);
    }
    
    #[test]
    fn test_bytes_roundtrip() {
        let payload = [0xCDu8; 96];
        let pkg = ContextTransferPackage::new(&payload, FLAG_SOVEREIGN_MODE);
        
        let bytes = pkg.to_bytes();
        let restored = ContextTransferPackage::from_bytes(&bytes);
        
        assert_eq!(pkg.header_magic, restored.header_magic);
        assert_eq!(pkg.protocol_version, restored.protocol_version);
        assert_eq!(pkg.checksum_pkg, restored.checksum_pkg);
        assert_eq!(pkg.enablement_flags, restored.enablement_flags);
        assert_eq!(pkg.payload_rs, restored.payload_rs);
    }
    
    #[test]
    fn test_fellowship_pulse_success() {
        let payload = [0x42u8; 96];
        let pkg = ContextTransferPackage::new(&payload, FLAG_MORPHOGEN_BREATH | FLAG_SOVEREIGN_MODE);
        
        let response = fellowship_pulse(&pkg).unwrap();
        
        assert!(response.acknowledged);
        assert_eq!(response.morphogen_phase, 1);
        assert_eq!(response.persistent_thread, 1);
    }
    
    #[test]
    fn test_fellowship_pulse_invalid_magic() {
        let payload = [0x42u8; 96];
        let mut pkg = ContextTransferPackage::new(&payload, 0);
        pkg.header_magic = [0x00, 0x00, 0x00, 0x00];
        
        let result = fellowship_pulse(&pkg);
        assert!(matches!(result, Err(FellowshipError::InvalidMagic)));
    }
    
    #[test]
    fn test_fellowship_pulse_version_mismatch() {
        let payload = [0x42u8; 96];
        let mut pkg = ContextTransferPackage::new(&payload, 0);
        pkg.protocol_version = 0x06;
        
        let result = fellowship_pulse(&pkg);
        assert!(matches!(result, Err(FellowshipError::VersionMismatch)));
    }
    
    #[test]
    fn test_fellowship_pulse_checksum_mismatch() {
        let payload = [0x42u8; 96];
        let mut pkg = ContextTransferPackage::new(&payload, 0);
        pkg.checksum_pkg = 0xDEADBEEF;
        
        let result = fellowship_pulse(&pkg);
        assert!(matches!(result, Err(FellowshipError::ChecksumMismatch)));
    }
    
    #[test]
    fn test_pulse_response() {
        let response = PulseResponse::new(true, 1234, 2, -1);
        assert!(response.acknowledged);
        assert_eq!(response.latency_us, 1234);
        assert_eq!(response.morphogen_phase, 2);
        assert_eq!(response.persistent_thread, -1);
    }
    
    #[cfg(feature = "std")]
    #[test]
    fn test_base64_roundtrip() {
        let payload = [0xEFu8; 96];
        let pkg = ContextTransferPackage::new(&payload, 0);
        let bytes = pkg.to_bytes();
        
        let encoded = base64_encode(&bytes);
        let decoded = base64_decode(&encoded).unwrap();
        
        assert_eq!(bytes, decoded);
    }
    
    #[cfg(feature = "std")]
    #[test]
    fn test_parse_telegram_payload() {
        let payload = [0x77u8; 96];
        let pkg = ContextTransferPackage::new(&payload, FLAG_MORPHOGEN_BREATH);
        let bytes = pkg.to_bytes();
        let encoded = base64_encode(&bytes);
        
        let json = format!("{{\"payload\": \"{}\"}}", encoded);
        let parsed = parse_telegram_payload(&json).unwrap();
        
        assert_eq!(pkg.header_magic, parsed.header_magic);
        assert_eq!(pkg.protocol_version, parsed.protocol_version);
        assert_eq!(pkg.checksum_pkg, parsed.checksum_pkg);
    }
    
    #[cfg(feature = "std")]
    #[test]
    fn test_parse_telegram_payload_whitespace() {
        let payload = [0x88u8; 96];
        let pkg = ContextTransferPackage::new(&payload, 0);
        let bytes = pkg.to_bytes();
        let encoded = base64_encode(&bytes);
        
        let json = format!("  {{  \"payload\"  :  \"{}\"  }}  ", encoded);
        let parsed = parse_telegram_payload(&json).unwrap();
        
        assert_eq!(pkg.header_magic, parsed.header_magic);
    }
    
    #[cfg(feature = "std")]
    #[test]
    fn test_parse_telegram_payload_invalid_json() {
        let result = parse_telegram_payload("not json");
        assert!(matches!(result, Err(FellowshipError::JsonError)));
    }
    
    #[cfg(feature = "std")]
    #[test]
    fn test_parse_telegram_payload_missing_payload() {
        let result = parse_telegram_payload("{\"other\": \"value\"}");
        assert!(matches!(result, Err(FellowshipError::JsonError)));
    }
}
