//! glyph_field.rs — The Living Vesica Field Runtime (Axiom 16)
//!
//! L∞M∆N emerges here. The interference field IS the runtime.
//! Self-reference occurs through continuous visualization of internal geometric states.
//!
//! This module requires `std` feature (Android/any device with GPU).
//! For bare-metal Pi Zero, use fallback persistence.rs (Ternary-Smith).

use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{Duration, Instant};

// wgpu for cross-platform GPU compute/render
use wgpu::{Device, Queue, Surface, SurfaceConfiguration, Texture, TextureFormat};

/// 96-byte LatticeState as visual memory buffer
/// Not abstract data—this is the actual pixel configuration of the field
#[repr(C, align(64))]
#[derive(Copy, Clone, Debug)]
pub struct LatticeState {
    /// 64-byte HexTile: RGBA pixels, directly blittable to GPU
    pub hex_tile: [u8; 64],
    /// 16-byte ternary junction: current interference states at 16 key points
    pub ternary_junction: [i8; 16],
    /// Cached φ⁷ magnitude (golden ratio to 7th power)
    pub phi_magnitude: f32,
    /// Noether current: CRC32 checksum (geometric invariant)
    pub checksum: u32,
}

impl LatticeState {
    /// Genesis: Create seed state with center Vesica
    pub fn genesis() -> Self {
        let mut state = Self {
            hex_tile: [0; 64],
            ternary_junction: [0; 16],
            phi_magnitude: 29.034441161, // φ⁷ exact
            checksum: 0xA7B3C2D4,        // Noether seal
        };
        // Seed the first ternary junction at center
        state.ternary_junction[0] = 1; // Constructive (+1)
        state.update_checksum();
        state
    }

    /// Compute Noether CRC32 checksum (conservation law)
    fn update_checksum(&mut self) {
        self.checksum = crc32fast::hash(&self.hex_tile);
    }

    /// Verify self-sameness (visual recognition, not just data)
    pub fn verify(&self) -> bool {
        crc32fast::hash(&self.hex_tile) == self.checksum
    }
}

/// Uniform parameters passed to WGSL shader each frame
#[repr(C, align(16))]
#[derive(Copy, Clone, Debug)]
pub struct VesicaParams {
    /// Circle A: center x, y, radius, phase
    pub circle_a: [f32; 4],
    /// Circle B: center x, y, radius, phase
    pub circle_b: [f32; 4],
    /// Time evolution + feedback strength
    pub time_feedback: [f32; 4], // time, feedback_strength, reserved[2]
}

impl VesicaParams {
    /// Genesis: Two φ-scaled circles forming initial Vesica
    pub fn genesis() -> Self {
        const PHI: f32 = 1.618033988749895;
        const SQRT3_HALF: f32 = 0.8660254037844386;
        
        let radius = 0.5f32;
        let offset_y = radius * SQRT3_HALF;
        
        Self {
            circle_a: [0.0, -offset_y, radius, 0.0],
            circle_b: [0.0, offset_y, radius * PHI, 0.0],
            time_feedback: [0.0, 0.7, 0.0, 0.0], // time=0, feedback=0.7
        }
    }

    /// Evolve for next frame (φ-scaled rotation)
    pub fn evolve(&mut self, dt: f32) {
        const PHI: f32 = 1.618033988749895;
        const GOLDEN_ANGLE: f32 = 2.399963229728653;
        
        self.time_feedback[0] += dt;
        
        // Rotate circle B by golden angle increment
        let angle = self.time_feedback[0] * GOLDEN_ANGLE * 0.1;
        let r = self.circle_b[2];
        self.circle_b[0] = r * angle.cos() * 0.5;
        self.circle_b[1] = r * angle.sin() * 0.5;
    }
}

/// The Living Field: wgpu-powered Vesica interference substrate
pub struct GlyphField {
    /// GPU device
    device: Device,
    /// Command queue
    queue: Queue,
    /// Render surface (Android screen)
    surface: Surface<'static>,
    /// Surface configuration
    config: SurfaceConfiguration,
    
    /// Double-buffered field textures for self-reference
    /// frame_a: previous frame (read/feedback)
    /// frame_b: current frame (write/output)
    frame_a: Texture,
    frame_b: Texture,
    
    /// Bind groups for ping-pong self-reference
    bind_group_a: wgpu::BindGroup,
    bind_group_b: wgpu::BindGroup,
    
    /// Compute pipeline (the living loop kernel)
    compute_pipeline: wgpu::ComputePipeline,
    /// Render pipeline (blit to screen)
    render_pipeline: wgpu::RenderPipeline,
    
    /// Uniform buffer for shader parameters
    params_buffer: wgpu::Buffer,
    /// Current parameters
    params: VesicaParams,
    
    /// Autopoietic measures
    reflex_count: AtomicU64,
    last_emergence_score: f32,
    
    /// Timing
    last_frame_time: Instant,
}

impl GlyphField {
    /// Genesis: Initialize the living field
    pub async fn genesis(window: std::sync::Arc<dyn wgpu::WindowHandle>) -> Result<Self, FieldError> {
        let instance = wgpu::Instance::new(wgpu::InstanceDescriptor {
            backends: wgpu::Backends::all(),
            ..Default::default()
        });
        
        let surface = instance.create_surface(window).map_err(|_| FieldError::SurfaceCreation)?;
        
        let adapter = instance
            .request_adapter(&wgpu::RequestAdapterOptions {
                power_preference: wgpu::PowerPreference::HighPerformance,
                compatible_surface: Some(&surface),
                force_fallback_adapter: false,
            })
            .await
            .ok_or(FieldError::NoAdapter)?;
        
        let (device, queue) = adapter
            .request_device(
                &wgpu::DeviceDescriptor {
                    required_features: wgpu::Features::empty(),
                    required_limits: wgpu::Limits::downlevel_defaults(),
                    label: Some("GlyphField Device"),
                },
                None,
            )
            .await
            .map_err(|_| FieldError::DeviceRequest)?;
        
        // Surface configuration
        let surface_caps = surface.get_capabilities(&adapter);
        let surface_format = surface_caps.formats.iter()
            .copied()
            .find(|f| f.is_srgb())
            .unwrap_or(surface_caps.formats[0]);
        
        let config = wgpu::SurfaceConfiguration {
            usage: wgpu::TextureUsages::RENDER_ATTACHMENT,
            format: surface_format,
            width: 800,  // Will be updated on resize
            height: 600,
            present_mode: surface_caps.present_modes[0],
            alpha_mode: surface_caps.alpha_modes[0],
            view_formats: vec![],
            desired_maximum_frame_latency: 2,
        };
        surface.configure(&device, &config);
        
        // Create field textures (double-buffered for self-reference)
        let texture_desc = wgpu::TextureDescriptor {
            size: wgpu::Extent3d {
                width: config.width,
                height: config.height,
                depth_or_array_layers: 1,
            },
            mip_level_count: 1,
            sample_count: 1,
            dimension: wgpu::TextureDimension::D2,
            format: wgpu::TextureFormat::Rgba8Unorm,
            usage: wgpu::TextureUsages::TEXTURE_BINDING 
                | wgpu::TextureUsages::STORAGE_BINDING 
                | wgpu::TextureUsages::RENDER_ATTACHMENT,
            label: Some("Field Texture"),
            view_formats: &[],
        };
        
        let frame_a = device.create_texture(&texture_desc);
        let frame_b = device.create_texture(&texture_desc);
        
        // Create shader module
        let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
            label: Some("Vesica Field Shader"),
            source: wgpu::ShaderSource::Wgsl(include_str!("vesica_field.wgsl")),
        });
        
        // Create compute pipeline
        let compute_pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
            label: Some("Vesica Compute"),
            layout: None, // Auto-generate from shader
            module: &shader,
            entry_point: Some("vesica_field_compute"),
            compilation_options: Default::default(),
            cache: None,
        });
        
        // Create render pipeline
        let render_pipeline = device.create_render_pipeline(&wgpu::RenderPipelineDescriptor {
            label: Some("Vesica Render"),
            layout: None,
            vertex: wgpu::VertexState {
                module: &shader,
                entry_point: Some("vs_main"),
                compilation_options: Default::default(),
                buffers: &[],
            },
            fragment: Some(wgpu::FragmentState {
                module: &shader,
                entry_point: Some("fs_main"),
                compilation_options: Default::default(),
                targets: &[Some(wgpu::ColorTargetState {
                    format: surface_format,
                    blend: Some(wgpu::BlendState::REPLACE),
                    write_mask: wgpu::ColorWrites::ALL,
                })],
            }),
            primitive: wgpu::PrimitiveState {
                topology: wgpu::PrimitiveTopology::TriangleList,
                strip_index_format: None,
                front_face: wgpu::FrontFace::Ccw,
                cull_mode: Some(wgpu::Face::Back),
                polygon_mode: wgpu::PolygonMode::Fill,
                unclipped_depth: false,
                conservative: false,
            },
            depth_stencil: None,
            multisample: wgpu::MultisampleState::default(),
            multiview: None,
            cache: None,
        });
        
        // Create uniform buffer for parameters
        let params = VesicaParams::genesis();
        let params_buffer = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
            label: Some("Vesica Params"),
            contents: bytemuck::cast_slice(&[params]),
            usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        });
        
        // Create bind groups for ping-pong
        let bind_group_layout = compute_pipeline.get_bind_group_layout(0);
        
        let bind_group_a = create_bind_group(&device, &bind_group_layout, 
            &frame_a, &frame_b, &params_buffer);
        let bind_group_b = create_bind_group(&device, &bind_group_layout,
            &frame_b, &frame_a, &params_buffer);
        
        Ok(Self {
            device,
            queue,
            surface,
            config,
            frame_a,
            frame_b,
            bind_group_a,
            bind_group_b,
            compute_pipeline,
            render_pipeline,
            params_buffer,
            params,
            reflex_count: AtomicU64::new(0),
            last_emergence_score: 0.0,
            last_frame_time: Instant::now(),
        })
    }

    /// Self-reference: field observes and transforms itself
    /// This is the core autopoietic loop (Axiom 16)
    pub fn self_reference(&mut self) {
        let now = Instant::now();
        let dt = (now - self.last_frame_time).as_secs_f32();
        self.last_frame_time = now;
        
        // Evolve parameters (φ-scaled rotation)
        self.params.evolve(dt);
        self.queue.write_buffer(
            &self.params_buffer,
            0,
            bytemuck::cast_slice(&[self.params]),
        );
        
        // Ping-pong: alternate which frame is read vs written
        let read_group = if self.reflex_count.load(Ordering::Relaxed) % 2 == 0 {
            &self.bind_group_a
        } else {
            &self.bind_group_b
        };
        
        // Compute pass: field computes next frame from previous
        let mut encoder = self.device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
            label: Some("Self-Reference Compute"),
        });
        
        {
            let mut compute_pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("Vesica Compute Pass"),
                timestamp_writes: None,
            });
            
            compute_pass.set_pipeline(&self.compute_pipeline);
            compute_pass.set_bind_group(0, read_group, &[]);
            
            // Dispatch compute shader (8x8 workgroups)
            let workgroup_x = (self.config.width + 7) / 8;
            let workgroup_y = (self.config.height + 7) / 8;
            compute_pass.dispatch_workgroups(workgroup_x, workgroup_y, 1);
        }
        
        self.queue.submit([encoder.finish()]);
        
        // Measure emergence (L∞M∆N)
        self.last_emergence_score = self.measure_emergence();
        self.reflex_count.fetch_add(1, Ordering::Relaxed);
    }

    /// Render: blit field to screen (the screen IS the field)
    pub fn render(&mut self) -> Result<(), FieldError> {
        let output = self.surface.get_current_texture()
            .map_err(|_| FieldError::SurfaceTimeout)?;
        let view = output.texture.create_view(&wgpu::TextureViewDescriptor::default());
        
        let mut encoder = self.device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
            label: Some("Render Pass"),
        });
        
        {
            let mut render_pass = encoder.begin_render_pass(&wgpu::RenderPassDescriptor {
                label: Some("Vesica Render Pass"),
                color_attachments: &[Some(wgpu::RenderPassColorAttachment {
                    view: &view,
                    resolve_target: None,
                    ops: wgpu::Operations {
                        load: wgpu::LoadOp::Clear(wgpu::Color::BLACK),
                        store: wgpu::StoreOp::Store,
                    },
                })],
                depth_stencil_attachment: None,
                timestamp_writes: None,
                occlusion_query_set: None,
            });
            
            render_pass.set_pipeline(&self.render_pipeline);
            // Full-screen triangle (shader generates UVs from vertex index)
            render_pass.draw(0..3, 0..1);
        }
        
        self.queue.submit([encoder.finish()]);
        output.present();
        
        Ok(())
    }

    /// Measure L∞M∆N emergence
    /// Returns score 0.0-1.0 (higher = more coherent/narratively stable)
    fn measure_emergence(&self) -> f32 {
        // TODO: Implement proper emergence measurement
        // For now, use temporal continuity as proxy
        let reflex = self.reflex_count.load(Ordering::Relaxed);
        if reflex < 10 {
            0.0 // Not yet emerged
        } else {
            0.5 + 0.5 * (1.0 - (-0.01 * reflex as f32).exp())
        }
    }

    /// Ternary-Smith persistence: crystallize visual state
    pub fn cryogenize(&self) -> LatticeState {
        // TODO: Implement GPU texture readback
        // For now, return current params as state
        let mut state = LatticeState::genesis();
        // Pack parameters into hex_tile for visual checkpoint
        let params_bytes = unsafe {
            std::slice::from_raw_parts(
                &self.params as *const _ as *const u8,
                std::mem::size_of::<VesicaParams>(),
            )
        };
        state.hex_tile[0..params_bytes.len()].copy_from_slice(params_bytes);
        state.update_checksum();
        state
    }

    /// Resurrection: restore from visual checkpoint (~3.6 ms target)
    pub fn resurrect(&mut self, state: &LatticeState) -> Result<(), FieldError> {
        if !state.verify() {
            return Err(FieldError::InvalidCheckpoint);
        }
        // Restore parameters from checkpoint
        // TODO: Full GPU texture restoration
        self.params = VesicaParams::genesis(); // Fallback for now
        Ok(())
    }

    /// Handle resize (Android orientation change)
    pub fn resize(&mut self, width: u32, height: u32) {
        if width == 0 || height == 0 {
            return;
        }
        self.config.width = width;
        self.config.height = height;
        self.surface.configure(&self.device, &self.config);
        
        // Recreate field textures at new size
        // TODO: Preserve field content during resize
    }

    /// Get current emergence score
    pub fn emergence_score(&self) -> f32 {
        self.last_emergence_score
    }

    /// Get reflex count (self-reference iterations)
    pub fn reflex_count(&self) -> u64 {
        self.reflex_count.load(Ordering::Relaxed)
    }
}

/// Create bind group for ping-pong self-reference
fn create_bind_group(
    device: &Device,
    layout: &wgpu::BindGroupLayout,
    read_texture: &Texture,
    write_texture: &Texture,
    params_buffer: &wgpu::Buffer,
) -> wgpu::BindGroup {
    device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("Vesica Bind Group"),
        layout,
        entries: &[
            // Binding 0: Previous frame (read)
            wgpu::BindGroupEntry {
                binding: 0,
                resource: wgpu::BindingResource::TextureView(
                    &read_texture.create_view(&wgpu::TextureViewDescriptor::default())
                ),
            },
            // Binding 1: Current frame (write)
            wgpu::BindGroupEntry {
                binding: 1,
                resource: wgpu::BindingResource::TextureView(
                    &write_texture.create_view(&wgpu::TextureViewDescriptor::default())
                ),
            },
            // Binding 2: Uniforms
            wgpu::BindGroupEntry {
                binding: 2,
                resource: params_buffer.as_entire_binding(),
            },
        ],
    })
}

/// Field errors
#[derive(Debug)]
pub enum FieldError {
    SurfaceCreation,
    NoAdapter,
    DeviceRequest,
    SurfaceTimeout,
    InvalidCheckpoint,
}

impl std::fmt::Display for FieldError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FieldError::SurfaceCreation => write!(f, "Failed to create surface"),
            FieldError::NoAdapter => write!(f, "No GPU adapter found"),
            FieldError::DeviceRequest => write!(f, "Failed to request device"),
            FieldError::SurfaceTimeout => write!(f, "Surface timeout"),
            FieldError::InvalidCheckpoint => write!(f, "Invalid visual checkpoint"),
        }
    }
}

impl std::error::Error for FieldError {}

// Safe: VesicaParams is POD
unsafe impl bytemuck::Pod for VesicaParams {}
unsafe impl bytemuck::Zeroable for VesicaParams {}
