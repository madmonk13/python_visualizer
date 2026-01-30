#!/usr/bin/env python3
"""
Psychedelic Music Visualizer - Main Module (Hardware Accelerated)
Orchestrates all components to render audio-reactive video with GPU encoding
"""

import numpy as np
import cv2
from PIL import Image
import subprocess
import os
import tempfile
from tqdm import tqdm
import math
import copy
import sys

from config import (
    FREQUENCY_BANDS, COLOR_PALETTES, 
    HUE_SHIFT_BASE, TRAIL_FADE_FACTOR, FADE_DURATION_SECONDS
)
from audio_processor import AudioProcessor
from effects import EffectsRenderer
from beat_detector import BeatDetector


class MusicVisualizer:
    def __init__(self, audio_path, output_path='output.mp4', cover_image_path=None, 
                 fps=30, resolution=(1280, 720), text_overlay=None, text_overlay2=None,
                 color_palette='rainbow', waveform_rotation='none', ring_rotation='none', 
                 starfield_rotation='none', starfield_direction='outward', preview_seconds=None,
                 cover_shape='square', cover_size=1.0, disable_rings=False, 
                 disable_starfield=False, ring_shape='circle', ring_count=3, ring_scale=1.0, 
                 waveform_orientation='horizontal', static_cover=False,
                 cover_timeline='none', ring_stagger='none', waveform_rotation_speed=1.0,
                 ring_rotation_speed=1.0, text_size=1.0, text_h_align='center', 
                 text_v_align='bottom'):
        
        self.audio_path = audio_path
        self.output_path = output_path
        self.cover_image_path = cover_image_path
        self.fps = fps
        self.width, height = resolution
        self.height = height
        self.text_overlay = text_overlay
        self.text_overlay2 = text_overlay2
        self.color_palette = color_palette
        self.waveform_rotation = waveform_rotation
        self.waveform_rotation_speed = waveform_rotation_speed
        self.ring_rotation = ring_rotation
        self.ring_rotation_speed = ring_rotation_speed
        self.starfield_rotation = starfield_rotation
        self.starfield_direction = starfield_direction
        self.preview_seconds = preview_seconds
        self.is_preview = preview_seconds is not None
        self.cover_shape = cover_shape
        self.cover_size = cover_size
        self.disable_rings = disable_rings
        self.disable_starfield = disable_starfield
        self.ring_shape = ring_shape
        self.ring_count = ring_count
        self.ring_scale = ring_scale
        self.waveform_orientation = waveform_orientation
        self.static_cover = static_cover
        self.cover_timeline = cover_timeline
        self.ring_stagger = ring_stagger
        self.text_size = text_size
        self.text_h_align = text_h_align
        self.text_v_align = text_v_align
        
        # Initialize components
        self.audio_processor = AudioProcessor(audio_path, fps=fps, is_preview=self.is_preview)
        self.effects_renderer = EffectsRenderer(self.width, self.height, is_preview=self.is_preview)
        self.beat_detector = BeatDetector()
        
        # Get duration from audio processor
        self.duration = self.audio_processor.duration
        
        # Setup frequency bands with color palette
        self.bands = self._setup_bands()
        
        # Calculate rotation speeds that complete whole rotations
        self._calculate_rotation_speeds()
        
        # Animation state
        self.rotation = 0
        self.cover_rotation = 0
        self.hue_offset = 0
        
        # Text fade tracking
        self.text_fade_history = []
        
        # Trail buffer for afterimage effect
        self.trail_buffer = None
        
        # Load cover image if provided
        self.cover_image = None
        if cover_image_path:
            try:
                self.cover_image = Image.open(cover_image_path).convert('RGB')
                print(f"Loaded cover image: {cover_image_path}")
            except Exception as e:
                print(f"Could not load cover image: {e}")
    
    def _setup_bands(self):
        """Setup frequency bands with color palette applied"""
        bands = copy.deepcopy(FREQUENCY_BANDS)
        
        if self.color_palette in COLOR_PALETTES:
            palette = COLOR_PALETTES[self.color_palette]
            for i, band in enumerate(bands):
                band['hue_offset'] = palette['colors'][i % len(palette['colors'])]
                band['saturation'] = palette['saturation']
                band['brightness'] = palette['brightness']
        else:
            print(f"Warning: Palette '{self.color_palette}' not found, using rainbow")
            for band in bands:
                band['saturation'] = 1.0
                band['brightness'] = 1.0
        
        return bands
    
    def _calculate_rotation_speeds(self):
        """Calculate rotation speeds that complete whole rotations over song duration"""
        # Get total number of frames (accounting for preview mode)
        if self.preview_seconds:
            total_duration = min(self.preview_seconds, self.duration)
        else:
            total_duration = self.duration
        
        total_frames = int(total_duration * self.fps)
        
        # Calculate how many rotations look good based on duration
        # Roughly 1 rotation per 3 minutes
        target_rotations = max(1, round(total_duration / 180))
        
        # Calculate the exact speed needed for whole rotations
        total_radians_needed = target_rotations * 2 * math.pi
        self.base_rotation_speed = total_radians_needed / total_frames
        
        # Volume multiplier should be small enough that it doesn't break the sync
        self.volume_rotation_multiplier = self.base_rotation_speed * 5
        
        print(f"Rotation sync: {target_rotations} rotation(s) over {total_duration:.1f}s")
        print(f"  Base speed: {self.base_rotation_speed:.6f} rad/frame")
        print(f"  Volume multiplier: {self.volume_rotation_multiplier:.6f}")
        print(f"  Waveform speed multiplier: {self.waveform_rotation_speed:.2f}x")
        print(f"  Ring speed multiplier: {self.ring_rotation_speed:.2f}x")
    
    def _calculate_cover_timeline_transform(self, progress):
        """
        Calculate cover transform based on timeline progress (0.0 to 1.0)
        Returns: (visible, scale, offset_x, offset_y, alpha)
        """
        if self.cover_timeline == 'none':
            return (True, 1.0, 0, 0, 1.0)
        
        # Timeline: 0-25% visible, 25-37.5% remove, 37.5-62.5% hidden, 62.5-75% return, 75-100% visible
        
        if progress < 0.25:
            # First quarter: visible
            return (True, 1.0, 0, 0, 1.0)
        
        elif progress < 0.375:
            # Remove action (12.5% duration)
            transition_progress = (progress - 0.25) / 0.125
            
            if self.cover_timeline == 'fade':
                alpha = 1.0 - transition_progress
                return (True, 1.0, 0, 0, alpha)
            
            elif self.cover_timeline == 'zoom':
                scale = 1.0 - transition_progress
                alpha = 1.0 - transition_progress
                return (True, scale, 0, 0, alpha)
            
            elif self.cover_timeline == 'slide_up':
                offset_y = -int(transition_progress * self.height)
                return (True, 1.0, 0, offset_y, 1.0)
            
            elif self.cover_timeline == 'slide_down':
                offset_y = int(transition_progress * self.height)
                return (True, 1.0, 0, offset_y, 1.0)
        
        elif progress < 0.625:
            # Hidden (25% duration)
            return (False, 0.0, 0, 0, 0.0)
        
        elif progress < 0.75:
            # Bring back action (12.5% duration)
            transition_progress = (progress - 0.625) / 0.125
            
            if self.cover_timeline == 'fade':
                alpha = transition_progress
                return (True, 1.0, 0, 0, alpha)
            
            elif self.cover_timeline == 'zoom':
                scale = transition_progress
                alpha = transition_progress
                return (True, scale, 0, 0, alpha)
            
            elif self.cover_timeline == 'slide_up':
                # Come in from bottom (negative at start, 0 at end)
                offset_y = int((1.0 - transition_progress) * self.height)
                return (True, 1.0, 0, offset_y, 1.0)
            
            elif self.cover_timeline == 'slide_down':
                # Come in from top (positive at start, 0 at end)
                offset_y = -int((1.0 - transition_progress) * self.height)
                return (True, 1.0, 0, offset_y, 1.0)
        
        else:
            # Last quarter: visible
            return (True, 1.0, 0, 0, 1.0)
    
    def _calculate_ring_stagger_offsets(self, frame_idx, total_frames):
        """
        Calculate rotation offsets for each ring based on stagger pattern
        Returns: tuple of offsets in radians for each ring (dynamic based on ring_count)
        """
        if self.ring_stagger == 'none' or self.ring_rotation == 'none':
            return tuple([0] * self.ring_count)
        
        progress = frame_idx / total_frames if total_frames > 0 else 0
        offsets = []
        
        for r in range(self.ring_count):
            if self.ring_stagger == 'inner_catch':
                # Inner rings start behind, catch up progressively
                offset = -math.pi / 2 * (1 - progress) * (1 - r / max(self.ring_count - 1, 1))
                
            elif self.ring_stagger == 'outer_catch':
                # Outer rings start behind, catch up progressively
                offset = -math.pi / 2 * (1 - progress) * (r / max(self.ring_count - 1, 1))
                
            elif self.ring_stagger == 'inner_lead':
                # Inner rings oscillate ahead and behind
                cycle_frequency = 2
                phase = r / max(self.ring_count - 1, 1) * math.pi / 3
                offset = math.sin(progress * cycle_frequency * 2 * math.pi + phase) * math.pi / 3
                
            elif self.ring_stagger == 'outer_lead':
                # Outer rings oscillate ahead and behind
                cycle_frequency = 2
                phase = (1 - r / max(self.ring_count - 1, 1)) * math.pi / 3
                offset = math.sin(progress * cycle_frequency * 2 * math.pi + phase) * math.pi / 3
                
            else:
                offset = 0
            
            offsets.append(offset)
        
        return tuple(offsets)
    
    def render_frame(self, frame_idx, total_frames):
        """Render a single frame with all psychedelic effects"""
        # Calculate volume intensity
        band_values = self.audio_processor.get_band_values(frame_idx, self.bands)
        avg_volume = np.mean(band_values) if band_values else 0
        max_possible = np.max(self.audio_processor.magnitude) if np.max(self.audio_processor.magnitude) > 0 else 1
        volume_intensity = avg_volume / max_possible
        
        # Detect beats
        beat_intensity = self.beat_detector.detect_beat(
            frame_idx, 
            self.audio_processor.frequencies, 
            self.audio_processor.magnitude
        )
        
        # Update animation state using calculated rotation speeds with speed multipliers
        rotation_speed = self.base_rotation_speed + (volume_intensity * self.volume_rotation_multiplier)
        
        # Apply separate speed multipliers for waveform and ring rotations
        self.rotation += rotation_speed * self.waveform_rotation_speed
        self.cover_rotation -= rotation_speed * self.ring_rotation_speed * 2
        self.hue_offset = (self.hue_offset + HUE_SHIFT_BASE + volume_intensity) % 360
        
        # Initialize or fade trail buffer
        if self.trail_buffer is None:
            self.trail_buffer = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        else:
            trail_array = np.array(self.trail_buffer)
            trail_array = (trail_array * TRAIL_FADE_FACTOR).astype(np.uint8)
            self.trail_buffer = Image.fromarray(trail_array)
        
        # Start with faded trail
        img = self.trail_buffer.copy()
        
        # Draw starfield (behind everything) - NOW WITH DIRECTION
        if not self.disable_starfield:
            self.effects_renderer.update_starfield(volume_intensity, self.starfield_rotation, self.starfield_direction)
            self.effects_renderer.draw_starfield(img, volume_intensity)
        
        # Create separate canvas for waveforms
        waveform_canvas = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        
        # Draw waveforms
        self.effects_renderer.draw_waveforms_with_glow(
            waveform_canvas, frame_idx, self.bands, 
            self.hue_offset, self.audio_processor, self.waveform_orientation
        )
        
        # Rotate waveforms based on rotation setting
        if self.waveform_rotation == 'none':
            waveform_rotated = waveform_canvas
        elif self.waveform_rotation == 'cw':
            # Clockwise rotation (positive angle)
            waveform_rotated = waveform_canvas.rotate(
                math.degrees(self.rotation), expand=False, 
                fillcolor=(0, 0, 0), resample=Image.BILINEAR
            )
        elif self.waveform_rotation == 'ccw':
            # Counter-clockwise rotation (negative angle)
            waveform_rotated = waveform_canvas.rotate(
                -math.degrees(self.rotation), expand=False, 
                fillcolor=(0, 0, 0), resample=Image.BILINEAR
            )
        else:
            waveform_rotated = waveform_canvas
        
        # Composite rotated waveforms
        img_array = np.array(img)
        waveform_array = np.array(waveform_rotated)
        mask = (waveform_array.sum(axis=2) > 0)
        img_array[mask] = waveform_array[mask]
        img = Image.fromarray(img_array)
        
        # Calculate timeline-based cover transform
        progress = frame_idx / total_frames if total_frames > 0 else 0
        cover_visible, cover_scale, cover_offset_x, cover_offset_y, cover_alpha = \
            self._calculate_cover_timeline_transform(progress)
        
        # Calculate ring stagger offsets
        ring_offsets = self._calculate_ring_stagger_offsets(frame_idx, total_frames)
        
        # Draw cover/rings on top (use cover_rotation which is affected by ring_rotation_speed)
        base_size = int(min(self.width, self.height) * 0.525 * self.cover_size)
        
        # Apply timeline scale ONLY to cover, not to ring base size
        if cover_visible and cover_scale > 0:
            timeline_cover_size = int(base_size * cover_scale)
            
            self.effects_renderer.draw_cover_and_rings(
                img=img,
                cover_image=self.cover_image,
                base_size=base_size,  # Rings use original base_size
                cover_size_override=timeline_cover_size,  # Cover uses scaled size
                volume_intensity=volume_intensity,
                beat_intensity=beat_intensity,
                rotation=self.cover_rotation,  # This rotation is affected by ring_rotation_speed
                hue_offset=self.hue_offset,
                bands=self.bands,
                cover_shape=self.cover_shape,
                ring_rotation=self.ring_rotation,
                disable_rings=self.disable_rings,
                ring_shape=self.ring_shape,
                ring_count=self.ring_count,
                ring_scale=self.ring_scale,
                static_cover=self.static_cover,
                cover_offset_x=cover_offset_x,
                cover_offset_y=cover_offset_y,
                cover_alpha=cover_alpha,
                ring_stagger_offsets=ring_offsets
            )
        else:
            # Still draw rings even if cover is hidden
            self.effects_renderer.draw_cover_and_rings(
                img=img,
                cover_image=None,  # No cover
                base_size=base_size,
                cover_size_override=base_size,
                volume_intensity=volume_intensity,
                beat_intensity=beat_intensity,
                rotation=self.cover_rotation,
                hue_offset=self.hue_offset,
                bands=self.bands,
                cover_shape=self.cover_shape,
                ring_rotation=self.ring_rotation,
                disable_rings=self.disable_rings,
                ring_shape=self.ring_shape,
                ring_count=self.ring_count,
                ring_scale=self.ring_scale,
                static_cover=self.static_cover,
                cover_offset_x=0,
                cover_offset_y=0,
                cover_alpha=1.0,
                ring_stagger_offsets=ring_offsets
            )
        
        # Draw text overlay
        if self.text_overlay or self.text_overlay2:
            self.effects_renderer.draw_text_overlay(
                img, self.text_overlay, self.text_overlay2, beat_intensity, 
                volume_intensity, self.text_fade_history, self.cover_image, base_size,
                self.text_size, self.text_h_align, self.text_v_align
            )
        
        # Update trail buffer
        self.trail_buffer = img.copy()
        
        # Apply fade to black at the end
        fade_frames = int(FADE_DURATION_SECONDS * self.fps)
        frames_from_end = total_frames - frame_idx
        
        if frames_from_end <= fade_frames:
            fade_amount = 1.0 - (frames_from_end / fade_frames)
            img_array = np.array(img)
            img_array = (img_array * (1 - fade_amount)).astype(np.uint8)
            img = Image.fromarray(img_array)
        
        return img
    
    def render(self):
        """Render the complete video with audio using hardware-accelerated encoding"""
        # Calculate frames
        if self.preview_seconds:
            render_duration = min(self.preview_seconds, self.duration)
            total_frames = int(render_duration * self.fps)
            print(f"⚡ PREVIEW MODE: Rendering first {render_duration:.1f}s")
        else:
            render_duration = self.duration
            total_frames = int(render_duration * self.fps)
        
        print(f"🚀 Hardware Acceleration: VideoToolbox (Apple Silicon)")
        print(f"Rendering {total_frames} frames at {self.fps} fps...")
        
        # Setup FFmpeg with hardware encoding (VideoToolbox for macOS)
        ffmpeg_cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', f'{self.width}x{self.height}',
            '-pix_fmt', 'rgb24',
            '-r', str(self.fps),
            '-i', '-',  # Read from stdin
            '-i', self.audio_path,  # Audio input
            '-c:v', 'h264_videotoolbox',  # Hardware encoder for macOS
            '-b:v', '8M',  # Bitrate
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-t', str(render_duration),  # Duration limit
            self.output_path
        ]
        
        # Start FFmpeg process
        try:
            process = subprocess.Popen(
                ffmpeg_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except FileNotFoundError:
            print("ERROR: FFmpeg not found. Please install it:")
            print("  brew install ffmpeg")
            return
        
        # Render frames and pipe to FFmpeg
        try:
            for frame_idx in tqdm(range(total_frames)):
                img = self.render_frame(frame_idx, total_frames)
                
                # Convert PIL Image to raw RGB bytes
                frame_bytes = img.tobytes()
                
                # Write to FFmpeg stdin
                process.stdin.write(frame_bytes)
            
            # Close stdin to signal end of input
            process.stdin.close()
            
            # Wait for FFmpeg to finish
            process.wait()
            
            if process.returncode == 0:
                print(f"\n✅ Video saved to: {self.output_path}")
            else:
                stderr_output = process.stderr.read().decode('utf-8')
                print(f"\n❌ FFmpeg error (return code {process.returncode}):")
                print(stderr_output[-1000:])  # Last 1000 chars of error
                
        except KeyboardInterrupt:
            print("\n⚠️  Render interrupted by user")
            process.terminate()
            process.wait()
        except Exception as e:
            print(f"\n❌ Error during render: {e}")
            process.terminate()
            process.wait()
            import traceback
            traceback.print_exc()