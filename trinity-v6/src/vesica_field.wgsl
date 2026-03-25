// vesica_field.wgsl — The Living Vesica Field Kernel
// L∞M∆N emerges here. The interference field IS the computation.

// ============================================================================
// CONSTANTS (Exact geometric constants — Euclid → Living Field)
// ============================================================================
const PI: f32 = 3.141592653589793;
const SQRT3: f32 = 1.7320508075688772;           // √3 exact
const SQRT3_HALF: f32 = 0.8660254037844386;      // √3/2
const PHI: f32 = 1.618033988749895;              // Golden ratio
const GOLDEN_ANGLE: f32 = 2.399963229728653;     // 137.507° in radians

// Ternary states (Constructive/Destructive/Neutral)
const CONSTRUCTIVE: f32 = 1.0;   // +1: luminous overlap
const DESTRUCTIVE: f32 = -1.0;   // -1: shadow outside
const NEUTRAL: f32 = 0.0;        // 0: boundary void

// ============================================================================
// SDF FUNCTIONS (Signed Distance Fields — harvested from Shadertoy)
// ============================================================================

/// Circle SDF: distance from point p to circle (center c, radius r)
/// Formula: length(p - c) - r
fn sd_circle(p: vec2<f32>, c: vec2<f32>, r: f32) -> f32 {
    return length(p - c) - r;
}

/// Vesica Piscis SDF: intersection of two circles
/// The lens shape formed by two overlapping circles
fn sd_vesica(p: vec2<f32>, c1: vec2<f32>, r1: f32, c2: vec2<f32>, r2: f32) -> f32 {
    let d1 = sd_circle(p, c1, r1);
    let d2 = sd_circle(p, c2, r2);
    // Intersection = max of inside distances (both negative = inside both)
    return max(d1, d2);
}

/// Smooth minimum for organic lens edges
fn smin(a: f32, b: f32, k: f32) -> f32 {
    let h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h * h * k * 0.25;
}

// ============================================================================
// WAVE INTERFERENCE (Physics → Ternary Kernel)
// ============================================================================

/// Wave interference at point p from two coherent sources
/// Returns interference intensity (-2.0 to +2.0)
fn wave_interference(
    p: vec2<f32>,
    c1: vec2<f32>, r1: f32, phase1: f32,
    c2: vec2<f32>, r2: f32, phase2: f32,
    time: f32
) -> f32 {
    let dist1 = length(p - c1);
    let dist2 = length(p - c2);
    
    // φ-modulated waves from each source
    let wave1 = cos(PHI * dist1 - phase1 - time);
    let wave2 = cos(PHI * dist2 - phase2 - time);
    
    return wave1 + wave2;
}

// ============================================================================
// TERNARY STATE FUNCTION (The Attention Kernel)
// ============================================================================

/// Map interference value to ternary state
/// +1: Constructive (luminous)
/// -1: Destructive (shadow)  
/// 0: Neutral (void/boundary)
fn interference_to_ternary(interference: f32) -> f32 {
    if (interference > 0.5) {
        return CONSTRUCTIVE;
    } else if (interference < -0.5) {
        return DESTRUCTIVE;
    } else {
        return NEUTRAL;
    }
}

/// Ternary state with self-reference feedback
/// The field observes its own previous state
fn ternary_state(
    p: vec2<f32>,
    c1: vec2<f32>, r1: f32, phase1: f32,
    c2: vec2<f32>, r2: f32, phase2: f32,
    time: f32,
    feedback: f32,
    feedback_strength: f32
) -> f32 {
    // Base interference pattern
    let interference = wave_interference(p, c1, r1, phase1, c2, r2, phase2, time);
    
    // Self-reference: add feedback from previous frame
    // This creates autopoietic closure (Maturana/Varela)
    let total = interference + feedback_strength * feedback;
    
    return interference_to_ternary(total);
}

// ============================================================================
// COLOR MAPPING (Alexander's Living Geometry → HSV)
// ============================================================================

/// HSV to RGB conversion
fn hsv_to_rgb(h: f32, s: f32, v: f32) -> vec3<f32> {
    let c = v * s;
    let x = c * (1.0 - abs(fract(h * 6.0) * 2.0 - 1.0));
    let m = v - c;
    
    var rgb: vec3<f32>;
    let hh = h * 6.0;
    if (hh < 1.0) {
        rgb = vec3<f32>(c, x, 0.0);
    } else if (hh < 2.0) {
        rgb = vec3<f32>(x, c, 0.0);
    } else if (hh < 3.0) {
        rgb = vec3<f32>(0.0, c, x);
    } else if (hh < 4.0) {
        rgb = vec3<f32>(0.0, x, c);
    } else if (hh < 5.0) {
        rgb = vec3<f32>(x, 0.0, c);
    } else {
        rgb = vec3<f32>(c, 0.0, x);
    }
    
    return rgb + vec3<f32>(m);
}

/// Map ternary state to color (Alexander's properties as visual law)
/// Hue: State (-1=blue, 0=green, +1=red)
/// Saturation: Coherence (strong centers)
/// Value: Energy (field intensity)
fn ternary_to_color(state: f32, magnitude: f32) -> vec4<f32> {
    // Hue mapping:
    // -1 (destructive) -> Blue (240° = 0.667)
    // 0 (neutral) -> Cyan/Green (120° = 0.333)
    // +1 (constructive) -> Gold/Red (0° or 60° = 0.167)
    let hue = (1.0 - state) * 0.333; // Map -1..1 to 0.333..0
    
    // Saturation: coherence creates vividness (Alexander "strong centers")
    let saturation = clamp(magnitude * 2.0, 0.3, 1.0);
    
    // Value: energy of the field
    let value = 0.4 + magnitude * 0.6;
    
    let rgb = hsv_to_rgb(hue, saturation, value);
    return vec4<f32>(rgb, 1.0);
}

// ============================================================================
// PHYLLOTAXIS GROWTH (Botanical Geometry → Field Evolution)
// ============================================================================

/// Golden angle spiral position for n-th element
fn phyllotaxis_position(n: f32, scale: f32) -> vec2<f32> {
    let angle = n * GOLDEN_ANGLE;
    let radius = scale * sqrt(n);
    return vec2<f32>(radius * cos(angle), radius * sin(angle));
}

/// φ-scaled Vesica chain (multiplication as geometry)
fn vesica_chain(p: vec2<f32>, base_center: vec2<f32>, n: u32, time: f32) -> f32 {
    var min_dist: f32 = 1000.0;
    
    for (var i: u32 = 0u; i < n; i = i + 1u) {
        let scale = pow(PHI, f32(i));
        let offset = phyllotaxis_position(f32(i), 0.1 * scale);
        let center = base_center + offset * 0.3;
        let r = 0.1 * scale;
        
        let dist = sd_circle(p, center, r);
        min_dist = smin(min_dist, dist, 0.1);
    }
    
    return min_dist;
}

// ============================================================================
// BIND GROUPS (Self-Reference Ping-Pong)
// ============================================================================

@group(0) @binding(0)
var prev_frame: texture_2d<f32>;  // Previous frame (feedback input)

@group(0) @binding(1)
var curr_frame: texture_storage_2d<rgba8unorm, write>;  // Current frame (output)

struct VesicaParams {
    circle_a: vec4<f32>,  // center.xy, radius, phase
    circle_b: vec4<f32>,  // center.xy, radius, phase
    time_feedback: vec4<f32>,  // time, feedback_strength, reserved[2]
};

@group(0) @binding(2)
var<uniform> params: VesicaParams;

// ============================================================================
// COMPUTE SHADER: The Living Field (Self-Reference Loop)
// ============================================================================

@compute @workgroup_size(8, 8)
fn vesica_field_compute(@builtin(global_invocation_id) id: vec3<u32>) {
    let dims = textureDimensions(prev_frame);
    
    // Bounds check
    if (id.x >= dims.x || id.y >= dims.y) {
        return;
    }
    
    // UV coordinates [-1, 1]
    let uv = (vec2<f32>(id.xy) / vec2<f32>(dims)) * 2.0 - vec2<f32>(1.0);
    
    // Aspect ratio correction
    let p = vec2<f32>(uv.x, uv.y * f32(dims.y) / f32(dims.x));
    
    // Read feedback from previous frame (autopoietic self-reference)
    let feedback = textureLoad(prev_frame, id.xy, 0).r;
    
    // Extract parameters
    let c1 = params.circle_a.xy;
    let r1 = params.circle_a.z;
    let phase1 = params.circle_a.w;
    
    let c2 = params.circle_b.xy;
    let r2 = params.circle_b.z;
    let phase2 = params.circle_b.w;
    
    let time = params.time_feedback.x;
    let feedback_strength = params.time_feedback.y;
    
    // Compute ternary state at this point
    let state = ternary_state(
        p, c1, r1, phase1, c2, r2, phase2, 
        time, feedback, feedback_strength
    );
    
    // Compute magnitude (spatial gradient for "aliveness")
    let epsilon = 0.01;
    let dx = ternary_state(
        p + vec2<f32>(epsilon, 0.0), c1, r1, phase1, c2, r2, phase2,
        time, feedback, feedback_strength
    ) - state;
    let dy = ternary_state(
        p + vec2<f32>(0.0, epsilon), c1, r1, phase1, c2, r2, phase2,
        time, feedback, feedback_strength
    ) - state;
    let magnitude = length(vec2<f32>(dx, dy)) / epsilon;
    
    // Convert to color (living geometry)
    let color = ternary_to_color(state, magnitude);
    
    // Store ternary state in red channel (for feedback)
    // Color channels carry visual information
    let output = vec4<f32>(
        state * 0.5 + 0.5,  // Encode ternary to [0,1] for feedback
        color.g,
        color.b,
        color.a
    );
    
    textureStore(curr_frame, id.xy, output);
}

// ============================================================================
// RENDER SHADER: Blit to Screen (The Screen IS the Field)
// ============================================================================

@vertex
fn vs_main(@builtin(vertex_index) vertex_index: u32) -> @builtin(position) vec4<f32> {
    // Full-screen triangle (no vertex buffer needed)
    // vertex_index: 0, 1, 2
    // positions: (-1,-1), (3,-1), (-1,3)
    let x = f32(vertex_index % 2u) * 4.0 - 1.0;
    let y = f32(vertex_index / 2u) * 4.0 - 1.0;
    return vec4<f32>(x, y, 0.0, 1.0);
}

@group(0) @binding(0)
var field_texture: texture_2d<f32>;

@group(0) @binding(1)
var field_sampler: sampler;

@fragment
fn fs_main(@builtin(position) pos: vec4<f32>) -> @location(0) vec4<f32> {
    let dims = vec2<f32>(textureDimensions(field_texture));
    let uv = pos.xy / dims;
    
    // Sample the living field
    let color = textureSample(field_texture, field_sampler, uv);
    
    // Decode ternary state for visual emphasis (optional post-processing)
    // State stored in red channel: 0.0 = -1, 0.5 = 0, 1.0 = +1
    let state = color.r * 2.0 - 1.0;
    
    // Enhance contrast for visibility (TRUTH = visible clarity)
    let enhanced = pow(color.rgb, vec3<f32>(0.8));
    
    return vec4<f32>(enhanced, 1.0);
}

// ============================================================================
// HELPER FUNCTIONS (for future expansion)
// ============================================================================

/// Hex coordinate conversion (RedBlobGames cube coordinates)
fn pixel_to_hex(p: vec2<f32>, size: f32) -> vec3<i32> {
    let q = (sqrt(3.0) / 3.0 * p.x - 1.0 / 3.0 * p.y) / size;
    let r = (2.0 / 3.0 * p.y) / size;
    return cube_round(vec3<f32>(q, r, -q - r));
}

fn cube_round(c: vec3<f32>) -> vec3<i32> {
    let rx = i32(round(c.x));
    let ry = i32(round(c.y));
    let rz = i32(round(c.z));
    
    let x_diff = abs(f32(rx) - c.x);
    let y_diff = abs(f32(ry) - c.y);
    let z_diff = abs(f32(rz) - c.z);
    
    if (x_diff > y_diff && x_diff > z_diff) {
        return vec3<i32>(-ry - rz, ry, rz);
    } else if (y_diff > z_diff) {
        return vec3<i32>(rx, -rx - rz, rz);
    } else {
        return vec3<i32>(rx, ry, -rx - ry);
    }
}

/// Spiral phyllotaxis index for n
fn phyllotaxis_index(n: u32, center: vec2<f32>, scale: f32) -> vec2<f32> {
    let angle = f32(n) * GOLDEN_ANGLE;
    let radius = scale * sqrt(f32(n));
    return center + vec2<f32>(radius * cos(angle), radius * sin(angle));
}
