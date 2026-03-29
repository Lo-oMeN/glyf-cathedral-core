#!/usr/bin/env python3
"""
golden_angle_morph.py - Generate golden-angle phyllotaxis morph GIF

Creates a looping animation of the phyllotaxis spiral with:
- Golden angle rotation (137.507764°)
- φ-harmonic scaling
- Color gradient through 7 glyph primitives
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
import matplotlib.animation as animation
from pathlib import Path

# Golden ratio constants
PHI = 1.618033988749895
GOLDEN_ANGLE = 2.39996323  # radians = 137.507764°
PHI_7 = 29.034441161

# 7 Glyph primitives with colors
GLYPHS = {
    'VOID': '#1a1a2e',      # Deep space
    'DOT': '#e94560',       # Vibrant red
    'CURVE': '#f7b731',     # Golden
    'LINE': '#20bf6b',      # Emerald
    'ANGLE': '#4b7bec',     # Blue
    'CIRCLE': '#a55eea',    # Purple
    'VESICA': '#26de81',    # Spring green
}

class GoldenAngleMorph:
    """Generate phyllotaxis morph animation."""
    
    def __init__(self, n_points=200, figsize=(800, 800), dpi=100):
        self.n_points = n_points
        self.figsize = figsize
        self.dpi = dpi
        self.frames = 60  # 2 seconds @ 30fps
        
    def phyllotaxis_points(self, n, scale=1.0, rotation=0.0):
        """Generate phyllotaxis spiral points."""
        points = []
        for i in range(n):
            theta = i * GOLDEN_ANGLE + rotation
            r = scale * np.sqrt(i) * 0.5
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            # Determine glyph type based on position
            glyph_idx = i % 7
            glyph_name = list(GLYPHS.keys())[glyph_idx]
            points.append((x, y, glyph_name, i))
        return points
    
    def render_frame(self, frame_idx):
        """Render a single frame."""
        # Create figure
        fig, ax = plt.subplots(figsize=(self.figsize[0]/self.dpi, 
                                        self.figsize[1]/self.dpi), 
                               dpi=self.dpi)
        ax.set_xlim(-15, 15)
        ax.set_ylim(-15, 15)
        ax.set_aspect('equal')
        ax.axis('off')
        fig.patch.set_facecolor('#0f0f1a')
        
        # Animation parameters
        t = frame_idx / self.frames  # 0 to 1
        rotation = t * 2 * np.pi  # Full rotation
        scale = 1.0 + 0.1 * np.sin(t * 2 * np.pi)  # Breathing effect
        
        # Generate points
        points = self.phyllotaxis_points(self.n_points, scale, rotation)
        
        # Draw vesica piscis at center
        center_alpha = 0.3 + 0.2 * np.sin(t * 2 * np.pi)
        vesica = Wedge((0, 0), 2, 0, 360, width=0.5, 
                       facecolor=GLYPHS['VESICA'], 
                       edgecolor='none', 
                       alpha=center_alpha)
        ax.add_patch(vesica)
        
        # Draw phyllotaxis points
        for x, y, glyph, idx in points:
            # Size based on distance from center
            dist = np.sqrt(x*x + y*y)
            size = 0.3 + 0.4 * (1 - dist / 15)
            
            # Alpha based on frame for wave effect
            wave = np.sin(t * 2 * np.pi + idx * 0.1) * 0.3 + 0.7
            
            circle = Circle((x, y), size * 0.5, 
                          facecolor=GLYPHS[glyph],
                          edgecolor='white',
                          linewidth=0.5,
                          alpha=wave)
            ax.add_patch(circle)
        
        # Title
        ax.text(0, 14, 'φ⁷ Golden Angle Morph', 
               ha='center', fontsize=16, color='white', 
               fontweight='bold', family='monospace')
        ax.text(0, -14, f'Frame {frame_idx+1}/{self.frames} | κ = 1.0', 
               ha='center', fontsize=10, color='#888888', 
               family='monospace')
        
        plt.tight_layout(pad=0)
        return fig, ax
    
    def generate_gif(self, output_path='golden_angle_morph.gif'):
        """Generate animated GIF."""
        print(f"Generating {self.frames} frames...")
        
        # Render all frames
        frames_data = []
        for i in range(self.frames):
            fig, ax = self.render_frame(i)
            fig.canvas.draw()
            
            # Convert to array using buffer_rgba
            buf = fig.canvas.buffer_rgba()
            ncols, nrows = fig.canvas.get_width_height()
            data = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 4)
            # Convert RGBA to RGB
            data = data[:, :, :3]
            frames_data.append(data)
            
            plt.close(fig)
            if (i + 1) % 10 == 0:
                print(f"  Frame {i+1}/{self.frames} rendered")
        
        # Create animation
        print(f"Creating GIF: {output_path}")
        fig, ax = plt.subplots(figsize=(self.figsize[0]/self.dpi, 
                                        self.figsize[1]/self.dpi),
                               dpi=self.dpi)
        ax.axis('off')
        fig.patch.set_facecolor('#0f0f1a')
        
        im = ax.imshow(frames_data[0])
        
        def update(frame):
            im.set_array(frames_data[frame])
            return [im]
        
        anim = animation.FuncAnimation(fig, update, frames=self.frames,
                                      interval=33, blit=True)  # 30fps
        
        anim.save(output_path, writer='pillow', fps=30, dpi=self.dpi)
        plt.close(fig)
        
        print(f"✅ GIF saved: {output_path}")
        return output_path


def main():
    """Generate golden angle morph GIF."""
    import sys
    
    output = sys.argv[1] if len(sys.argv) > 1 else '/tmp/golden_angle_morph.gif'
    
    morph = GoldenAngleMorph(n_points=150, figsize=(600, 600), dpi=80)
    result = morph.generate_gif(output)
    
    # Get file size
    import os
    size = os.path.getsize(result)
    print(f"File size: {size/1024:.1f} KB")
    
    return result


if __name__ == '__main__':
    main()
