"""
Waveform rendering module
Handles drawing frequency band waveforms with glow effects
"""

import math
from PIL import Image, ImageDraw, ImageFilter


class WaveformRenderer:
    def __init__(self, width, height, is_preview=False):
        self.width = width
        self.height = height
        self.is_preview = is_preview
    
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
    
    def draw(self, img, frame_idx, bands, hue_offset, audio_processor, orientation='horizontal'):
        """Draw the frequency band waveforms with glow effects"""
        waveform_layer = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        waveform_draw = ImageDraw.Draw(waveform_layer)
        
        waveform_points = 100 if self.is_preview else 150
        
        if orientation == 'vertical':
            self._draw_vertical(waveform_draw, frame_idx, bands, hue_offset, 
                              audio_processor, waveform_points)
        else:
            self._draw_horizontal(waveform_draw, frame_idx, bands, hue_offset, 
                                audio_processor, waveform_points)
        
        blur_radius = 1 if self.is_preview else 2
        waveform_layer = waveform_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        img.paste(waveform_layer, (0, 0), None)
    
    def _draw_vertical(self, draw, frame_idx, bands, hue_offset, audio_processor, points):
        """Draw vertical orientation waveforms (columns top to bottom)"""
        band_width = self.width // len(bands)
        
        for band_idx, band in enumerate(bands):
            waveform = audio_processor.get_band_waveform(frame_idx, band_idx, bands, points=points)
            center_x = (band_idx + 0.5) * band_width
            
            base_hue = (hue_offset + band['hue_offset']) % 360
            sensitivity = 1.0 + (band_idx / (len(bands) - 1)) * 2.0
            
            # Draw two layers with mirroring
            for layer in range(2):
                layer_hue = (base_hue + layer * 40) % 360
                sat = band.get('saturation', 1.0)
                bright = band.get('brightness', 1.0)
                color = self.hsv_to_rgb(layer_hue, sat, bright)
                
                phase_offset = layer * 0.3
                
                points_left = []
                points_right = []
                
                for i, value in enumerate(waveform):
                    y = int((i / len(waveform)) * self.height)
                    t = i / len(waveform)
                    
                    amplitude = value * (band_width * 0.65) * sensitivity
                    wave1 = math.sin((t * math.pi * 4) + phase_offset) * amplitude
                    wave2 = math.sin((t * math.pi * 8) + (phase_offset * 2)) * (amplitude * 0.3)
                    wave3 = math.cos((t * math.pi * 2) + (hue_offset * 0.02)) * (amplitude * 0.2)
                    
                    x_left = int(center_x - (wave1 + wave2 + wave3))
                    x_right = int(center_x + wave1 + wave2 + wave3)
                    
                    points_left.append((x_left, y))
                    points_right.append((x_right, y))
                
                # Draw filled area
                if layer == 0 and len(points_left) > 1:
                    fill_points = points_left + points_right[::-1]
                    draw.polygon(fill_points, fill=color)
                
                # Draw glow halo
                if len(points_left) > 1:
                    glow_layers = 6 if self.is_preview else 12
                    
                    for thickness in range(glow_layers, 0, -1):
                        glow_intensity = (1 - thickness / glow_layers) * 0.5
                        glow_r = int(color[0] * glow_intensity)
                        glow_g = int(color[1] * glow_intensity)
                        glow_b = int(color[2] * glow_intensity)
                        glow_color = (glow_r, glow_g, glow_b)
                        
                        draw.line(points_left, fill=glow_color, width=thickness + 8)
                        draw.line(points_right, fill=glow_color, width=thickness + 8)
                    
                    draw.line(points_left, fill=color, width=6 - layer)
                    draw.line(points_right, fill=color, width=6 - layer)
                
                # Draw particles on peaks
                for i in range(0, len(waveform), 15):
                    if waveform[i] > 0.7:
                        y = int((i / len(waveform)) * self.height)
                        particle_hue = (base_hue + i * 2) % 360
                        particle_color = self.hsv_to_rgb(particle_hue, 1.0, 1.0)
                        
                        for radius in range(10, 2, -1):
                            glow_intensity = (1 - radius / 10) * 0.5
                            glow_r = int(particle_color[0] * glow_intensity)
                            glow_g = int(particle_color[1] * glow_intensity)
                            glow_b = int(particle_color[2] * glow_intensity)
                            draw.ellipse(
                                [center_x-radius, y-radius, center_x+radius, y+radius],
                                fill=(glow_r, glow_g, glow_b)
                            )
                        
                        draw.ellipse(
                            [center_x-3, y-3, center_x+3, y+3],
                            fill=particle_color
                        )
    
    def _draw_horizontal(self, draw, frame_idx, bands, hue_offset, audio_processor, points):
        """Draw horizontal orientation waveforms (rows left to right)"""
        band_height = self.height // len(bands)
        
        for band_idx, band in enumerate(bands):
            waveform = audio_processor.get_band_waveform(frame_idx, band_idx, bands, points=points)
            center_y = (band_idx + 0.5) * band_height
            
            base_hue = (hue_offset + band['hue_offset']) % 360
            sensitivity = 1.0 + (band_idx / (len(bands) - 1)) * 2.0
            
            # Draw two layers with mirroring
            for layer in range(2):
                layer_hue = (base_hue + layer * 40) % 360
                sat = band.get('saturation', 1.0)
                bright = band.get('brightness', 1.0)
                color = self.hsv_to_rgb(layer_hue, sat, bright)
                
                phase_offset = layer * 0.3
                
                points_upper = []
                points_lower = []
                
                for i, value in enumerate(waveform):
                    x = int((i / len(waveform)) * self.width)
                    t = i / len(waveform)
                    
                    amplitude = value * (band_height * 0.65) * sensitivity
                    wave1 = math.sin((t * math.pi * 4) + phase_offset) * amplitude
                    wave2 = math.sin((t * math.pi * 8) + (phase_offset * 2)) * (amplitude * 0.3)
                    wave3 = math.cos((t * math.pi * 2) + (hue_offset * 0.02)) * (amplitude * 0.2)
                    
                    y_upper = int(center_y + wave1 + wave2 + wave3)
                    y_lower = int(center_y - (wave1 + wave2 + wave3))
                    
                    points_upper.append((x, y_upper))
                    points_lower.append((x, y_lower))
                
                # Draw filled area
                if layer == 0 and len(points_upper) > 1:
                    fill_points = points_upper + points_lower[::-1]
                    draw.polygon(fill_points, fill=color)
                
                # Draw glow halo
                if len(points_upper) > 1:
                    glow_layers = 6 if self.is_preview else 12
                    
                    for thickness in range(glow_layers, 0, -1):
                        glow_intensity = (1 - thickness / glow_layers) * 0.5
                        glow_r = int(color[0] * glow_intensity)
                        glow_g = int(color[1] * glow_intensity)
                        glow_b = int(color[2] * glow_intensity)
                        glow_color = (glow_r, glow_g, glow_b)
                        
                        draw.line(points_upper, fill=glow_color, width=thickness + 8)
                        draw.line(points_lower, fill=glow_color, width=thickness + 8)
                    
                    draw.line(points_upper, fill=color, width=6 - layer)
                    draw.line(points_lower, fill=color, width=6 - layer)
                
                # Draw particles on peaks
                for i in range(0, len(waveform), 15):
                    if waveform[i] > 0.7:
                        x = int((i / len(waveform)) * self.width)
                        particle_hue = (base_hue + i * 2) % 360
                        particle_color = self.hsv_to_rgb(particle_hue, 1.0, 1.0)
                        
                        for radius in range(10, 2, -1):
                            glow_intensity = (1 - radius / 10) * 0.5
                            glow_r = int(particle_color[0] * glow_intensity)
                            glow_g = int(particle_color[1] * glow_intensity)
                            glow_b = int(particle_color[2] * glow_intensity)
                            draw.ellipse(
                                [x-radius, center_y-radius, x+radius, center_y+radius],
                                fill=(glow_r, glow_g, glow_b)
                            )
                        
                        draw.ellipse(
                            [x-3, center_y-3, x+3, center_y+3],
                            fill=particle_color
                        )