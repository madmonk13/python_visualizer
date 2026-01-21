"""
Ring and cover art rendering module
Handles cover image display and reactive ring effects
Uses modular ring shape system
"""

import math
import numpy as np
from PIL import Image, ImageDraw
import rings


class RingRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convert HSV to RGB (0-255 range) with enhanced vibrancy"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        # Boost saturation and brightness for more vibrant colors
        r = int(min(255, (r + m) * 255 * 1.2))
        g = int(min(255, (g + m) * 255 * 1.2))
        b = int(min(255, (b + m) * 255 * 1.2))
        
        return (r, g, b)
    
    def draw_cover_and_rings(self, img, cover_image, base_size, volume_intensity, 
                            beat_intensity, rotation, hue_offset, bands, 
                            cover_shape='square', ring_rotation='none', 
                            disable_rings=False, ring_shape='circle',
                            ring_count=3, ring_scale=1.0, static_cover=False, 
                            cover_offset_x=0, cover_offset_y=0, cover_alpha=1.0, 
                            cover_size_override=None, ring_stagger_offsets=(0, 0, 0)):
        """Draw cover art and reactive rings"""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Apply timeline offsets to center position (for cover only, not rings)
        cover_center_x = center_x + cover_offset_x
        cover_center_y = center_y + cover_offset_y
        
        # Use override size for cover if provided, otherwise use base_size
        cover_base_size = cover_size_override if cover_size_override is not None else base_size
        
        # Draw cover
        if cover_image and cover_alpha > 0:
            if cover_shape == 'square':
                # Apply volume/beat reaction only if not static
                if static_cover:
                    cover_width = int(cover_base_size * 1.2)
                    cover_height = int(cover_base_size * 1.2)
                else:
                    # Add beat and volume reaction to square covers
                    reaction = 1 + volume_intensity * 0.3 + beat_intensity * 0.5
                    cover_width = int(cover_base_size * 1.2 * reaction)
                    cover_height = int(cover_base_size * 1.2 * reaction)
                
                # Safety check: ensure dimensions are valid
                if cover_width < 1 or cover_height < 1:
                    # Skip drawing if too small
                    pass
                else:
                    cover_resized = cover_image.resize((cover_width, cover_height))
                    
                    # Apply alpha if needed
                    if cover_alpha < 1.0:
                        cover_resized = cover_resized.convert('RGBA')
                        alpha_layer = Image.new('L', cover_resized.size, int(255 * cover_alpha))
                        cover_resized.putalpha(alpha_layer)
                        img.paste(cover_resized, (cover_center_x - cover_width // 2, cover_center_y - cover_height // 2), cover_resized)
                    else:
                        img.paste(cover_resized, (cover_center_x - cover_width // 2, cover_center_y - cover_height // 2))
                    
            else:  # round
                # Apply volume/beat reaction only if not static
                if static_cover:
                    center_size = int(cover_base_size * 0.6)
                else:
                    center_size = int(cover_base_size * 0.6 * (1 + volume_intensity * 0.3 + beat_intensity * 0.5))
                
                # Safety check: ensure dimensions are valid
                if center_size < 1:
                    # Skip drawing if too small
                    pass
                else:
                    center_cover = cover_image.resize((center_size * 2, center_size * 2))
                    center_cover = center_cover.convert('RGBA')
                    
                    mask = Image.new('L', (center_size * 2, center_size * 2), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.ellipse([0, 0, center_size * 2, center_size * 2], fill=int(255 * cover_alpha))
                    
                    center_cover.putalpha(mask)
                    img.paste(center_cover, (cover_center_x - center_size, cover_center_y - center_size), center_cover)
        
        # Build list of which rings to draw based on ring_count
        # Map to waveform bands: highest frequency (innermost) to lowest (outermost)
        # Total 8 bands available, when ring_count < 8, remove from outside (lowest frequencies)
        total_bands = 8
        if ring_count > 0:
            # Start from the highest frequency bands (end of list) and work backwards
            rings_to_draw = list(range(total_bands - ring_count, total_bands))
        else:
            rings_to_draw = []
        
        # Draw rings if not disabled and we have at least one ring to draw
        # Rings are always drawn at original center (no offset applied)
        if not disable_rings and len(rings_to_draw) > 0:
            # Get the ring shape instance
            ring_shape_instance = rings.get_ring_shape(ring_shape)
            
            if ring_shape_instance is None:
                print(f"Warning: Ring shape '{ring_shape}' not found, using circle")
                ring_shape_instance = rings.get_ring_shape('circle')
            
            # Calculate rotation angle based on ring_rotation setting
            if ring_rotation == 'cw':
                base_ring_angle = math.degrees(rotation)  # Clockwise
            elif ring_rotation == 'ccw':
                base_ring_angle = -math.degrees(rotation)  # Counter-clockwise
            else:  # 'none'
                base_ring_angle = 0
            
            # Optimization: Skip rotation entirely for circles when no rotation
            needs_rotation = base_ring_angle != 0
            
            # Optimization: Only use larger canvas if rotation is needed
            if needs_rotation:
                # Use larger canvas to prevent clipping when rotating
                canvas_size = max(self.width, self.height) * 2
                canvas_center_x = canvas_size // 2
                canvas_center_y = canvas_size // 2
            else:
                # No rotation needed - use normal canvas size
                canvas_size = None
                canvas_center_x = center_x
                canvas_center_y = center_y
            
            # Create ONE canvas for all rings (optimization: draw all rings together)
            if canvas_size:
                all_rings_layer = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            else:
                all_rings_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            
            all_rings_draw = ImageDraw.Draw(all_rings_layer)
            
            # Draw all rings on the single canvas
            for idx, band_idx in enumerate(rings_to_draw):
                # Size variation based on beat and volume, scaled by ring_scale
                # Spread rings more evenly with more rings
                ring_spacing = 0.15 if ring_count <= 3 else 0.12
                base_ring_size = base_size * (0.4 + idx * ring_spacing) * ring_scale
                beat_expansion = beat_intensity * 80
                volume_expansion = volume_intensity * 0.5 * base_ring_size
                ring_size = int(base_ring_size + beat_expansion + volume_expansion)
                
                # Use waveform band colors directly - band_idx maps to frequency band
                if bands and len(bands) > band_idx:
                    ring_hue = (hue_offset + bands[band_idx].get('hue_offset', 0)) % 360
                    sat = bands[band_idx].get('saturation', 1.0)
                    bright = bands[band_idx].get('brightness', 0.9)
                else:
                    # Fallback if no bands
                    ring_hue = (hue_offset + band_idx * 45) % 360
                    sat = 1.0
                    bright = 0.9
                
                ring_color = self.hsv_to_rgb(ring_hue, sat, bright)
                line_width = int(3 + volume_intensity * 4 + beat_intensity * 6)
                
                # Calculate stagger offset for this ring
                stagger_idx = idx % len(ring_stagger_offsets) if len(ring_stagger_offsets) > 0 else 0
                ring_stagger_angle = math.degrees(ring_stagger_offsets[stagger_idx]) if len(ring_stagger_offsets) > 0 else 0
                total_ring_angle = base_ring_angle + ring_stagger_angle
                
                # For staggered rotation, we need individual layers
                if ring_stagger_angle != 0 and needs_rotation:
                    # Need separate layer for this ring due to stagger
                    if canvas_size:
                        ring_layer = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
                    else:
                        ring_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                    ring_draw = ImageDraw.Draw(ring_layer)
                    
                    # Draw this ring using the modular shape
                    self._draw_modular_ring(ring_draw, canvas_center_x, canvas_center_y, 
                                          ring_size, ring_size, ring_shape_instance, 
                                          ring_color, line_width, beat_intensity)
                    
                    # Rotate this ring's layer
                    ring_layer = ring_layer.rotate(total_ring_angle, expand=False, 
                                                   fillcolor=(0, 0, 0, 0), 
                                                   resample=Image.BILINEAR)
                    
                    # Composite onto main rings layer
                    all_rings_layer = Image.alpha_composite(all_rings_layer, ring_layer)
                else:
                    # No stagger or no rotation - draw directly on all_rings_layer
                    self._draw_modular_ring(all_rings_draw, canvas_center_x, canvas_center_y, 
                                          ring_size, ring_size, ring_shape_instance, 
                                          ring_color, line_width, beat_intensity)
            
            # Apply rotation to ALL rings at once (if needed and no stagger)
            if needs_rotation and all(s == 0 for s in ring_stagger_offsets):
                all_rings_layer = all_rings_layer.rotate(base_ring_angle, expand=False, 
                                                        fillcolor=(0, 0, 0, 0), 
                                                        resample=Image.BILINEAR)
            
            # Crop and paste to final position if we used larger canvas
            if canvas_size:
                offset_x = (canvas_size - self.width) // 2
                offset_y = (canvas_size - self.height) // 2
                all_rings_layer = all_rings_layer.crop((offset_x, offset_y, 
                                                       offset_x + self.width, 
                                                       offset_y + self.height))
            
            # Composite all rings onto the main image
            img.paste(all_rings_layer, (0, 0), all_rings_layer)
    
    def _draw_modular_ring(self, draw, cx, cy, w, h, ring_shape_instance, color, width, beat):
        """Draw a ring using the modular ring shape system"""
        # Draw glow layers
        for glow in range(8, 0, -1):
            ring_shape_instance.draw_glow(draw, cx, cy, w, h, color, width, glow, beat)
        
        # Draw main ring outline
        ring_shape_instance.draw_outline(draw, cx, cy, w, h, color, width)
    
    def draw_text_overlay(self, img, text, text2, beat_intensity, volume_intensity, 
                         text_fade_history, cover_image, base_size, text_size=1.0,
                         text_h_align='center', text_v_align='bottom'):
        """Draw white text with consistent font size and configurable alignment"""
        if not text and not text2:
            return
        
        text_fade_history.append(volume_intensity)
        if len(text_fade_history) > 60:
            text_fade_history.pop(0)
        
        avg_recent_volume = np.mean(text_fade_history) if text_fade_history else 0
        base_alpha = 0.3 + (avg_recent_volume * 0.7)
        beat_boost = beat_intensity * 0.2
        alpha = min(1.0, base_alpha + beat_boost)
        
        text_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Use consistent font size for both lines
        try:
            from PIL import ImageFont
            font_size = int(self.height * 0.08 * text_size)
            font = None
            for font_name in ['Helvetica', 'Arial', 'DejaVuSans', 'FreeSans']:
                try:
                    font = ImageFont.truetype(font_name, font_size)
                    break
                except:
                    continue
            if not font:
                font = ImageFont.load_default()
        except:
            font = None
        
        shadow_offset = 3
        shadow_alpha = int(alpha * 180)
        text_alpha = int(alpha * 255)
        
        # Calculate vertical position based on alignment
        if text_v_align == 'top':
            y_start = int(self.height * 0.1)
        elif text_v_align == 'middle':
            y_start = int(self.height * 0.45)
        else:  # bottom
            if cover_image:
                cover_bottom = (self.height // 2) + base_size
                y_start = cover_bottom + 40
            else:
                y_start = int(self.height * 0.7)
        
        # Draw first line of text
        if text:
            if font:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
            else:
                text_width = len(text) * 10
            
            # Calculate horizontal position based on alignment
            if text_h_align == 'left':
                x = int(self.width * 0.05)
            elif text_h_align == 'right':
                x = int(self.width * 0.95) - text_width
            else:  # center
                x = (self.width - text_width) // 2
            
            # Shadow
            if font:
                draw.text((x + shadow_offset, y_start + shadow_offset), text, 
                         font=font, fill=(0, 0, 0, shadow_alpha))
            else:
                draw.text((x + shadow_offset, y_start + shadow_offset), text, 
                         fill=(0, 0, 0, shadow_alpha))
            
            # Main text
            if font:
                draw.text((x, y_start), text, font=font, fill=(255, 255, 255, text_alpha))
            else:
                draw.text((x, y_start), text, fill=(255, 255, 255, text_alpha))
        
        # Draw second line of text (same font size)
        if text2:
            y_line2 = y_start + (font_size if font else 25) + 10
            
            if font:
                bbox2 = draw.textbbox((0, 0), text2, font=font)
                text_width2 = bbox2[2] - bbox2[0]
            else:
                text_width2 = len(text2) * 8
            
            # Calculate horizontal position based on alignment
            if text_h_align == 'left':
                x2 = int(self.width * 0.05)
            elif text_h_align == 'right':
                x2 = int(self.width * 0.95) - text_width2
            else:  # center
                x2 = (self.width - text_width2) // 2
            
            # Shadow
            if font:
                draw.text((x2 + shadow_offset, y_line2 + shadow_offset), text2, 
                         font=font, fill=(0, 0, 0, shadow_alpha))
            else:
                draw.text((x2 + shadow_offset, y_line2 + shadow_offset), text2, 
                         fill=(0, 0, 0, shadow_alpha))
            
            # Main text
            if font:
                draw.text((x2, y_line2), text2, font=font, fill=(255, 255, 255, text_alpha))
            else:
                draw.text((x2, y_line2), text2, fill=(255, 255, 255, text_alpha))
        
        img.paste(text_layer, (0, 0), text_layer)