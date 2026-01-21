"""
Visual effects module - Main coordinator
Imports and delegates to specialized effect modules
"""

from effects_starfield import StarfieldEffect
from effects_waveforms import WaveformRenderer
from effects_rings import RingRenderer


class EffectsRenderer:
    """Main effects renderer that coordinates all visual effects"""
    
    def __init__(self, width, height, is_preview=False):
        self.width = width
        self.height = height
        self.is_preview = is_preview
        
        # Initialize sub-renderers
        self.starfield = StarfieldEffect(width, height, is_preview)
        self.waveforms = WaveformRenderer(width, height, is_preview)
        self.rings = RingRenderer(width, height)
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convenience method for color conversion"""
        return WaveformRenderer.hsv_to_rgb(h, s, v)
    
    def update_starfield(self, volume_intensity, rotation_mode='none'):
        """Update starfield particle positions"""
        self.starfield.update(volume_intensity, rotation_mode)
    
    def draw_starfield(self, img, volume_intensity):
        """Draw the starfield effect"""
        self.starfield.draw(img, volume_intensity)
    
    def draw_waveforms_with_glow(self, img, frame_idx, bands, hue_offset, 
                                 audio_processor, orientation='horizontal'):
        """Draw frequency band waveforms"""
        self.waveforms.draw(img, frame_idx, bands, hue_offset, 
                          audio_processor, orientation)
    
    def draw_cover_and_rings(self, img, cover_image, base_size, volume_intensity, 
                            beat_intensity, rotation, hue_offset, bands, 
                            cover_shape='square', ring_rotation='none', 
                            disable_rings=False, ring_shape='circle',
                            ring_count=3, ring_scale=1.0, static_cover=False, 
                            cover_offset_x=0, cover_offset_y=0, cover_alpha=1.0, 
                            cover_size_override=None, ring_stagger_offsets=(0, 0, 0)):
        """Draw cover art and reactive rings"""
        self.rings.draw_cover_and_rings(
            img, cover_image, base_size, volume_intensity, 
            beat_intensity, rotation, hue_offset, bands, 
            cover_shape, ring_rotation, disable_rings, ring_shape,
            ring_count, ring_scale, static_cover,
            cover_offset_x, cover_offset_y, cover_alpha, cover_size_override,
            ring_stagger_offsets
        )
    
    def draw_text_overlay(self, img, text, text2, beat_intensity, volume_intensity, 
                         text_fade_history, cover_image, base_size, text_size=1.0,
                         text_h_align='center', text_v_align='bottom'):
        """Draw text overlay"""
        self.rings.draw_text_overlay(
            img, text, text2, beat_intensity, volume_intensity, 
            text_fade_history, cover_image, base_size, text_size,
            text_h_align, text_v_align
        )